<template>
  <div class="exchange-calculator">
    <h1 class="text-center mb-4">환율 계산기</h1>
    <div class="card p-4 shadow-sm">
      <!-- 출발 통화 선택 -->
      <div class="form-group mb-3">
        <label for="fromCurrency" class="form-label">출발 통화:</label>
        <select v-model="fromCurrency" id="fromCurrency" class="form-select">
          <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">{{ rate.cur_unit }} ({{ rate.cur_nm }})</option>
        </select>
      </div>

      <!-- 도착 통화 선택 -->
      <div class="form-group mb-3">
        <label for="toCurrency" class="form-label">도착 통화:</label>
        <select v-model="toCurrency" id="toCurrency" class="form-select">
          <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">{{ rate.cur_unit }} ({{ rate.cur_nm }})</option>
        </select>
      </div>

      <!-- 환전 금액 입력 -->
      <div class="form-group mb-3">
        <label for="amount" class="form-label">환전 금액:</label>
        <input type="number" id="amount" v-model.number="amount" class="form-control" placeholder="금액을 입력하세요" @input="preventNegativeInput" />
      </div>

      <!-- 계산 버튼 -->
      <div class="text-center">
        <button @click="calculateExchange" class="btn btn-secondary w-100">환율 계산</button>
      </div>
    </div>

    <!-- 계산 결과 -->
    <div v-if="lastResult !== null" class="result-container mt-4 text-center">
      <h2>환전 결과</h2>
      <p class="fw-bold">{{ lastAmount }} {{ lastFromCurrency }} → {{ lastResult.toFixed(2) }} {{ lastToCurrency }}</p>
      <button @click="resetCalculator" class="btn btn-outline-secondary mt-3">초기화</button>
    </div>
    <!-- 푸터 -->
    <footer class="footer">
      <div class="container">
        <p>© 2024 Start No Light Only Debt. All rights reserved.</p>
        <p>어려운 대출 정보를 모두가 손쉽고 편리하게 대출 정보를 받을 수 있도록 우리 프로그램은 계속 노력합니다.</p>
        <p>
          Contact us:
          <a href="mailto:support@example.com">kms990415@naver.com</a>
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { rates } from "@/stores/rates.js"; // 환율 데이터 가져오기

// 상태 관리
const fromCurrency = ref("KRW"); // 기본값: 원화
const toCurrency = ref("USD"); // 기본값: 미국 달러
const amount = ref(0); // 입력 금액
const result = ref(null); // 계산 결과
const lastResult = ref(null); // 최종 결과
const lastFromCurrency = ref(""); // 마지막 출발 통화
const lastToCurrency = ref(""); // 마지막 도착 통화
const lastAmount = ref(0); // 마지막 입력 금액

// 환율 계산 함수
const calculateExchange = () => {
  // 출발 통화의 매매 기준율
  const fromRate = parseFloat(rates.find((rate) => rate.cur_unit === fromCurrency.value)?.deal_bas_r || 1);

  // 도착 통화의 매매 기준율
  const toRate = parseFloat(rates.find((rate) => rate.cur_unit === toCurrency.value)?.deal_bas_r || 1);

  // 계산: (출발 통화 금액 × 출발 통화 환율) / 도착 통화 환율
  result.value = amount.value * (fromRate / toRate);

  // 결과를 최종 변수에 저장하여 이후 변경에도 유지
  lastResult.value = result.value;
  lastFromCurrency.value = fromCurrency.value;
  lastToCurrency.value = toCurrency.value;
  lastAmount.value = amount.value;
};

// 음수 입력 방지
const preventNegativeInput = () => {
  if (amount.value < 0) {
    amount.value = 0; // 음수 입력 시 0으로 고정
  }
};

// 초기화 함수
const resetCalculator = () => {
  fromCurrency.value = "KRW";
  toCurrency.value = "USD";
  amount.value = 0;
  result.value = null; // 결과 초기화
  lastResult.value = null; // 최종 결과 초기화
  lastFromCurrency.value = "";
  lastToCurrency.value = "";
  lastAmount.value = 0;
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.exchange-calculator {
  padding: 30px;
  max-width: 500px;
  margin: 0 auto;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
h1 {
  font-family: "Noto Sans KR", sans-serif;
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 카드 스타일 */
.card {
  font-family: "Noto Sans KR", sans-serif;
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

/* 결과 컨테이너 스타일 */
.result-container {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 25px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 */
}

.btn-outline-secondary {
  color: #6c757d;
  border: 1px solid #6c757d;
  background-color: transparent;
  padding: 8px 16px;
  font-size: 0.95rem;
  border-radius: 25px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 푸터 스타일 */
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #f8f9fa; /* 밝은 회색 배경 */
  text-align: center;
  padding: 10px 0;
  font-size: 14px;
  color: #333; /* 텍스트 색상 */
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* 상단 그림자 */
  border-top: 1px solid #ddd; /* 상단 테두리 */
}

.footer a {
  color: #007bff; /* 링크 색상 */
  text-decoration: none; /* 밑줄 제거 */
}

.footer a:hover {
  text-decoration: underline; /* 링크 호버 시 밑줄 */
  color: #0056b3; /* 링크 호버 시 색상 */
}
</style>
