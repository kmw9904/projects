<template>
  <div>
    <!-- 네비게이션 버튼 -->
    <button @click="navigationStore.goHome">홈으로 가기</button>
    <button @click="navigationStore.goBack">뒤로 가기</button>

    <!-- 신용 대출 상품 조회 제목 -->
    <h2>신용 대출 상품 조회</h2>

    <!-- 조건 검색 폼 -->
    <form @submit.prevent="handleSearch">
      <label for="loanAmount">대출금액:</label>
      <input type="number" id="loanAmount" v-model="filters.loanAmount" />
      <br />

      <label for="loanPeriod">대출기간:</label>
      <input type="number" id="loanPeriod" v-model="filters.loanPeriod" />
      <br />

      <label for="loanType">대출 종류:</label>
      <select id="loanType" v-model="filters.loanType">
        <option value="전체">전체</option>
        <option value="일반신용대출">일반신용대출</option>
        <option value="장기카드대출">장기카드대출</option>
      </select>
      <br />

      <button type="submit">검색</button>
    </form>

    <!-- 결과 출력 -->
    <CreditLoanDetailView :products="filteredProducts" />
  </div>
</template>

<script setup>
import { onMounted, watch, ref, computed } from "vue";
import { useBankStore } from "@/stores/bank";
import { useNavigationStore } from "@/stores/navigation";
import CreditLoanDetailView from "./CreditLoanDetailView.vue";

// NavigationStore 초기화
const navigationStore = useNavigationStore();

// BankStore 초기화
const store = useBankStore();

// 필터링 조건
const filters = ref({
  loanAmount: null,
  loanPeriod: null,
  loanType: "전체",
});

// 원본 데이터 상태
const products = ref({
  credit: {
    result: {
      baseList: [], // 금융회사와 상품 정보 목록
      optionList: [], // 옵션 목록
    },
  },
});

// 특정 상품 ID로 옵션을 연결하고 상품과 함께 매핑
const mergedProducts = computed(() => {
  const baseList = products.value.credit.result.baseList || [];
  const optionList = products.value.credit.result.optionList || [];

  // baseList와 optionList를 매핑하여 옵션 추가
  return baseList.map((base) => {
    const options = optionList.filter((option) => option.fin_prdt_cd === base.fin_prdt_cd && option.crdt_prdt_type === base.crdt_prdt_type);

    // 중복 제거
    const uniqueOptions = Array.from(new Map(options.map((opt) => [opt.crdt_lend_rate_type, opt])).values());

    return { ...base, options: uniqueOptions };
  });
});

// 필터링된 결과
const filteredProducts = computed(() => {
  // "전체" 선택 시 필터링 없이 모든 데이터 반환
  if (filters.value.loanType === "전체") {
    return mergedProducts.value;
  }

  // 필터 조건: 대출 종류 포함 여부 확인
  return mergedProducts.value.filter((product) => product.fin_prdt_nm.includes(filters.value.loanType) || product.crdt_prdt_type_nm.includes(filters.value.loanType));
});

// 검색 버튼 클릭 시 필터링 로직 실행
const handleSearch = () => {
  console.log("검색 조건:", filters.value);
};

// 컴포넌트 마운트 시 API 호출
onMounted(() => {
  store.getCreditLoan();
});

// store.creditLoans가 업데이트되면 products.value에 데이터를 반영
watch(
  () => store.creditLoans,
  (newValue) => {
    if (newValue) {
      products.value = newValue; // 업데이트된 데이터를 products에 반영
      console.log("Updated Products:", products.value); // 디버깅
    }
  }
);
</script>

<style scoped></style>
