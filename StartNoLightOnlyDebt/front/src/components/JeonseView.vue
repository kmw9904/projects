<template>
  <div>
    <!-- 네비게이션 버튼 -->
    <button @click="navigationStore.goHome">홈으로 가기</button>
    <button @click="navigationStore.goBack">뒤로 가기</button>

    <!-- 전세 대출 상품 조회 제목 -->
    <h2>전세 자금 대출 상품 조회</h2>
    <h4>조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 렌더링 -->
    <div v-if="mergedProducts.length > 0">
      <!-- 금융회사 및 상품 정보와 옵션 -->
      <div v-for="product in mergedProducts" :key="product.fin_prdt_cd">
        <p>금융 회사 : {{ product.kor_co_nm }}</p>
        <p>상품명 : {{ product.fin_prdt_nm }}</p>
        <p v-for="option in product.options" :key="option.fin_prdt_cd">
          <strong>상환 방식:</strong>
          {{ option.rpay_type_nm }} |
          <strong>금리 유형:</strong>
          {{ option.lend_rate_type_nm }} |
          <strong>최저 금리:</strong>
          {{ option.lend_rate_min }} |
          <strong>최고 금리:</strong>
          {{ option.lend_rate_max }} |
          <strong>평균 금리:</strong>
          {{ option.lend_rate_avg }}
          <RouterLink :to="{name : CalculatorView}"></RouterLink>
        </p>
        <hr />
      </div>
    </div>

    <!-- 데이터 로딩 중 표시 -->
    <div v-else>
      <p>데이터를 받아오는 중....</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, ref, computed } from "vue";
import { useBankStore } from "@/stores/bank";
import { useNavigationStore } from "@/stores/navigation";
import CalculatorView from "./CalculatorView.vue";

// BankStore 및 NavigationStore 초기화
const store = useBankStore();
const navigationStore = useNavigationStore();

// 데이터 상태 초기화
const products = ref({
  jeonse: {
    result: {
      baseList: [], // 금융회사와 상품 정보 목록
      optionList: [], // 옵션 목록
    },
  },
});

// 특정 상품 ID로 옵션을 연결하고 상품과 함께 매핑
const mergedProducts = computed(() => {
  const baseList = products.value.jeonse.result.baseList || [];
  const optionList = products.value.jeonse.result.optionList || [];

  // baseList와 optionList를 fin_prdt_cd 기준으로 매핑
  return baseList.map((base) => {
    const options = optionList.filter((option) => option.fin_prdt_cd === base.fin_prdt_cd);
    return { ...base, options };
  });
});

// 컴포넌트 마운트 시 API 호출
// 전세 대출 데이터를 가져오기 위해 store의 getJeonse 메서드 호출
onMounted(() => {
  store.getJeonse();
});

// store.jeonses가 업데이트되면 products.value에 데이터를 반영
watch(
  () => store.jeonses, // 감시 대상
  (newValue) => {
    if (newValue) {
      products.value = newValue; // 업데이트된 데이터를 products에 반영
      console.log(products.value); // 디버깅을 위해 데이터 출력
    }
  }
);
</script>

<style scoped></style>
