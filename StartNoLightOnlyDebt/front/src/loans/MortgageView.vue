<template>
  <div>
    <!-- 네비게이션 버튼 -->
    <button @click="navigationStore.goHome">홈으로 가기</button>
    <button @click="navigationStore.goBack">뒤로 가기</button>

    <!-- 주택담보 대출 상품 조회 제목 -->
    <h2>주택담보 대출 상품 조회</h2>

    <!-- 조건 검색 폼 -->
    <form @submit.prevent="handleSearch">
      <label for="loanAmount">대출금액:</label>
      <input type="number" v-model.number="loanAmount" id="loanAmount" placeholder="대출금액 입력" />
      원
      <br />

      <label for="loanPeriod">대출기간:</label>
      <input type="number" v-model.number="loanPeriod" id="loanPeriod" placeholder="대출기간 입력" />
      년
      <br />

      <label for="repaymentType">상환 방식:</label>
      <select id="repaymentType" v-model="filters.repaymentType">
        <option value="전체">전체</option>
        <option value="고정금리">고정금리</option>
        <option value="변동금리">변동금리</option>
      </select>
      <br />
      <button type="submit">검색</button>
    </form>

    <MortgageDetailView v-if="filteredProducts.length > 0" :products="filteredProducts" :loanAmount="loanAmount" :loanPeriod="loanPeriod" />
    <p v-else>조건에 맞는 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useBankStore } from "@/stores/bank";
import { useNavigationStore } from "@/stores/navigation";
import MortgageDetailView from "./MortgageDetailView.vue";

// Stores 초기화
const store = useBankStore();
const navigationStore = useNavigationStore();

const loanAmount = ref(0); // 대출 금액
const loanPeriod = ref(0); // 대출 기간

// 필터링 조건
const filters = ref({
  repaymentType: "전체",
});

// 원본 데이터 상태
const products = ref([]);

// store.mortgages 데이터를 products로 반영
watch(
  () => store.mortgages,
  (newValue) => {
    if (newValue) {
      products.value = newValue; // 업데이트된 데이터를 products에 반영
      console.log("Updated Mortgage Products:", products.value);
    }
  }
);

// 특정 상품 ID로 옵션을 연결하고 상품과 함께 매핑
const mergedProducts = computed(() => {
  const groupedByProductId = products.value.reduce((acc, option) => {
    const product = option.product;
    const productId = product.product_id;

    if (!acc[productId]) {
      acc[productId] = {
        product_id: productId,
        product_name: product.product_name || "알 수 없음",
        company_name: product.company_name || "금융 회사 정보 없음",
        options: [],
      };
    }

    acc[productId].options.push(option);

    return acc;
  }, {});

  return Object.values(groupedByProductId);
});

// 필터링된 결과
const filteredProducts = computed(() => {
  if (filters.value.repaymentType === "전체") {
    return mergedProducts.value;
  }
  return mergedProducts.value.filter((product) => product.options.some((option) => option.rpay_type_nm?.includes(filters.value.repaymentType)));
});

// 검색 버튼 클릭 시 필터링 로직 실행
const handleSearch = () => {
  if (loanAmount.value <= 0 || loanPeriod.value <= 0) {
    alert("대출금액과 대출기간을 올바르게 입력하세요.");
    return;
  }

  store.getMortgage(); // 필요한 데이터 호출
};
</script>

<style scoped></style>
