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

      <!-- 최저 상환 금액 기준 정렬 체크박스 -->
      <label>
        <input type="checkbox" v-model="sortByMinPayment" />
        최저 상환 금액 기준 정렬
      </label>
      <br />

      <!-- 선호 은행만 보기 체크박스 -->
      <label>
        <input type="checkbox" v-model="filterByPreferredBanks" />
        선호 은행만 보기
      </label>
      <br />

      <button type="submit">검색</button>
    </form>

    <MortgageDetailView v-if="sortedProducts.length > 0" :products="sortedProducts" :loanAmount="loanAmount" :loanPeriod="loanPeriod" />
    <p v-else>조건에 맞는 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useBankStore } from "@/stores/bank";
import { useNavigationStore } from "@/stores/navigation";
import MortgageDetailView from "./MortgageDetailView.vue";
import axios from "axios";

// Stores 초기화
const store = useBankStore();
const navigationStore = useNavigationStore();

const API_URL = "http://127.0.0.1:8000";

const loanAmount = ref(0); // 대출 금액
const loanPeriod = ref(0); // 대출 기간
const sortByMinPayment = ref(false); // 최저 상환 금액 기준 정렬 여부
const filterByPreferredBanks = ref(false); // 선호 은행 필터링 여부

// 선호 은행 데이터
const preferredBanks = ref([]);

// 선호 은행 가져오기
const getPreferredBanks = () => {
  return axios({
    method: "get",
    url: `${API_URL}/accounts/preferred-banks/`,
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  })
    .then((res) => {
      preferredBanks.value = res.data.banks.filter((bank) => bank.is_preferred).map((bank) => bank.company_name);
    })
    .catch((err) => {
      console.error("선호 은행 데이터 가져오기 실패:", err.response?.data || err.message);
    });
};

// 필터링 조건
const filters = ref({
  repaymentType: "전체", // 상환 방식 (전체, 고정금리, 변동금리)
});

// 원본 데이터 상태
const products = ref([]);

// store.mortgages 데이터를 products로 반영
watch(
  () => store.mortgages,
  (newValue) => {
    if (newValue) {
      products.value = newValue; // 업데이트된 데이터를 products에 반영
      console.log(products.value);
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
  let result = mergedProducts.value;

  // 상환 방식(금리 유형) 필터링
  if (filters.value.repaymentType !== "전체") {
    result = result
      .map((product) => {
        // 조건에 맞는 옵션만 필터링
        const filteredOptions = product.options.filter((option) => {
          const lendRateType = (option.lend_rate_type_nm || "").trim().toLowerCase();
          const repaymentType = filters.value.repaymentType.trim().toLowerCase();
          return lendRateType === repaymentType;
        });

        // 옵션이 존재하면 상품을 반환
        if (filteredOptions.length > 0) {
          return {
            ...product,
            options: filteredOptions, // 조건에 맞는 옵션만 포함
          };
        }
        return null; // 조건에 맞는 옵션이 없으면 상품 제외
      })
      .filter((product) => product !== null); // null 값을 제거
  }

  // 선호 은행 필터링
  if (filterByPreferredBanks.value) {
    result = result.filter((product) => preferredBanks.value.includes(product.company_name));
  }

  console.log("Filtered products before returning:", result);

  return result;
});
// 최저 상환 금액 기준 정렬
const sortedProducts = computed(() => {
  if (!sortByMinPayment.value) {
    return filteredProducts.value;
  }

  return filteredProducts.value
    .map((product) => {
      const sortedOptions = [...product.options].sort((a, b) => {
        const aPayment = a.avgPayment || Infinity;
        const bPayment = b.avgPayment || Infinity;
        return aPayment - bPayment;
      });
      return { ...product, options: sortedOptions };
    })
    .sort((a, b) => {
      const aMin = a.options[0]?.avgPayment || Infinity;
      const bMin = b.options[0]?.avgPayment || Infinity;
      return aMin - bMin;
    });
});

// 검색 버튼 클릭 시 필터링 로직 실행
const handleSearch = () => {
  if (loanAmount.value <= 0 || loanPeriod.value <= 0) {
    alert("대출금액과 대출기간을 올바르게 입력하세요.");
    return;
  }

  store.getMortgage(); // 필요한 데이터 호출
};

// 초기화
onMounted(() => {
  getPreferredBanks();
});
</script>

<style scoped></style>
