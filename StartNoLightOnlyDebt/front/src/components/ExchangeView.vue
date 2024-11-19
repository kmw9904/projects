<template>
  <div>
    <h1>환율 계산기</h1>
    <div>
      <!-- 출발 통화 선택 -->
      <label>출발 통화:</label>
      <select v-model="fromCurrency">
        <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">{{ rate.cur_unit }} ({{ rate.cur_nm }})</option>
      </select>
    </div>
    <div>
      <!-- 도착 통화 선택 -->
      <label>도착 통화:</label>
      <select v-model="toCurrency">
        <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">{{ rate.cur_unit }} ({{ rate.cur_nm }})</option>
      </select>
    </div>
    <div>
      <!-- 환전 금액 입력 -->
      <label>환전 금액:</label>
      <input type="number" v-model.number="amount" placeholder="금액을 입력하세요" />
    </div>
    <button @click="calculateExchange">환율 계산</button>

    <!-- 계산 결과 -->
    <div v-if="result !== null">
      <h2>환전 결과</h2>
      <p>{{ amount }} {{ fromCurrency }} → {{ result.toFixed(2) }} {{ toCurrency }}</p>
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
h1 {
  text-align: center;
  margin-bottom: 20px;
}
div {
  margin: 10px 0;
}
select,
input {
  margin-left: 10px;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
