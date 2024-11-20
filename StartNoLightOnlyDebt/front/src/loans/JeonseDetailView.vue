<template>
  <div>
    <h4>조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 렌더링 -->
    <div v-if="products.length > 0">
      <div v-for="product in products" :key="product.product_id">
        <p>
          <strong>금융 회사:</strong>
          {{ product.company_name }}
        </p>
        <p>
          <strong>상품명:</strong>
          {{ product.product_name }}
        </p>

        <!-- 옵션 리스트 출력 -->
        <div v-for="option in product.options" :key="option.option_id">
          <p>
            <strong>상환 방식:</strong>
            {{ option.rpay_type_nm || "정보 없음" }} |
            <strong>금리 유형:</strong>
            {{ option.lend_rate_type_nm || "정보 없음" }} |
            <strong>최저 금리:</strong>
            {{ option.lend_rate_min || "N/A" }} |
            <strong>최고 금리:</strong>
            {{ option.lend_rate_max || "N/A" }} |
            <strong>평균 금리:</strong>
            {{ option.lend_rate_avg || "N/A" }}
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
