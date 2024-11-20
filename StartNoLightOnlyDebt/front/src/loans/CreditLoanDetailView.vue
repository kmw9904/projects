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
              <strong>금리 유형:</strong>
              {{ option.crdt_lend_rate_type_nm || "정보 없음" }} |
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
import { defineProps } from "vue";

// 부모 컴포넌트에서 전달받은 props
const props = defineProps({
  products: Array, // 필터링된 상품 목록
});
</script>

<style scoped></style>
