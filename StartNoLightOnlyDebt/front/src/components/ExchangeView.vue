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
    <div v-if="result !== null" class="result-container mt-4 text-center">
      <h2>환전 결과</h2>
      <p class="fw-bold">{{ amount }} {{ fromCurrency }} → {{ result.toFixed(2) }} {{ toCurrency }}</p>
      <button @click="resetCalculator" class="btn btn-outline-secondary mt-3">초기화</button>
    </div>
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

// 환율 계산 함수
const calculateExchange = () => {
  // 출발 통화의 매매 기준율
  const fromRate = parseFloat(rates.find((rate) => rate.cur_unit === fromCurrency.value)?.deal_bas_r || 1);

  // 도착 통화의 매매 기준율
  const toRate = parseFloat(rates.find((rate) => rate.cur_unit === toCurrency.value)?.deal_bas_r || 1);

  // 계산: (출발 통화 금액 × 출발 통화 환율) / 도착 통화 환율
  result.value = amount.value * (fromRate / toRate);
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
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 카드 스타일 */
.card {
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
</style>
