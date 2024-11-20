<template>
  <div>
    <h4>조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 렌더링 -->
    <div v-if="products.length > 0">
      <div v-for="product in products" :key="product.product_id">
        <p>
          <strong>금융 회사:</strong>
          {{ product.company_name || "금융 회사 정보 없음" }}
        </p>
        <p>
          <strong>상품명:</strong>
          {{ product.product_name || "상품명 정보 없음" }}
        </p>

        <!-- 옵션 리스트 출력 -->
        <div v-if="product.options.length > 0">
          <div v-for="option in product.options" :key="option.option_id">
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

            <JeonseDiscussionView />
          </div>
        </div>
        <div v-else>
          <p>옵션이 없습니다.</p>
        </div>

        <hr />
      </div>
    </div>

    <!-- 데이터가 없을 경우 -->
    <div v-else>
      <p>조건에 맞는 결과가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, onMounted } from "vue";
import axios from "axios";
import JeonseDiscussionView from "./JeonseDiscussionView.vue";

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
    url: `http://127.0.0.1:8000/api/v1/calculate/jeonse/${option.option_id}/`,
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
/* 스타일 없음 */
</style>
