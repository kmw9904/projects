<template>
  <div class="mortgage-conditions-container">
    <h4 class="mortgage-title text-center mb-4">조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 -->
    <div v-if="products.length > 0" class="products-list">
      <div v-for="product in products" :key="product.product_id" class="product-item card mb-3 shadow-sm">
        <div class="card-body">
          <p class="card-title">
            <div class="bank-img">
              <img :src="`/pictures/${product.company_name}.png`" alt="금융 회사 로고" />
            </div>
            <strong>금융 회사:</strong>
            {{ product.company_name || "금융 회사 정보 없음" }}
          </p>
          <p>
            <strong>상품명:</strong>
            {{ product.product_name || "상품명 정보 없음" }}
          </p>

          <!-- 옵션 리스트 -->
          <div v-if="product.options.length > 0" class="options-list mt-3">
            <div v-for="option in product.options" :key="option.option_id" class="option-item p-3">
              <p>
                <strong>상환 방식:</strong>
                {{ option.rpay_type_nm || "정보 없음" }} |
                <strong>금리 유형:</strong>
                {{ option.lend_rate_type_nm || "정보 없음" }} |
                <strong>최저 금리:</strong>
                {{ option.lend_rate_min || "N/A" }} |
                <strong>평균 금리:</strong>
                {{ option.lend_rate_avg || "N/A" }} |
                <strong>최고 금리:</strong>
                {{ option.lend_rate_max || "N/A" }}
              </p>
              <p>
                <strong>최저 상환 금액:</strong>
                {{ option.minPayment !== undefined ? `${formatCurrency(option.minPayment)}원` : "계산 중..." }}
              </p>
              <p>
                <strong>평균 상환 금액:</strong>
                {{ option.avgPayment !== undefined ? `${formatCurrency(option.avgPayment)}원` : "계산 중..." }}
              </p>
              <p>
                <strong>최고 상환 금액:</strong>
                {{ option.maxPayment !== undefined ? `${formatCurrency(option.maxPayment)}원` : "계산 중..." }}
              </p>
              <RouterLink :to="{ name: 'FinancialProductDetail', params: { productId: product.options[0].product.product_id } }" class="btn btn-primary">상세 정보 보기</RouterLink>
              <MortgageDiscussionView :productId="product.product_id" :productName="product.product_name" />
            </div>
          </div>
          <div v-else class="text-muted">옵션이 없습니다.</div>
        </div>
      </div>
    </div>

    <!-- 데이터가 없을 경우 -->
    <div v-else class="text-center text-muted">
      <p>조건에 맞는 결과가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { defineProps, onMounted, ref } from "vue";
import axios from "axios";
import MortgageDiscussionView from "./MortgageDiscussionView.vue";

// 부모 컴포넌트에서 전달받은 props
const props = defineProps({
  products: Array, // 필터링된 상품 목록
  loanAmount: Number, // 대출 금액
  loanPeriod: Number, // 대출 기간 (연 단위)
});

// 숫자 포맷팅 함수
const formatCurrency = (value) => {
  if (typeof value !== "number") return value;
  return new Intl.NumberFormat("ko-KR", {
    style: "decimal",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

// 월 상환 금액 계산 API 호출
const calculateMonthlyPayment = (option) => {
  return axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1/calculate/mortgage/${option.option_id}/`,
    params: {
      loan_amount: props.loanAmount,
      years: props.loanPeriod,
    },
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  })
    .then((response) => {
      if (response.data.calculations && response.data.calculations.length > 0) {
        const calculation = response.data.calculations.find((calc) => calc.option_id === option.option_id);
        if (calculation) {
          option.minPayment = calculation.monthly_payment_min || null;
          option.avgPayment = calculation.monthly_payment_avg || null;
          option.maxPayment = calculation.monthly_payment_max || null;
        }
      } else {
        console.warn("월 상환 금액 데이터가 없습니다.");
      }
    })
    .catch((error) => {
      console.error("월 상환 금액 계산 중 오류:", error.response || error.message);
    });
};

// 모든 옵션에 대해 월 상환 금액 계산
const calculateAllPayments = () => {
  props.products.forEach((product) => {
    product.options.forEach((option) => {
      calculateMonthlyPayment(option);
    });
  });
};

// 컴포넌트가 로드될 때 자동으로 계산
onMounted(() => {
  calculateAllPayments();
});
</script>

<style scoped>
.mortgage-conditions-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  max-width: 800px;
}

.mortgage-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: gray;
}

.products-list .product-item {
  background: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px; /* 카드 간격 추가 */
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #007bff;
}

.options-list {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.option-item {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}

.text-muted {
  font-size: 0.9rem;
  color: #6c757d;
}

.bank-img {
  width: 100%; /* 부모 컨테이너에 맞게 조정 */
  max-width: 660px; /* 최대 너비 제한 */
  height: 200px; /* 고정 높이 */
  margin-bottom: 10px; /* 이미지와 텍스트 사이 간격 */
}

.bank-img img {
  width: 100%; /* 컨테이너 너비에 맞게 이미지 조정 */
  height: 100%; /* 고정 높이에 맞게 이미지 조정 */
  object-fit: contain; /* 이미지가 비율에 맞게 축소되며 잘리지 않음 */
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
}
</style>


