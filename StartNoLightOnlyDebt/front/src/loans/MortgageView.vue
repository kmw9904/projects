<template>
  <div>
    <!-- 네비게이션 버튼 -->
    <button @click="navigationStore.goHome">홈으로 가기</button>
    <button @click="navigationStore.goBack">뒤로 가기</button>

    <!-- 주택담보 대출 상품 조회 제목 -->
    <h2>주택담보 대출 상품 조회</h2>

    <!-- 조건 검색 폼 -->
    <form @submit.prevent="handleSearch">
      <label for="repaymentType">상환 방식:</label>
      <select id="repaymentType" v-model="filters.repaymentType">
        <option value="전체">전체</option>
        <option value="고정금리">고정금리</option>
        <option value="변동금리">변동금리</option>
      </select>
      <br />
      <button type="submit">검색</button>
    </form>

    <h4>조건에 맞는 금융 조건</h4>

    <!-- 데이터가 로드된 경우 렌더링 -->
    <div v-if="filteredProducts.length > 0">
      <div v-for="product in filteredProducts" :key="product.product_id">
        <p><strong>금융 회사:</strong> {{ product.company_name }}</p>
        <p><strong>상품명:</strong> {{ product.product_name }}</p>

        <!-- 옵션 리스트 출력 -->
        <div v-for="option in product.options" :key="option.option_id">
          <p>
            <strong>담보 유형:</strong> {{ option.mrtg_type_nm || "정보 없음" }} |
            <strong>상환 방식:</strong> {{ option.rpay_type_nm || "정보 없음" }} |
            <strong>금리 유형:</strong> {{ option.lend_rate_type_nm || "정보 없음" }} |
            <strong>최저 금리:</strong> {{ option.lend_rate_min || "N/A" }} |
            <strong>최고 금리:</strong> {{ option.lend_rate_max || "N/A" }} |
            <strong>평균 금리:</strong> {{ option.lend_rate_avg || "N/A" }}
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
import { ref, computed, onMounted, watch } from "vue";
import { useBankStore } from "@/stores/bank";
import { useNavigationStore } from "@/stores/navigation";

// Stores 초기화
const store = useBankStore();
const navigationStore = useNavigationStore();

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
      console.log("Updated Products:", products.value);
    }
  }
);

// 특정 상품 ID로 옵션을 연결하고 상품과 함께 매핑
const mergedProducts = computed(() => {
  // product_id 기준으로 옵션을 그룹화
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
  return mergedProducts.value.filter((product) =>
    product.options.some((option) =>
      option.rpay_type_nm?.includes(filters.value.repaymentType)
    )
  );
});

// 검색 버튼 클릭 시 필터링 로직 실행
const handleSearch = () => {
  console.log("검색 조건:", filters.value);
};

// 컴포넌트 마운트 시 API 호출
onMounted(() => {
  store.getMortgage();
});
</script>

<style scoped></style>
