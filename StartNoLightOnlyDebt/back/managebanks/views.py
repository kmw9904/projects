import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import FinancialCompanySerializer
from .models import FinancialProduct, MortgageOption, JeonseOption, CreditLoanOption, FinancialCompany
from datetime import datetime
from decimal import Decimal


def calculate_bullet_repayment(loan_amount, annual_rate):
    """만기일시상환방식: 월 이자액 계산"""
    monthly_rate = Decimal(annual_rate) / 12 / 100
    return loan_amount * monthly_rate


def calculate_installment_repayment(loan_amount, annual_rate, months):
    """분할상환방식: 원리금 균등상환 월 상환액 계산"""
    monthly_rate = Decimal(annual_rate) / 12 / 100
    numerator = loan_amount * monthly_rate * (1 + monthly_rate) ** months
    denominator = (1 + monthly_rate) ** months - 1
    return numerator / denominator


class CalculateMonthlyPayment(APIView):
    """
    대출 상품 월 상환액 계산 API
    """
    def get(self, request, product_type, product_id):
        loan_amount = request.query_params.get('loan_amount')
        months = request.query_params.get('months')

        # 필수 파라미터 검증
        if not loan_amount or not months:
            return Response({"error": "loan_amount와 months는 필수 입력값입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan_amount = Decimal(loan_amount)
            months = int(months)
        except (ValueError, TypeError):
            return Response({"error": "loan_amount는 숫자, months는 정수여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 데이터베이스 조회
        if product_type == "jeonse":
            options = JeonseOption.objects.filter(option_id__icontains=product_id)
        elif product_type == "mortgage":
            options = MortgageOption.objects.filter(option_id__icontains=product_id)
        elif product_type == "credit":
            options = CreditLoanOption.objects.filter(option_id__icontains=product_id)
        else:
            return Response({"error": "지원하지 않는 상품 유형입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not options.exists():
            return Response({"error": f"{product_type} 상품에 대한 옵션 데이터를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 월 상환액 계산
        results = []
        for option in options:
            if product_type == "credit":
                # 신용 대출: crdt_grad_avg(평균 금리) 사용
                annual_rate = option.crdt_grad_avg
                if not annual_rate:
                    continue
                min_payment = calculate_installment_repayment(loan_amount, annual_rate, months)
                max_payment = min_payment  # 신용 대출에서는 단일 금리 사용
            else:
                # 전세, 주택담보 대출: lend_rate_min, lend_rate_max 사용
                lend_rate_min = option.lend_rate_min
                lend_rate_max = option.lend_rate_max
                rpay_type_nm = getattr(option, "rpay_type_nm", "분할상환방식")

                if not lend_rate_min or not lend_rate_max:
                    continue

                if rpay_type_nm == "만기일시상환방식":
                    min_payment = calculate_bullet_repayment(loan_amount, lend_rate_min)
                    max_payment = calculate_bullet_repayment(loan_amount, lend_rate_max)
                elif rpay_type_nm == "분할상환방식":
                    min_payment = calculate_installment_repayment(loan_amount, lend_rate_min, months)
                    max_payment = calculate_installment_repayment(loan_amount, lend_rate_max, months)
                else:
                    continue

            results.append({
                "option_id": option.option_id,
                "rpay_type_nm": getattr(option, "rpay_type_nm", "분할상환방식"),
                "lend_rate_min": lend_rate_min if product_type != "credit" else annual_rate,
                "lend_rate_max": lend_rate_max if product_type != "credit" else annual_rate,
                "monthly_payment_min": round(min_payment, 2),
                "monthly_payment_max": round(max_payment, 2),
            })

        return Response({"calculations": results}, status=status.HTTP_200_OK)


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except (ValueError, TypeError):
        return None

class FetchFinancialData(APIView):
    def get(self, request):
        # API 엔드포인트와 인증키
        endpoints = {
            'credit': 'https://finlife.fss.or.kr/finlifeapi/creditLoanProductsSearch.json',
            'jeonse': 'https://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json',
            'mortgage': 'https://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json',
            'company': 'https://finlife.fss.or.kr/finlifeapi/companySearch.json',  # 금융회사 API 추가
        }
        auth_key = 'a9151a31e6015873973e2a2402878959'
        params = {'auth': auth_key, 'topFinGrpNo': '020000', 'pageNo': 1}

        all_responses = {}
        for key, url in endpoints.items():
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    all_responses[key] = data
                    if key == 'company':
                        self.process_company_data(data)
                    else:
                        self.process_data(key, data)
                else:
                    all_responses[key] = {
                        "error": f"Failed to fetch data: {response.status_code}",
                        "details": response.text,
                    }
            except requests.RequestException as e:
                all_responses[key] = {"error": str(e)}

        return Response(all_responses, status=status.HTTP_200_OK)

    def process_company_data(self, data):
        result = data.get('result', {})
        base_list = result.get('baseList', [])

        for company_data in base_list:
            fin_co_no = company_data.get('fin_co_no')
            kor_co_nm = company_data.get('kor_co_nm')
            homp_url = company_data.get('homp_url')

            if not fin_co_no:
                continue

            FinancialCompany.objects.update_or_create(
                company_id=fin_co_no,
                defaults={'company_name': kor_co_nm, 'homp_url': homp_url},
            )

    def process_data(self, key, data):
        result = data.get('result', {})
        base_list = result.get('baseList', [])
        option_list = result.get('optionList', [])

        for product_data in base_list:
            fin_co_no = product_data.get('fin_co_no')
            fin_co_name = product_data.get('kor_co_nm')
            if not fin_co_no:
                print(f"Missing fin_co_no for product {product_data.get('fin_prdt_cd')}")
                continue

            financial_company, _ = FinancialCompany.objects.get_or_create(
                company_id=fin_co_no,
                defaults={'company_name': fin_co_name},
            )

            FinancialProduct.objects.update_or_create(
                product_id=product_data['fin_prdt_cd'],
                defaults={
                    'fin_co_no': financial_company,
                    'product_name': product_data.get('fin_prdt_nm'),
                    'join_way': product_data.get('join_way'),
                    'loan_inci_expn': product_data.get('loan_inci_expn'),
                    'erly_rpay_fee': product_data.get('erly_rpay_fee'),
                    'dly_rate': product_data.get('dly_rate'),
                    'loan_lmt': product_data.get('loan_lmt'),
                    'dcls_month': parse_date(product_data.get('dcls_month')),
                    'dcls_strt_day': parse_date(product_data.get('dcls_strt_day')),
                    'dcls_end_day': parse_date(product_data.get('dcls_end_day')),
                    'fin_co_subm_day': parse_date(product_data.get('fin_co_subm_day')),
                    'prdt_div': product_data.get('prdt_div'),
                },
            )

        self.process_options(key, option_list)

    def process_options(self, key, option_list):
        for option_data in option_list:
            product = FinancialProduct.objects.filter(
                product_id=option_data.get('fin_prdt_cd')
            ).first()
            if not product:
                continue

            if key == 'credit':
                CreditLoanOption.objects.update_or_create(
                    option_id=f"{option_data['fin_prdt_cd']}_{option_data['crdt_lend_rate_type']}_opt",
                    defaults={
                        'dcls_month': parse_date(option_data.get('dcls_month')),
                        'crdt_prdt_type': option_data.get('crdt_prdt_type'),
                        'crdt_lend_rate_type': option_data.get('crdt_lend_rate_type'),
                        'crdt_lend_rate_type_nm': option_data.get('crdt_lend_rate_type_nm'),
                        'crdt_grad_1': option_data.get('crdt_grad_1'),
                        'crdt_grad_4': option_data.get('crdt_grad_4'),
                        'crdt_grad_5': option_data.get('crdt_grad_5'),
                        'crdt_grad_6': option_data.get('crdt_grad_6'),
                        'crdt_grad_avg': option_data.get('crdt_grad_avg'),
                        'fin_prdt_cd': product,
                    },
                )
            elif key == 'jeonse':
                JeonseOption.objects.update_or_create(
                    option_id=f"{option_data['fin_prdt_cd']}_{option_data['rpay_type']}_{option_data['lend_rate_type']}_opt",
                    defaults={
                        'dcls_month': parse_date(option_data.get('dcls_month')),
                        'rpay_type': option_data.get('rpay_type'),
                        'rpay_type_nm': option_data.get('rpay_type_nm'),
                        'lend_rate_type': option_data.get('lend_rate_type'),
                        'lend_rate_type_nm': option_data.get('lend_rate_type_nm'),
                        'lend_rate_min': option_data.get('lend_rate_min'),
                        'lend_rate_max': option_data.get('lend_rate_max'),
                        'lend_rate_avg': option_data.get('lend_rate_avg'),
                        'fin_prdt_cd': product,
                    },
                )
            elif key == 'mortgage':
                MortgageOption.objects.update_or_create(
                    option_id=f"{option_data['fin_prdt_cd']}_{option_data['rpay_type']}_{option_data['lend_rate_type']}_opt",
                    defaults={
                        'dcls_month': parse_date(option_data.get('dcls_month')),
                        'mrtg_type': option_data.get('mrtg_type'),
                        'mrtg_type_nm': option_data.get('mrtg_type_nm'),
                        'rpay_type': option_data.get('rpay_type'),
                        'rpay_type_nm': option_data.get('rpay_type_nm'),
                        'lend_rate_type': option_data.get('lend_rate_type'),
                        'lend_rate_type_nm': option_data.get('lend_rate_type_nm'),
                        'lend_rate_min': option_data.get('lend_rate_min'),
                        'lend_rate_max': option_data.get('lend_rate_max'),
                        'lend_rate_avg': option_data.get('lend_rate_avg'),
                        'fin_prdt_cd': product,
                    },
                )


class BankListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        banks = FinancialCompany.objects.all()
        serializer = FinancialCompanySerializer(banks, many=True)
        return Response(serializer.data)
