<template>
  <div class="product-container">
    <h4 class="product-title text-center mb-4">조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 -->
    <div v-if="products.length > 0" class="product-list">
      <div v-for="product in products" :key="product.product_id" class="product-item card mb-4 shadow-sm">
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
          <div v-if="product.options.length > 0" class="option-list mt-3">
            <div v-for="option in product.options" :key="option.option_id" class="option-item">
              <p>
                <strong>금리 유형:</strong>
                {{ option.crdt_lend_rate_type_nm || "정보 없음" }}
              </p>
              <p>
                <strong>900점 초과:</strong>
                {{ option.crdt_grad_1 || "N/A" }} |
                <strong>801~900:</strong>
                {{ option.crdt_grad_4 || "N/A" }} |
                <strong>701~800:</strong>
                {{ option.crdt_grad_5 || "N/A" }} |
                <strong>601~700:</strong>
                {{ option.crdt_grad_6 || "N/A" }} |
                <strong>평균 금리:</strong>
                {{ option.crdt_grad_avg || "N/A" }}
              </p>
              <p>
                <strong>월 상환 금액:</strong>
                {{ option.monthlyPayment !== undefined ? `${formatCurrency(option.monthlyPayment)}원` : "계산 중..." }}
              </p>
              <!-- 댓글 및 좋아요 컴포넌트 -->
              <CreditLoanDiscussionView :productId="product.product_id" :productName="product.product_name" :optionType="'credit'" />
            </div>
          </div>
          <div v-else>
            <p class="text-muted">옵션이 없습니다.</p>
          </div>
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
import { defineProps, onMounted, ref } from "vue";
import axios from "axios";
import CreditLoanDiscussionView from "./CreditLoanDiscussionView.vue";

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
    url: `http://127.0.0.1:8000/api/v1/calculate/credit/${option.option_id}/`,
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
        option.monthlyPayment = calculation ? calculation.monthly_payment : null;
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
1
// 컴포넌트가 로드될 때 자동으로 계산
onMounted(() => {
  calculateAllPayments();
});
</script>

<style scoped>
.product-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.product-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.product-list {
  margin-top: 15px;
}

.product-item {
  background: #ffffff;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid #eaeaea;
  border-radius: 5px;
}

.bank-img {
  width: 690px; /* 이미지 컨테이너의 너비 */
  height: auto;
  flex-shrink: 0; /* 크기를 줄이지 않음 */
}

.bank-img img {
  width: 100%; /* 컨테이너 너비에 맞게 이미지 조정 */
  height: 200px; /* 비율 유지 */
  object-fit: contain; /* 이미지가 비율에 맞게 축소되며 잘리지 않음 */
  border-radius: 5px; /* 이미지 둥근 테두리 */
  border: 1px solid #eaeaea; /* 이미지 테두리 */
}

.option-list {
  margin-top: 15px;
}

.option-item {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}
.product-list {
  margin-top: 15px;
}

.product-item {
  background: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 15px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #007bff;
}

.option-list {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 5px;
  border: 1px solid #e9ecef;
}

.option-item {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #eaeaea;
  border-radius: 5px;
  background: #ffffff;
}

.text-muted {
  font-size: 0.9rem;
  color: #6c757d;
}

.bank-img {
  width: 660px; /* 이미지 컨테이너의 너비 */
  height: auto;
  flex-shrink: 0; /* 크기를 줄이지 않음 */
}

.bank-img img {
  width: 100%; /* 컨테이너 너비에 맞게 이미지 조정 */
  height: 200px; /* 비율 유지 */
  object-fit: contain; /* 이미지가 비율에 맞게 축소되며 잘리지 않음 */
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
}
</style>
