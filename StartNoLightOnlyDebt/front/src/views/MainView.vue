<template>
  <div>
    <h1>Start No Light Only Debt</h1>
    <h2>금융 상품 조회</h2>
  </div>

  <!-- 네비게이션 -->
  <div>
    <RouterLink :to="{ name: 'CreditLoanView' }">개인 대출</RouterLink>
    |
    <RouterLink :to="{ name: 'JeonseView' }">전세 대출</RouterLink>
    |
    <RouterLink :to="{ name: 'MortgageView' }">담보 대출</RouterLink>
  </div>

  <!-- 상품 둘러보기 -->
  <div>
    <h3>상품 둘러보기</h3>
  </div>

  <!-- 사람들이 좋아요한 상품 -->
  <div>
    <h4>사람들이 좋아요한 상품</h4>

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

    <div>
      
    </div>

    <!-- 데이터가 없을 경우 -->
    <div v-if="topLikedCredit.length === 0 && topLikedJeonse.length === 0 && topLikedMortgage.length === 0">
      <p>아직 좋아요를 받은 상품이 없습니다. 상품을 검색하고 좋아요를 눌러보세요!</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const topLikedCredit = ref([]);
const topLikedJeonse = ref([]);
const topLikedMortgage = ref([]);

// 좋아요가 높은 상품 가져오기
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
</script>

<style scoped>
h4 {
  margin-top: 20px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
}
</style>
