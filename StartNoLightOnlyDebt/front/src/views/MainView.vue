<template>
  <div class="container-fluid p-0">
    <div class="jumbotron">
      <div class="text-container">
        <h1 class="text-title">대출 정보 제공 서비스</h1>
        <p class="lead">신뢰할 수 있는 금융 정보를 제공합니다.</p>
        <p>
          <button type="button" class="btn btn-start btn-secondary">빚으로 시작하기</button>
        </p>
      </div>
    </div>

    <div class="product-section py-5 bg-light">
      <div class="container">
        <h2 class="section-title text-center mb-4">금융 상품 조회</h2>

        <div class="menu d-flex justify-content-center mb-4">
          <button class="btn btn-outline-primary mx-2" @click="targetLoan('CreditLoanView')">신용 대출</button>
          <button class="btn btn-outline-primary mx-2" @click="targetLoan('JeonseView')">전세 대출</button>
          <button class="btn btn-outline-primary mx-2" @click="targetLoan('MortgageView')">담보 대출</button>
        </div>

        <div class="dynamic-view mt-4">
          <div v-if="nowLoan === 'CreditLoanView'">
            <CreditLoanView />
          </div>
          <div v-else-if="nowLoan === 'JeonseView'">
            <JeonseView />
          </div>
          <div v-else-if="nowLoan === 'MortgageView'">
            <MortgageView />
          </div>
        </div>
      </div>
    </div>

    <div class="explore-section py-5 bg-white">
      <div class="container">
        <h3 class="explore-title text-center mb-4">상품 둘러보기</h3>
      </div>
    </div>

    <div class="liked-products py-5 bg-light">
      <div class="container">
        <h4 class="liked-title text-center mb-4">사람들이 좋아요한 상품</h4>

        <div v-if="topLikedCredit.length > 0">
          <h5 class="product-category text-center">개인 대출</h5>
          <ul class="list-group list-group-flush">
            <li v-for="product in topLikedCredit" :key="product.product_id" class="list-group-item">
              <div class="d-flex justify-content-between align-items-center">
                <span>
                  <strong>{{ product.product_name }}</strong>
                  ({{ product.company_name }})
                  <br />
                  좋아요: {{ product.likes }}
                </span>
                <RouterLink :to="{ name: 'CreditLoanDiscussionView', params: { productId: product.product_id } }" class="btn btn-link">댓글 보기</RouterLink>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { RouterLink } from "vue-router";
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import CreditLoanView from "@/loans/CreditLoanView.vue";
import JeonseView from "@/loans/JeonseView.vue";
import MortgageView from "@/loans/MortgageView.vue";
import { useBankStore } from "@/stores/bank";

const API_URL = "http://127.0.0.1:8000";

const topLikedCredit = ref([]);
const topLikedJeonse = ref([]);
const topLikedMortgage = ref([]);
const store = useArticleStore();

const topLikedArticle = computed(() => store.topLikedArticle);

onMounted(() => {
  store.fetchArticles();
});

const fetchTopLikedProducts = async () => {
  try {
    const creditResponse = await axios.get(`${API_URL}/credit/top-liked/`);
    topLikedCredit.value = creditResponse.data;

    const jeonseResponse = await axios.get(`${API_URL}/jeonse/top-liked/`);
    topLikedJeonse.value = jeonseResponse.data;

    const mortgageResponse = await axios.get(`${API_URL}/mortgage/top-liked/`);
    topLikedMortgage.value = mortgageResponse.data;
  } catch (error) {
    console.error("최고 좋아요 상품 가져오기 실패:", error);
  }
};

onMounted(() => {
  fetchTopLikedProducts();
});
const nowLoan = ref("CreditLoanView");
const targetLoan = function (loan) {
  nowLoan.value = loan;
  console.log(nowLoan.value);
};
</script>

<style scoped>
/* Jumbotron 스타일 */
.jumbotron {
  height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("/public/pictures/배경화면.jpg");
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.text-container {
  max-width: 600px;
  animation: fadeIn 2s ease-in-out;
}

.text-title {
  font-size: 3.5rem;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.lead {
  font-size: 1.25rem;
  margin-top: 1rem;
}

.btn-start {
  font-size: 1.2rem;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  transition: all 0.3s ease-in-out;
}

.btn-start:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Product Section */
.product-section {
  padding: 2rem 0;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
}

/* Explore Section */
.explore-title {
  font-size: 1.8rem;
  font-weight: bold;
}

/* Liked Products */
.liked-title {
  font-size: 1.8rem;
  font-weight: bold;
}

.product-category {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

/* 등장 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
