<template>
  <div class="mortgage-container">
    <h2 class="mortgage-title text-center mb-4"><img class="product-img" src="/pictures/주택담보상품조회.png" alt="" /></h2>

    <!-- 조건 검색 폼 -->
    <form @submit.prevent="handleSearch" class="search-form mb-4 p-3 shadow-sm rounded">
      <div class="form-group">
        <label for="loanAmount" class="form-label">빚 금액:</label>
        <input type="number" v-model.number="loanAmount" id="loanAmount" class="form-control" placeholder="대출금액 입력" />
        <small class="text-muted">예: 50000000 (5천만원)</small>
      </div>

      <div class="form-group">
        <label for="loanPeriod" class="form-label">족쇄 기간:</label>
        <input type="number" v-model.number="loanPeriod" id="loanPeriod" class="form-control" placeholder="대출기간 입력" />
        <small class="text-muted">예: 5 (5년)</small>
      </div>

      <div class="form-group">
        <label for="paymentType" class="form-label">족쇄 유형:</label>
        <select v-model="filters.paymentType" id="paymentType" class="form-select">
          <option value="전체">전체</option>
          <option value="고정금리">고정금리</option>
          <option value="변동금리">변동금리</option>
        </select>
      </div>

      <div class="form-group">
        <label for="repaymentType" class="form-label">족쇄 방식:</label>
        <select v-model="filters.repaymentType" id="repaymentType" class="form-select">
          <option value="전체">전체</option>
          <option value="분할상환방식">분할상환방식</option>
          <option value="만기일시상환방식">만기일시상환방식</option>
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

      <button type="submit" class="btn btn-secondary mt-3 w-100">검색</button>
    </form>

    <!-- 결과 출력 -->
    <div class="results-container">
      <MortgageDetailView v-if="isReady && sortedProducts.length > 0" :products="sortedProducts" :loanAmount="loanAmount" :loanPeriod="loanPeriod" />
      <p v-else-if="isReady" class="text-center text-muted">조건에 맞는 결과가 없습니다.</p>
      <p v-else class="text-center text-muted">조건을 입력하세요..</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import MortgageDetailView from "./MortgageDetailView.vue";
import axios from "axios";
import { useNavigationStore } from "@/stores/navigation";

// API URL 설정
const API_URL = "http://127.0.0.1:8000/api/v1";
const navigationStore = useNavigationStore();

const loanAmount = ref(0); // 대출 금액
const loanPeriod = ref(0); // 대출 기간
const sortByMinPayment = ref(false); // 최저 상환 금액 기준 정렬 여부
const filterByPreferredBanks = ref(false); // 선호 은행 필터링 여부
const filters = ref({ paymentType: "전체", repaymentType: "전체" }); // 상환 방식 필터

const products = ref([]); // 결과 데이터
const preferredBanks = ref([]); // 선호 은행 데이터
const isReady = ref(false); // 데이터 로딩 상태

// 선호 은행 데이터 가져오기
const getPreferredBanks = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/accounts/preferred-banks/`, {
      headers: { Authorization: `Token ${localStorage.getItem("token")}` },
    });
    preferredBanks.value = response.data.banks.filter((bank) => bank.is_preferred).map((bank) => bank.company_name);
  } catch (err) {
    console.error("선호 은행 데이터 가져오기 실패:", err.response?.data || err.message);
  }
};

// 검색 버튼 클릭 시 실행
const handleSearch = async () => {
  isReady.value = false; // 로딩 상태 시작
  if (loanAmount.value <= 0 || loanPeriod.value <= 0) {
    alert("대출금액과 대출기간을 올바르게 입력하세요.");
    isReady.value = true;
    return;
  }

  try {
    const response = await axios.get(`${API_URL}/mortgage-loans/`, {
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
      const productId = option.option_id;
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
    isReady.value = true; // 로딩 상태 종료
  } catch (error) {
    console.error("검색 중 오류:", error.response || error.message);
    alert("검색 중 문제가 발생했습니다. 다시 시도해주세요.");
    isReady.value = true;
  }
};

// 월 상환 금액 계산 API 호출
const calculateMonthlyPayment = async (option) => {
  try {
    const response = await axios.get(`${API_URL}/calculate/mortgage/${option.option_id}/`, {
      params: {
        loan_amount: loanAmount.value,
        years: loanPeriod.value,
      },
      headers: { Authorization: `Token ${localStorage.getItem("token")}` },
    });

    if (response.data.calculations?.length > 0) {
      const calculation = response.data.calculations.find((calc) => calc.option_id === option.option_id);
      option.avgPayment = calculation ? calculation.monthly_payment : null;
    }
  } catch (error) {
    console.error("월 상환 금액 계산 중 오류:", error.response || error.message);
  }
};

// 모든 옵션에 대해 월 상환 금액 계산
const calculateAllPayments = async () => {
  const promises = [];
  products.value.forEach((product) => {
    product.options.forEach((option) => promises.push(calculateMonthlyPayment(option)));
  });
  await Promise.all(promises); // 모든 계산이 완료될 때까지 대기
};

// 필터링된 결과
const filteredProducts = computed(() => {
  let result = products.value;

  // 상환 방식 필터링
  if (filters.value.paymentType !== "전체") {
    result = result
      .map((product) => {
        const filteredOptions = product.options.filter((option) => {
          const lendRateType = (option.lend_rate_type_nm || "").trim().toLowerCase();
          return lendRateType === filters.value.paymentType.trim().toLowerCase();
        });
        return filteredOptions.length > 0 ? { ...product, options: filteredOptions } : null;
      })
      .filter((product) => product !== null);
  }

  // 상환 방식 필터링
  if (filters.value.repaymentType !== "전체") {
    result = result
      .map((product) => {
        const filteredOptions = product.options.filter((option) => {
          const RpayType = (option.rpay_type_nm || "").trim().toLowerCase();
          return RpayType === filters.value.repaymentType.trim().toLowerCase();
        });
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
  if (!sortByMinPayment.value) return filteredProducts.value;

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

// 초기화
onMounted(() => {
  getPreferredBanks();
});
</script>

<style scoped>
/* 컨테이너 스타일 */
.mortgage-container {
  font-family: "Noto Sans KR", sans-serif;
  padding: 30px;
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  border-radius: 15px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  margin: 40px auto;
  max-width: 900px;
  animation: fadeIn 1s ease-in-out;
}

/* 제목 이미지 스타일 */
.mortgage-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: gray;
  margin-bottom: 20px;
}

.product-img {
  width: 100%;
  max-width: 450px;
  height: auto;
  animation: slideIn 1s ease-out;
}

/* 검색 폼 스타일 */
.search-form {
  background: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.8s ease-in-out;
}

/* 폼 그룹 */
.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
  color: #495057;
}

small {
  display: block;
  margin-top: 5px;
  color: #6c757d;
}

/* 인풋 필드 스타일 */
input.form-control,
select.form-select {
  border: 1px solid #ced4da;
  border-radius: 8px;
  padding: 10px;
  font-size: 1rem;
  transition: border-color 0.3s ease-in-out;
}

input.form-control:focus,
select.form-select:focus {
  border-color: #6c757d;
  box-shadow: 0 0 8px rgba(108, 117, 125, 0.2);
}

/* 체크박스 */
.form-check-label {
  color: #495057;
  font-size: 0.95rem;
}

.form-check-input {
  margin-right: 8px;
  accent-color: #6c757d;
}

/* 버튼 스타일 */
.btn-secondary {
  font-size: 1.2rem;
  color: white;
  background: linear-gradient(45deg, #6c757d, #5a6268);
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  transition: all 0.3s ease-in-out;
  width: 100%;
  max-width: 200px;
  display: block;
  margin: 20px auto 0;
  text-align: center;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background: linear-gradient(45deg, #5a6268, #6c757d);
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

/* 결과 컨테이너 */
.results-container {
  margin-top: 30px;
}

.text-muted {
  font-size: 1rem;
  color: #6c757d;
}

/* 애니메이션 효과 */
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  0% {
    opacity: 0;
    transform: translateX(-30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
