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
      원
      <br />

      <label for="loanPeriod">대출기간:</label>
      <input type="number" id="loanPeriod" v-model="filters.loanPeriod" />
      년
      <br />

      <label for="loanType">대출 종류:</label>
      <select id="loanType" v-model="filters.loanType">
        <option value="전체">전체</option>
        <option value="일반신용대출">일반신용대출</option>
        <option value="장기카드대출">장기카드대출</option>
      </select>
      <br />

      <button type="submit" :disabled="!isValidInput">검색</button>
    </form>

    <!-- 결과 출력 -->
    <CreditLoanDetailView :products="filteredProducts" :loanAmount="filters.loanAmount" :loanPeriod="filters.loanPeriod" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useBankStore } from "@/stores/bank";
import { useNavigationStore } from "@/stores/navigation";
import CreditLoanDetailView from "./CreditLoanDetailView.vue";

// NavigationStore 초기화
const navigationStore = useNavigationStore();

// BankStore 초기화
const store = useBankStore();

// 필터링 조건
const filters = ref({
  loanAmount: 0, // 초기값 설정
  loanPeriod: 0, // 초기값 설정
  loanType: "전체",
});

// 입력값 유효성 검사
const isValidInput = computed(() => filters.value.loanAmount > 0 && filters.value.loanPeriod > 0);

// 원본 데이터 상태
const products = ref([]);

// 옵션 매핑
const mergedProducts = computed(() => {
  const groupedByProductId = products.value.reduce((acc, option) => {
    const product = option.product;
    const productId = product.product_id;

    if (!acc[productId]) {
      acc[productId] = {
        product_id: productId,
        product_name: product.product_name || "알 수 없음",
        company_name: product.company_name || "금융 회사 정보 없음",
        options: [], // 옵션 리스트 초기화
      };
    }

    // 옵션 추가
    acc[productId].options.push(option);

    return acc;
  }, {});

  return Object.values(groupedByProductId);
});

// 필터링된 결과
const filteredProducts = computed(() => {
  if (filters.value.loanType === "전체") {
    return mergedProducts.value;
  }
  return mergedProducts.value.filter((product) => product.product_name.includes(filters.value.loanType));
});

// 검색 버튼 클릭 시 필터링 로직 실행
const handleSearch = () => {
  console.log("검색 조건:", filters.value);
};

// store.creditLoans를 products에 반영
watch(
  () => store.creditLoans,
  (newValue) => {
    if (newValue) {
      products.value = newValue;
      console.log("Updated Products:", products.value);
    }
  }
);

// 컴포넌트 마운트 시 API 호출
onMounted(() => {
  store.getCreditLoan();
});
</script>

<style scoped></style>
