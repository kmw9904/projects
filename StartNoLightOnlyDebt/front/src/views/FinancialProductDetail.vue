<template>
  <div class="detail-container">
    <h3 class="text-center mb-4">상품 상세 정보</h3>

    <div v-if="product" class="product-detail card shadow-sm p-4">
      <div class="bank-img text-center mb-4">
        <img :src="`/pictures/${product.company_name}.png`" alt="금융 회사 로고" />
      </div>

      <p>
        <strong>금융 회사:</strong>
        {{ product.company_name || "정보 없음" }}
        <a :href="`${product.homp_url}`">바로가기</a>
      </p>
      <p>
        <strong>상품명:</strong>
        {{ product.product_name || "정보 없음" }}
      </p>
      <p>
        <strong>가입 방법:</strong>
        {{ product.join_way || "정보 없음" }}
      </p>
      <p>
        <strong>부대 비용:</strong>
        {{ product.loan_inci_expn || "정보 없음" }}
      </p>
      <p>
        <strong>중도상환수수료:</strong>
        {{ product.erly_rpay_fee || "정보 없음" }}
      </p>
      <p>
        <strong>연체 이자율:</strong>
        {{ product.dly_rate || "정보 없음" }}
      </p>
      <p>
        <strong>대출 한도:</strong>
        {{ product.loan_lmt || "정보 없음" }}
      </p>
      <p>
        <strong>공시 제출 월:</strong>
        {{ product.dcls_month || "정보 없음" }}
      </p>
      <p>
        <strong>공시 시작일:</strong>
        {{ product.dcls_strt_day || "정보 없음" }}
      </p>
      <p>
        <strong>공시 종료일:</strong>
        {{ product.dcls_end_day || "정보 없음" }}
      </p>
      <p>
        <strong>금융회사 제출일:</strong>
        {{ product.fin_co_subm_day || "정보 없음" }}
      </p>
      <p>
        <strong>상품 구분:</strong>
        {{ product.prdt_div || "정보 없음" }}
      </p>
      <button @click="store.goBack">뒤로 가기</button>
    </div>

    <div v-else class="text-center text-muted">
      <p>상품 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { useNavigationStore } from "@/stores/navigation";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const store = useNavigationStore();

// 현재 라우트에서 productId 가져오기
const route = useRoute();
const productId = route.params.productId;

// 상품 데이터를 저장할 변수
const product = ref(null);

// 데이터 로드 함수
const fetchProductDetail = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/product/${productId}/`);
    product.value = response.data;
    console.log(product.value);
  } catch (error) {
    console.error("상품 정보를 가져오는 중 오류 발생:", error.response || error.message);
  }
};

// 컴포넌트가 마운트될 때 데이터 로드
onMounted(() => {
  fetchProductDetail();
});
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.bank-img img {
  max-width: 100px;
  height: auto;
}

.product-detail {
  background: #ffffff;
  border: none;
  border-radius: 10px;
}
</style>
