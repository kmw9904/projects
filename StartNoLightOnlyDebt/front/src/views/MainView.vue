<template>
  <div class="container-fluid p-0">
    <div id="top" class="jumbotron">
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
          <div id="product-section" class="lightbutton">
            <a href="#product-section" class="btn btn-start btn-secondary"><img class="light-button" src="/pictures/빚버튼.png" alt=""></a>
          </div>
        </p>
      </div>
    </div>
  </div>

  <div id="product-section" class="product-section py-5 bg-light">
  <div class="container">
    <h2 id="search" class="section-title text-center mb-4"><img class="search-img" @click="scrollToSection('product-section')" src="/pictures/상품조회.png" alt="검색 상품"></h2>

    <!-- 전체 레이아웃을 좌우로 분리 -->
    <div class="row">
      <!-- 왼쪽 버튼 섹션 -->
      <div class="col-md-4 sticky-col">
        <div class="menu">
          <button class="btn btn-outline-secondary w-100 mb-3" @click="() => { scrollToSection(); targetLoan('CreditLoanView'); }"><img class="loan-img" src="/pictures/신용대출.png" alt="개인대출"></button>
          <button class="btn btn-outline-secondary w-100 mb-3" @click="() => { scrollToSection(); targetLoan('JeonseView'); }"><img class="loan-img" src="/pictures/전세대출.png" alt="전세대출"></button>
          <button class="btn btn-outline-secondary w-100"  @click="() => { scrollToSection(); targetLoan('MortgageView'); }"><img class="loan-img" src="/pictures/담보대출.png" alt="담보대출"></button>
        </div>
      </div>

      <!-- 오른쪽 계산 섹션 -->
      <div class="col-md-8">
        <div class="dynamic-view">
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
  </div>
</div>

<!-- 좋아요가 가장 많은 상품 -->
<div class="top-liked-products py-5 bg-white">
  <div id="best-products" class="container">
    <h2 id="search" class="section-title text-center mb-4"><img class="best-img" src="/pictures/베스트상품.png" alt="베스트 상품"></h2>
    <div v-if="topLikedProducts.length > 0" class="row">
      <div
        v-for="product in topLikedProducts"
        :key="product.product_id"
        class="col-lg-4 col-md-6 mb-4"
      >
      <div class="card product-card shadow-sm">
        <div class="card-body">
            <div id="title-name" class="card-title">
              <div v-if="product.product_type == 'credit'">
                <p>개인 신용 대출</p>
              </div>
              <div v-else-if="product.product_type == 'jeonse'">
                <p>전세 자금 대출</p>
              </div>
              <div v-else-if="product.product_type == 'mortgage'">
                <p>주택 담보 대출</p>
              </div>
            </div>
            <h5 class="card-title"><RouterLink :to="{ name: 'FinancialProductDetail', params: { productId: product.fin_prdt_cd } }" class="product-name">{{ product.product_name }}</RouterLink></h5>
            <p class="card-text">
              {{ product.company_name }}
            </p>
            <p class="card-text">
              <strong>❤️</strong> {{ product.likes }}
            </p>

            <!-- 조건별로 컴포넌트 표시 -->
            <div v-if="product.product_type == 'credit'">
              <CreditLoanDiscussionView
                :productId="product.product_id"
                :productName="product.product_name"
                :optionType="product.product_id"
              />
            </div>
            <div v-if="product.product_type == 'jeonse'">
              <JeonseDiscussionView
                :productId="product.product_id"
                :productName="product.product_name"
                :optionType="product.product_id"
              />
            </div>
            <div v-if="product.product_type == 'mortgage'">
              <MortgageDiscussionView
                :productId="product.product_id"
                :productName="product.product_name"
                :optionType="product.product_id"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-muted">
      <p>아직 좋아요를 받은 상품이 없습니다.</p>
    </div>
  </div>
</div>
<div v-if="topLikedArticle" class="top-liked-article py-5 bg-light">
  <div id="top-article" class="container text-center">
    <h3 class="section-title mb-4"><img class="best-img" src="/pictures/최고게시글.png" alt="베스트 상품"></h3>
    <div class="article-card card shadow-sm mx-auto">
      <div class="card-body">
        <h4 class="article-title card-title mb-3">{{ topLikedArticle.title }}</h4>
        <p class="article-content mb-4">{{ topLikedArticle.content }}</p>
        <p class="article-likes mb-3">
          <strong>❤️</strong> {{ topLikedArticle.likes_count }}
        </p>
        <RouterLink
          :to="{ name: 'ArticleDetail', params: { id: topLikedArticle.id } }"
          class="btn btn-primary"
        >
          게시글 상세 보기
        </RouterLink>
      </div>
    </div>
  </div>
</div>
<div v-else class="text-center py-5">
  <p class="text-muted">아직 좋아요를 받은 게시글이 없습니다.</p>
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
import CreditLoanDiscussionView from "@/loans/CreditLoanDiscussionView.vue";
import JeonseDiscussionView from "@/loans/JeonseDiscussionView.vue";
import MortgageDiscussionView from "@/loans/MortgageDiscussionView.vue";

const API_URL = "http://127.0.0.1:8000";

const topLikedProducts = ref([]);
const store = useArticleStore();

const topLikedArticle = computed(() => store.topLikedArticle);

onMounted(() => {
  store.fetchArticles();
});

const fetchTopLikedProducts = async () => {
  try {
    // 상품 유형별 가장 좋아요가 많은 상품 가져오기
    const creditResponse = await axios.get(`${API_URL}/interactions/credit/top-liked/`);
    const jeonseResponse = await axios.get(`${API_URL}/interactions/jeonse/top-liked/`);
    const mortgageResponse = await axios.get(`${API_URL}/interactions/mortgage/top-liked/`);

    topLikedProducts.value = [creditResponse.data, jeonseResponse.data, mortgageResponse.data].filter((product) => product.likes); // 좋아요가 있는 상품만 필터링
    console.log('좋아요상품 :',topLikedProducts.value);
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
};

const scrollToSection = function() {
  const section = document.getElementById("product-section")
  if (section) {
    section.scrollIntoView({behavior:"smooth"})
  }
}


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
  border: none;
  transition: all 0.3s ease-in-out;
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
  margin-bottom: 2rem;
}

.menu {
  padding-top: 100px;
}
.menu button {
  font-size: 0,5rem;
  padding: 0.8rem;
  border-radius: 5px;
  border: none;
  transition: all 0.3s ease-in-out;
}

.menu button:hover {
  transform: scale(1.05);
  background-color: lightgray;
  color: #fff;
}

/* Dynamic View */
.dynamic-view {
  margin-top: 2rem;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

.loan-img {
  width: 100px;
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

/* 레이아웃 조정 */
.row {
  align-items: flex-start; /* 상단 정렬 */
}

.sticky-col {
  position: sticky;
  top: 20px; /* 상단에서의 고정 위치 */
  z-index: 10; /* 다른 요소 위에 렌더링 */
  height: max-content; /* 컨텐츠 높이에 맞춤 */
}

#search {
  font-size: 3rem;
  font-weight: bold;
  padding-bottom: 30px;
}

.best-img {
  width: 500px;
  height: auto;
}

.search-img {
  width: 1000px;
  height: auto; 
}

#product-section {
  background-color: transparent !important; /* 부모 요소 배경색 제거 */
}

a.btn {
  background-color: transparent !important; /* 부모 링크 배경 제거 */
  border: none !important; /* 테두리 제거 */
  box-shadow: none !important; /* 그림자 제거 */
  padding: 0 !important; /* 여백 제거 */
  margin: 0 !important; /* 외부 여백 제거 */
}

.light-button {
  background-color: transparent !important;
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
  width: 300px;
  height: auto;
}

/* 좋아요가 가장 많은 상품 스타일 */
.top-liked-products {
  background-color: #f9f9f9;
  padding: 3rem 0;
}

.product-card {
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: all 0.3s ease-in-out;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: #ffffff;
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 0.5rem;
  text-align: center;
  padding-bottom: 10px;
}

#title-name {
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 0.5rem;
  text-align: center;
}

.card-text {
  font-size: 1.2rem;
  color: #495057;
  text-align: center;
}

.card-body {
  padding: 1.5rem;
}

/* 텍스트 중앙 정렬 */
.text-muted {
  font-size: 0.95rem;
  color: #6c757d;
}

/* 가장 좋아요를 많이 받은 게시글 스타일 */
.top-liked-article {
  background-color: #f8f9fa;
  padding: 3rem 0;
}

.article-card {
  max-width: 600px;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  transition: all 0.3s ease-in-out;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.article-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #343a40;
  text-align: center;
  margin-bottom: 1rem;
}

.article-content {
  font-size: 1.2rem;
  color: #495057;
  text-align: left;
}

.article-likes {
  font-size: 1.1rem;
  color: #6c757d;
  text-align: right;
}

.btn-primary {
  background-color: #6c757d;
  border: none;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.8rem 1.5rem;
  border-radius: 5px;
}

.btn-primary:hover {
  background-color: #5a6268;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-name {
  color: black; /* 링크 텍스트를 검은색으로 설정 */
  text-decoration: none; /* 밑줄 제거 */
}
</style>
