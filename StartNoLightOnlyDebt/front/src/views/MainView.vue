<template>
  <div class="container-fluid p-0">
    <div class="jumbotron">
      <div class="text-container">
        <h1 class="text-title">대출 정보 제공 서비스</h1>
        <p class="lead">신뢰할 수 있는 금융 정보를 제공합니다.</p>
        <p>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <div id="product-section">
            <a href="#product-section" class="btn btn-start btn-secondary">빚으로 시작하기</a>
          </div>
        </p>
      </div>
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

  <!-- 개인 대출 -->
  <div v-if="topLikedCredit.length > 0">
    <h5>개인 대출</h5>
    <ul>
      <li v-for="product in topLikedCredit" :key="product.product_id">
        <p>
          <strong>{{ product.product_name }}</strong>
          ({{ product.company_name }})
          <br />
          좋아요: {{ product.likes }}
        </p>
        <RouterLink :to="{ name: 'CreditLoanDiscussionView', params: { productId: product.product_id } }">댓글 보기</RouterLink>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>아직 좋아요를 받은 개인 대출 상품이 없습니다.</p>
  </div>

  <!-- 전세 대출 -->
  <div v-if="topLikedJeonse.length > 0">
    <h5>전세 대출</h5>
    <ul>
      <li v-for="product in topLikedJeonse" :key="product.product_id">
        <p>
          <strong>{{ product.product_name }}</strong>
          ({{ product.company_name }})
          <br />
          좋아요: {{ product.likes }}
        </p>
        <RouterLink :to="{ name: 'JeonseLoanDiscussionView', params: { productId: product.product_id } }">댓글 보기</RouterLink>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>아직 좋아요를 받은 전세 대출 상품이 없습니다.</p>
  </div>
  <!-- 담보 대출 -->
  <div v-if="topLikedMortgage.length > 0">
    <h5>담보 대출</h5>
    <ul>
      <li v-for="product in topLikedMortgage" :key="product.product_id">
        <p>
          <strong>{{ product.product_name }}</strong>
          ({{ product.company_name }})
          <br />
          좋아요: {{ product.likes }}
        </p>
        <RouterLink :to="{ name: 'MortgageLoanDiscussionView', params: { productId: product.product_id } }">댓글 보기</RouterLink>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>아직 좋아요를 받은 담보 대출 상품이 없습니다.</p>
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
  <div>
    <div v-if="topLikedArticle">
      <h3>가장 좋아요를 많이 받은 게시글</h3>
      <h4>{{ topLikedArticle.title }}</h4>
      <p>{{ topLikedArticle.content }}</p>
      <p>좋아요: {{ topLikedArticle.likes_count }}</p>
      <RouterLink :to="{ name: 'ArticleDetail', params: { id: topLikedArticle.id } }">상세 보기</RouterLink>
    </div>
    <div v-else>
      <p>아직 좋아요를 받은 게시글이 없습니다.</p>
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
    const creditResponse = await axios.get(`${API_URL}/interactions/credit/top-liked/`);
    topLikedCredit.value = creditResponse.data;

    const jeonseResponse = await axios.get(`${API_URL}/interactions/jeonse/top-liked/`);
    topLikedJeonse.value = jeonseResponse.data;

    const mortgageResponse = await axios.get(`${API_URL}/interactions/mortgage/top-liked/`);
    topLikedMortgage.value = mortgageResponse.data;
  } catch (error) {
    console.error("최고 좋아요 상품 가져오기 실패:", error.response?.data || error.message);
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
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

.btn-start {
  font-size: 1.2rem;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  transition: all 0.3s ease-in-out;
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.btn-start:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: #5a6268;
}

/* Product Section */
.product-section {
  padding: 2rem 0;
  background-color: #f8f9fa;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
}

.menu button {
  font-size: 1rem;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
}

.menu button:hover {
  transform: scale(1.05);
  background-color: #0056b3;
  color: #fff;
}

/* Dynamic View */
.dynamic-view {
  margin-top: 2rem;
}

/* 개인 대출 섹션 */
ul {
  list-style: none;
  padding: 0;
}

h5 {
  font-size: 1.3rem;
  font-weight: bold;
  margin-top: 2rem;
  color: #495057;
}

li {
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

li:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background-color: #f8f9fa;
}

p {
  margin: 0;
}

button.btn-link {
  color: #007bff;
  text-decoration: none;
  font-size: 0.9rem;
}

button.btn-link:hover {
  text-decoration: underline;
}

/* Explore Section */
.explore-section {
  padding: 2rem 0;
  background-color: #ffffff;
}

.explore-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #343a40;
}

/* Liked Products */
.liked-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #343a40;
}

.list-group-item {
  border: none;
  padding: 1rem 0;
}

.list-group-item:hover {
  background-color: #f1f1f1;
}

.product-category {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #495057;
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

html {
  scroll-padding-top: 200px; /* 사진 크기만큼 간격 추가 */
}

</style>
