<template>
  <div>
    <h4>조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 렌더링 -->
    <div v-if="products.length > 0">
      <div v-for="product in products" :key="product.fin_prdt_cd">
        <p>
          <strong>금융 회사:</strong>
          {{ product.kor_co_nm }}
        </p>
        <p>
          <strong>상품명:</strong>
          {{ product.fin_prdt_nm }}
        </p>
        <p>
          <strong>대출 종류:</strong>
          {{ product.crdt_prdt_type_nm }}
        </p>

        <!-- 옵션 리스트 출력 -->
        <div v-for="option in product.options" :key="option.crdt_lend_rate_type">
          <p>
            <strong>금리 유형:</strong>
            {{ option.crdt_lend_rate_type_nm }} |
            <strong>900점 초과:</strong>
            {{ option.crdt_grad_1 }} |
            <strong>801~900:</strong>
            {{ option.crdt_grad_4 }} |
            <strong>701~800:</strong>
            {{ option.crdt_grad_5 }} |
            <strong>601~700:</strong>
            {{ option.crdt_grad_6 }} |
            <strong>평균 금리:</strong>
            {{ option.crdt_grad_avg }}
          </p>
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
import { defineProps } from "vue";

// 부모 컴포넌트에서 전달받은 props
const props = defineProps({
  products: Array, // 필터링된 상품 목록
});
</script>

<style scoped></style>
