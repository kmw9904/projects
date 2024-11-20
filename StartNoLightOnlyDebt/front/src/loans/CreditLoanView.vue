<template>
  <div>
    <h2>신용 대출 상품 조회</h2>

    <!-- 검색 조건 입력 -->
    <form @submit.prevent="handleSearch">
      <label for="loanAmount">대출금액:</label>
      <input type="number" v-model.number="loanAmount" id="loanAmount" placeholder="대출금액 입력" />
      원
      <br />

      <label for="loanPeriod">대출기간:</label>
      <input type="number" v-model.number="loanPeriod" id="loanPeriod" placeholder="대출기간 입력" />
      년
      <br />

      <label for="loanType">대출 종류:</label>
      <select v-model="loanType" id="loanType">
        <option value="전체">전체</option>
        <option value="일반신용대출">일반신용대출</option>
        <option value="장기카드대출">장기카드대출</option>
      </select>
      <br />

      <button type="submit">검색</button>
    </form>

    <!-- 결과 출력 -->
    <CreditLoanDetailView v-if="products.length > 0" :products="products" :loanAmount="loanAmount" :loanPeriod="loanPeriod" />
    <p v-else>검색 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CreditLoanDetailView from "./CreditLoanDetailView.vue";
import axios from "axios";

// 검색 조건 상태
const loanAmount = ref(0);
const loanPeriod = ref(0);
const loanType = ref("전체");

// 결과 데이터
const products = ref([]);

// 검색 버튼 클릭 시 실행
const handleSearch = () => {
  if (loanAmount.value <= 0 || loanPeriod.value <= 0) {
    alert("대출금액과 대출기간을 올바르게 입력하세요.");
    return;
  }

  axios
    .get("http://127.0.0.1:8000/api/v1/credit-loans/", {
      params: {
        loan_amount: loanAmount.value,
        loan_period: loanPeriod.value,
      },
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`, // 인증 토큰 추가
      },
    })
    .then((response) => {
      const options = response.data;

      // products 데이터 재구성
      const groupedProducts = {};
      options.forEach((option) => {
        const productId = option.product.product_id;
        if (!groupedProducts[productId]) {
          groupedProducts[productId] = {
            product_id: productId,
            company_name: option.product.company_name || "금융 회사 정보 없음",
            product_name: option.product.product_name || "상품명 정보 없음",
            options: [],
          };
        }
        groupedProducts[productId].options.push(option);
      });

      // 결과를 배열로 변환
      products.value = Object.values(groupedProducts);

      if (products.value.length === 0) {
        alert("조건에 맞는 결과가 없습니다.");
      }
    })
    .catch((error) => {
      console.error("검색 중 오류:", error.response || error.message);
      alert("검색 중 문제가 발생했습니다. 다시 시도해주세요.");
    });
};
</script>
