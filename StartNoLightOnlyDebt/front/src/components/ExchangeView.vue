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
        <input type="number" id="amount" v-model.number="amount" class="form-control" placeholder="금액을 입력하세요" />
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
  // 출발 통화의 매매 기준율 (숫자로 변환)
  const fromRate = parseFloat(rates.find((rate) => rate.cur_unit === fromCurrency.value)?.deal_bas_r || 1);

  // 도착 통화의 매매 기준율 (숫자로 변환)
  const toRate = parseFloat(rates.find((rate) => rate.cur_unit === toCurrency.value)?.deal_bas_r || 1);

  // 올바른 환율 계산 로직: 모든 경우에 동일한 방식으로 계산
  result.value = amount.value * (fromRate / toRate);
};
</script>

<style scoped>
.exchange-calculator {
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
}

.result-container {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
