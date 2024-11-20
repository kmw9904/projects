<template>
  <div>
    <h2>신용 대출 상품 조회</h2>

    <!-- 검색 조건 입력 -->
    <form @submit.prevent="handleSearch">
      <label for="loanAmount">대출금액:</label>
      <input type="number" v-model.number="loanAmount" id="loanAmount" placeholder="대출금액 입력" />
      원
      <br />

      <label for="loanPeriod">대출기간:</label>
      <input type="number" v-model.number="loanPeriod" id="loanPeriod" placeholder="대출기간 입력" />
      년
      <br />

      <label for="loanType">대출 종류:</label>
      <select v-model="loanType" id="loanType">
        <option value="전체">전체</option>
        <option value="일반신용대출">일반신용대출</option>
        <option value="장기카드대출">장기카드대출</option>
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
        <input type="checkbox" v-model="showPreferredBanksOnly" />
        선호 은행만 보기
      </label>
      <br />

      <button type="submit">검색</button>
    </form>

    <!-- 결과 출력 -->
    <CreditLoanDetailView v-if="sortedAndFilteredProducts.length > 0" :products="sortedAndFilteredProducts" :loanAmount="loanAmount" :loanPeriod="loanPeriod" />
    <p v-else>검색 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import CreditLoanDetailView from "./CreditLoanDetailView.vue";
import axios from "axios";

// API URL 설정
const API_URL = "http://127.0.0.1:8000/api/v1";

// 검색 조건 상태
const loanAmount = ref(0);
const loanPeriod = ref(0);
const loanType = ref("전체");
const sortByMinPayment = ref(false); // 최저 상환 금액 정렬 여부
const showPreferredBanksOnly = ref(false); // 선호 은행 필터링 여부

// 결과 데이터
const products = ref([]);
const preferredBanks = ref([]); // 선호 은행 ID 리스트

// 사용자 선호 은행 가져오기
const getPreferredBanks = function () {
  return axios({
    method: "get",
    url: `${API_URL}/accounts/preferred-banks/`,
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  })
    .then((res) => {
      console.log("선호 은행 목록 가져오기 성공:", res.data);
      preferredBanks.value = res.data; // 선호 은행 ID 리스트 저장
    })
    .catch((err) => {
      console.error("선호 은행 목록 가져오기 실패:", err.response?.data || err.message);
      alert("선호 은행 데이터를 가져오지 못했습니다.");
    });
};

// 검색 버튼 클릭 시 실행
const handleSearch = () => {
  if (loanAmount.value <= 0 || loanPeriod.value <= 0) {
    alert("대출금액과 대출기간을 올바르게 입력하세요.");
    return;
  }

  axios
    .get(`${API_URL}/credit-loans/`, {
      params: {
        loan_amount: loanAmount.value,
        loan_period: loanPeriod.value,
      },
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      const options = response.data;

      // products 데이터 재구성
      const groupedProducts = {};
      options.forEach((option) => {
        const productId = option.product.product_id;
        if (!groupedProducts[productId]) {
          groupedProducts[productId] = {
            product_id: productId,
            company_name: option.product.company_name || "금융 회사 정보 없음",
            product_name: option.product.product_name || "상품명 정보 없음",
            options: [],
          };
        }
        groupedProducts[productId].options.push(option);
      });

      // 결과를 배열로 변환
      products.value = Object.values(groupedProducts);

      if (products.value.length === 0) {
        alert("조건에 맞는 결과가 없습니다.");
      }
    })
    .catch((error) => {
      console.error("검색 중 오류:", error.response || error.message);
      alert("검색 중 문제가 발생했습니다. 다시 시도해주세요.");
    });
};

// 정렬 및 필터링된 결과
const sortedAndFilteredProducts = computed(() => {
  let filteredProducts = products.value;

  // 선호 은행 필터링
  if (showPreferredBanksOnly.value) {
    filteredProducts = filteredProducts.filter((product) => preferredBanks.value.some((bank) => bank === product.company_name));
  }

  // 최저 상환 금액 기준 정렬
  if (sortByMinPayment.value) {
    return filteredProducts
      .map((product) => {
        const sortedOptions = [...product.options].sort((a, b) => {
          const aPayment = a.monthlyPayment || Infinity;
          const bPayment = b.monthlyPayment || Infinity;
          return aPayment - bPayment;
        });
        return { ...product, options: sortedOptions };
      })
      .sort((a, b) => {
        const aMin = a.options[0]?.monthlyPayment || Infinity;
        const bMin = b.options[0]?.monthlyPayment || Infinity;
        return aMin - bMin;
      });
  }

  return filteredProducts;
});

// 초기화
onMounted(() => {
  getPreferredBanks();
});
</script>
