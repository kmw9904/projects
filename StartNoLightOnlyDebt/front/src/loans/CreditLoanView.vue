<template>
  <div class="credit-loan-container">
    <h2 class="text-center mb-4"><img class="product-img" src="/pictures/개인신용상품조회.png" alt="" /></h2>

    <!-- 검색 조건 입력 -->
    <form @submit.prevent="handleSearch" class="search-form mb-4 p-3 shadow-sm rounded">
      <div class="form-group">
        <label for="loanAmount" class="form-label">빚 금액:</label>
        <input type="number" class="form-control" v-model.number="loanAmount" id="loanAmount" placeholder="대출금액 입력" />
        <small class="text-muted">예: 5000000 (5백만원)</small>
      </div>

      <div class="form-group">
        <label for="loanPeriod" class="form-label">족쇄 기간:</label>
        <input type="number" class="form-control" v-model.number="loanPeriod" id="loanPeriod" placeholder="대출기간 입력" />
        <small class="text-muted">예: 1 (1년)</small>
      </div>

      <div class="form-group">
        <label for="loanType" class="form-label">족쇄 종류:</label>
        <select v-model="loanType" id="loanType" class="form-select">
          <option value="전체">전체</option>
          <option value="일반신용대출">일반신용대출</option>
          <option value="장기카드대출">장기카드대출</option>
        </select>
      </div>

      <div class="form-check">
        <input type="checkbox" v-model="sortByMinPayment" class="form-check-input" id="sortByMinPayment" />
        <label for="sortByMinPayment" class="form-check-label">최저 상환 금액 기준 정렬</label>
      </div>

      <div class="form-check">
        <input type="checkbox" v-model="filterByPreferredBanks" class="form-check-input" id="filterByPreferredBanks" />
        <label for="filterByPreferredBanks" class="form-check-label">선호 은행만 보기</label>
      </div>

      <button type="submit" class="btn btn-secondary mt-3">검색</button>
    </form>

    <!-- 결과 출력 -->
    <div class="results-container">
      <CreditLoanDetailView v-if="isReady && sortedProducts.length > 0" :products="sortedProducts" :loanAmount="loanAmount" :loanPeriod="loanPeriod" />
      <p v-else-if="isReady" class="text-center text-muted">검색 결과가 없습니다.</p>
      <p v-else class="text-center text-muted">조건을 입력하세요..</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import CreditLoanDetailView from "./CreditLoanDetailView.vue";
import axios from "axios";

// API URL 설정
const API_URL = "http://127.0.0.1:8000/api/v1";

const loanAmount = ref(0); // 대출 금액
const loanPeriod = ref(0); // 대출 기간
const loanType = ref("전체"); // 대출 종류
const sortByMinPayment = ref(false); // 최저 상환 금액 기준 정렬 여부
const filterByPreferredBanks = ref(false); // 선호 은행 필터링 여부

const products = ref([]); // 결과 데이터
const preferredBanks = ref([]); // 선호 은행 데이터
const isReady = ref(false); // 데이터 로딩 상태

// 사용자 선호 은행 가져오기
const getPreferredBanks = () => {
  return axios({
    method: "get",
    url: `http://127.0.0.1:8000/accounts/preferred-banks/`,
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  })
    .then((res) => {
      preferredBanks.value = res.data.banks.filter((bank) => bank.is_preferred).map((bank) => bank.company_name);
    })
    .catch((err) => {
      console.error("선호 은행 데이터 가져오기 실패:", err.response?.data || err.message);
    });
};

// 검색 버튼 클릭 시 실행
const handleSearch = async () => {
  isReady.value = false; // 로딩 시작
  if (loanAmount.value <= 0 || loanPeriod.value <= 0) {
    alert("대출금액과 대출기간을 올바르게 입력하세요.");
    isReady.value = true;
    return;
  }

  try {
    const response = await axios.get(`${API_URL}/credit-loans/`, {
      params: {
        loan_amount: loanAmount.value,
        loan_period: loanPeriod.value,
      },
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    });

    const options = response.data;
    const groupedProducts = {};

    // 데이터 그룹화
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

    products.value = Object.values(groupedProducts);
    await calculateAllPayments(); // 월 상환 금액 계산
    isReady.value = true; // 로딩 완료
  } catch (error) {
    console.error("검색 중 오류:", error.response || error.message);
    alert("검색 중 문제가 발생했습니다. 다시 시도해주세요.");
    isReady.value = true;
  }
};

// 월 상환 금액 계산 API 호출
const calculateMonthlyPayment = (option) => {
  return axios({
    method: "get",
    url: `${API_URL}/calculate/credit/${option.option_id}/`,
    params: {
      loan_amount: loanAmount.value,
      years: loanPeriod.value,
    },
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  })
    .then((response) => {
      if (response.data.calculations && response.data.calculations.length > 0) {
        const calculation = response.data.calculations.find((calc) => calc.option_id === option.option_id);
        option.monthlyPayment = calculation ? calculation.monthly_payment : null;
      } else {
        console.warn("월 상환 금액 데이터가 없습니다.");
      }
    })
    .catch((error) => {
      console.error("월 상환 금액 계산 중 오류:", error.response || error.message);
    });
};

// 모든 옵션에 대해 월 상환 금액 계산
const calculateAllPayments = async () => {
  const promises = [];
  products.value.forEach((product) => {
    product.options.forEach((option) => {
      promises.push(calculateMonthlyPayment(option));
    });
  });
  await Promise.all(promises); // 모든 계산이 완료될 때까지 대기
};

// 필터링된 결과
const filteredProducts = computed(() => {
  let result = products.value;

  // 대출 종류 필터링
  if (loanType.value !== "전체") {
    result = result
      .map((product) => {
        const filteredOptions = product.options.filter((option) => option.product.product_name.toLowerCase().includes(loanType.value.toLowerCase()));
        return filteredOptions.length > 0 ? { ...product, options: filteredOptions } : null;
      })
      .filter((product) => product !== null);
  }

  // 선호 은행 필터링
  if (filterByPreferredBanks.value) {
    result = result.filter((product) => preferredBanks.value.includes(product.company_name));
  }

  return result;
});

// 정렬된 결과
const sortedProducts = computed(() => {
  if (!sortByMinPayment.value) {
    return filteredProducts.value;
  }

  return filteredProducts.value
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
});

// 초기화
onMounted(() => {
  getPreferredBanks();
});
</script>

<style scoped>
.credit-loan-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  max-width: 800px;
}

h2 {
  font-size: 2rem;
  font-weight: bold;
  color: gray;
}

.search-form {
  background: #ffffff;
  border: 1px solid #ddd;
}

.product-img {
  width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
}

small {
  display: block;
  margin-top: 5px;
  color: #6c757d;
}

.btn {
  width: 100%;
}

.results-container {
  margin-top: 20px;
}

.text-muted {
  font-size: 0.9rem;
  color: #6c757d;
}

.btn-secondary {
  font-size: 1.2rem; /* 글씨 크기 */
  color: white; /* 글씨 색상 */
  background-color: #6c757d; /* 기본 배경색 */
  border: none; /* 테두리 제거 */
  padding: 0.8rem 2rem; /* 버튼 크기 */
  border-radius: 30px; /* 둥근 모서리 */
  transition: all 0.3s ease-in-out; /* 호버 애니메이션 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

.btn-secondary:hover {
  background-color: #5a6268; /* 호버 시 배경색 */
  color: #f1f1f1; /* 호버 시 글씨 색상 */
  transform: translateY(-3px); /* 호버 시 살짝 떠오르는 효과 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 호버 시 그림자 강화 */
}
</style>
