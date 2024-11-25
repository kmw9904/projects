<template>
  <div class="detail-container">
    <h3 class="text-center mb-4">상품 상세 정보</h3>

    <div v-if="product" class="product-detail card shadow-sm p-4">
      <div class="bank-img text-center mb-4">
        <img :src="`/pictures/${product.company_name}.png`" alt="금융 회사 로고" />
      </div>

      <div class="product-info">
        <p>
          <strong>금융 회사</strong>
          <br />
          {{ product.company_name || "정보 없음" }}
          <a :href="`${product.homp_url}`" class="btn-link">바로가기</a>
        </p>
        <p>
          <strong>상품명</strong>
          <br />
          {{ product.product_name || "정보 없음" }}
        </p>
        <p>
          <strong>가입 방법</strong>
          <br />
          {{ product.join_way || "정보 없음" }}
        </p>
        <p>
          <strong>부대 비용</strong>
          <br />
          {{ product.loan_inci_expn || "정보 없음" }}
        </p>
        <p>
          <strong>중도상환수수료</strong>
          <br />
          {{ product.erly_rpay_fee || "정보 없음" }}
        </p>
        <p>
          <strong>연체 이자율</strong>
          <br />
          {{ product.dly_rate || "정보 없음" }}
        </p>
        <p>
          <strong>대출 한도</strong>
          <br />
          {{ product.loan_lmt || "정보 없음" }}
        </p>
        <p>
          <strong>공시 제출 월</strong>
          <br />
          {{ product.dcls_month || "정보 없음" }}
        </p>
        <p>
          <strong>공시 시작일</strong>
          <br />
          {{ product.dcls_strt_day || "정보 없음" }}
        </p>
        <p>
          <strong>공시 종료일</strong>
          <br />
          {{ product.dcls_end_day || "정보 없음" }}
        </p>
        <p>
          <strong>금융회사 제출일</strong>
          <br />
          {{ product.fin_co_subm_day || "정보 없음" }}
        </p>
        <p>
          <strong>상품 구분</strong>
          <br />
          {{ product.prdt_div || "정보 없음" }}
        </p>
      </div>

      <div class="text-center mt-4">
        <button @click="store.goBack" class="btn btn-primary">뒤로 가기</button>
      </div>
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
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.bank-img img {
  max-width: 150px;
  height: auto;
  margin-bottom: 20px;
}

.product-detail {
  background: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-info p {
  font-size: 1rem;
  line-height: 1.8;
  color: #555;
  border-bottom: 1px solid #f1f1f1; /* 항목 구분선 */
  padding: 8px 0;
}

.product-info strong {
  color: #333;
  font-weight: 600;
}

a.btn-link {
  color: #007bff;
  text-decoration: underline;
}

a.btn-link:hover {
  color: #0056b3;
}

button.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 25px;
  transition: all 0.3s ease-in-out;
}

button.btn-primary:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
