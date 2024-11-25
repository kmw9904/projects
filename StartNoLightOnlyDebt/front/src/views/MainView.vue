<template>
  <!-- 메인 -->
  <div class="container-fluid p-0">
    <div id="top" class="jumbotron">
      <div class="text-container">
        <h1 class="text-title">대출 정보 제공 SNO 서비스</h1>
        <p class="lead">신뢰할 수 있는 금융 정보를 제공합니다.</p>
        <p>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <div id="product-section1" class="lightbutton">
            <h2 @click="goToIntroduceSection" >시작하기</h2>
          </div>
        </p>
      </div>
    </div>
  </div>

<div class="introduce" id="introduce-section">
  <p>꼭 필요했던 대출</p>
</div>

<div class="intro-description">
  <p class="title">금융을 넘어</p>
  <p class="title">일상을 더 편리하게</p>
</div>

<div class="intro-budget-image">
  <img src="/pictures/예산.jpg" alt="예산">
</div>
 
<div class="list-description">
  <p class="title">월 납입금 예상, 선호 은행 대출 리스트까지</p>
  <p class="title">SNO와 함께</p>
  <p class="subtitle" >접근하기 어려웠던 대출 정보</p>
  <p class="subtitle" >편하게 조회하고 대출 알아보세요</p>
</div>

<div class="product-description-img">
  <img src="/pictures/상품평.jpg" alt="상품평">
</div>

<div class="product-description">
  <p class="title" >대출 상품에 대한 사람들의 평가까지</p>
  <p class="subtitle" >다양한 사람들의 의견을 들어</p>
  <p class="subtitle" >SNO와 함께 추천 받으세요</p>
</div>


<!-- 상품 조회 -->
<div id="product-section" class="product-section py-5 bg-light">
  <div class="container">
    <h2 id="search" class="section-title text-center mb-4">대출 상품 검색하기</h2>
  
    <!-- 전체 레이아웃을 좌우로 분리 -->
    <div class="row">
      <!-- 왼쪽 버튼 섹션 -->
      <div class="col-md-4 sticky-col">
        <div class="menu">
          <button class="btn btn-outline-secondary w-100 mb-3" @click="() => { scrollToIntroduce(); targetLoan('CreditLoanView'); }"><img class="loan-img" src="/pictures/신용대출.png" alt="개인대출"></button>
          <button class="btn btn-outline-secondary w-100 mb-3" @click="() => { scrollToIntroduce(); targetLoan('JeonseView'); }"><img class="loan-img" src="/pictures/전세대출.png" alt="전세대출"></button>
          <button class="btn btn-outline-secondary w-100"  @click="() => { scrollToIntroduce(); targetLoan('MortgageView'); }"><img class="loan-img" src="/pictures/담보대출.png" alt="담보대출"></button>
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

<div class="article-description-img">
  <img src="/pictures/게시글.jpg" alt="게시글">
</div>
<div class="article-description">
  <p class="title">가장 인기많은 상품을 둘러보세요</p>
  <p class="subtitle">사람들의 다양한 의견을 들어볼 수 있어요</p>
</div>

<!-- 좋아요가 가장 많은 상품 조회-->
<div class="top-liked-products py-5 bg-white">
  <div id="best-products" class="container">
    <h2 id="search" class="section-title text-center mb-4">베스트 상품</h2>
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

<div class="best-description-img">
  <img src="/pictures/알티클.jpg" alt="베스트 게시글">
</div>
<div class="best-description">
  <p class="title">가끔은 재미있는 글, 은행 정보에 대해서 둘러보세요</p>
  <p class="subtitle">SNO는 은행 정보 뿐만 아니라 커뮤니케이션 장소도 제공합니다.</p>
</div>

<!-- 베스트 게시글 조회 -->
<div v-if="topLikedArticle" class="top-liked-article py-5 bg-light">
  <div id="top-article" class="container text-center">
    <h2 class="section-title mb-4">베스트 게시글</h2>
    <div class="article-card card shadow-sm mx-auto">
      <div class="card-body">
        <h4 class="article-title card-title mb-3">{{ topLikedArticle.title }}</h4>
        <p class="article-content mb-4">{{ topLikedArticle.content }}</p>
        <p class="article-likes mb-3">
          <strong>❤️</strong> {{ topLikedArticle.likes_count }}
        </p>
        <RouterLink
          :to="{ name: 'ArticleDetail', params: { id: topLikedArticle.id } }"
          class="btn btn-second"
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

<!-- 푸터 -->
<footer class="footer">
  <div class="container">
    <p>© 2024 Start No Light Only Debt. All rights reserved.</p>
    <p>어려운 대출 정보를 모두가 손쉽고 편리하게 대출 정보를 받을 수 있도록 우리 프로그램은 빛을 향해 나아갑니다.</p>
    <p>
      Contact us:
      <a href="mailto:support@example.com">kms990415@naver.com</a>
    </p>
  </div>
</footer>


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
    const creditResponse = await axios.get(`${API_URL}/interactions/credit/top-liked/`);
    const jeonseResponse = await axios.get(`${API_URL}/interactions/jeonse/top-liked/`);
    const mortgageResponse = await axios.get(`${API_URL}/interactions/mortgage/top-liked/`);

    topLikedProducts.value = [creditResponse.data, jeonseResponse.data, mortgageResponse.data].filter((product) => product.likes);
    console.log('좋아요상품 :', topLikedProducts.value);
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

const goToIntroduceSection = () => {
  const section = document.getElementById("product-section1");
  if (section) {
    section.scrollIntoView({ behavior: "smooth" }); // 부드러운 스크롤 이동
  } else {
    console.warn('Section "introduce-section" not found.');
  }
};

const scrollToIntroduce = (sectionId) => {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
};

onMounted(() => {
  console.log("Component mounted");

  // introduce-section에 대한 Observer
  const introduceSection = document.getElementById("introduce-section");
  if (introduceSection) {
    console.log("Introduce section found");

    const observerIntroduce = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          introduceSection.classList.add("scrolled");
          console.log("Scrolled class added to introduce-section");
        } else {
          introduceSection.classList.remove("scrolled");
          console.log("Scrolled class removed from introduce-section");
        }
      });
    }, {
      threshold: 0.5 // 섹션의 50%가 화면에 보이면 작동
    });

    observerIntroduce.observe(introduceSection);
    console.log("Intersection Observer added for introduce-section");
  } else {
    console.log("Introduce section NOT found");
  }

  // intro-description에 대한 Observer
  const introDescription = document.querySelector(".intro-description");
  if (introDescription) {
    console.log("Intro description section found");

    const observerIntroDescription = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          introDescription.classList.add("scrolled");
          console.log("Scrolled class added to intro-description");
        } else {
          introDescription.classList.remove("scrolled");
          console.log("Scrolled class removed from intro-description");
        }
      });
    }, {
      threshold: 0.5
    });

    observerIntroDescription.observe(introDescription);
    console.log("Intersection Observer added for intro-description");
  } else {
    console.log("Intro description section NOT found");
  }

  // intro-budget-image에 대한 Observer
  const introBudgetImage = document.querySelector(".intro-budget-image");
  if (introBudgetImage) {
    console.log("Intro budget image section found");

    const observerIntroBudgetImage = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          introBudgetImage.classList.add("scrolled");
          console.log("Scrolled class added to intro-budget-image");
        } else {
          introBudgetImage.classList.remove("scrolled");
          console.log("Scrolled class removed from intro-budget-image");
        }
      });
    }, {
      threshold: 0.5
    });

    observerIntroBudgetImage.observe(introBudgetImage);
    console.log("Intersection Observer added for intro-budget-image");
  } else {
    console.log("Intro budget image section NOT found");
  }

  // list-description에 대한 Observer
  const listDescription = document.querySelector(".list-description");
  if (listDescription) {
    console.log("List description section found");

    const observerListDescription = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          listDescription.classList.add("scrolled");
          console.log("Scrolled class added to list-description");
        } else {
          listDescription.classList.remove("scrolled");
          console.log("Scrolled class removed from list-description");
        }
      });
    }, {
      threshold: 0.5
    });

    observerListDescription.observe(listDescription);
    console.log("Intersection Observer added for list-description");
  } else {
    console.log("List description section NOT found");
  }

  // product-description-img에 대한 Observer
  const productDescriptionImg = document.querySelector(".product-description-img");
  if (productDescriptionImg) {
    console.log("Product description image section found");

    const observerProductDescriptionImg = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          productDescriptionImg.classList.add("scrolled");
          console.log("Scrolled class added to product-description-img");
        } else {
          productDescriptionImg.classList.remove("scrolled");
          console.log("Scrolled class removed from product-description-img");
        }
      });
    }, {
      threshold: 0.5
    });

    observerProductDescriptionImg.observe(productDescriptionImg);
    console.log("Intersection Observer added for product-description-img");
  } else {
    console.log("Product description image section NOT found");
  }

  // product-description에 대한 Observer
  const productDescription = document.querySelector(".product-description");
  if (productDescription) {
    console.log("Product description section found");

    const observerProductDescription = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          productDescription.classList.add("scrolled");
          console.log("Scrolled class added to product-description");
        } else {
          productDescription.classList.remove("scrolled");
          console.log("Scrolled class removed from product-description");
        }
      });
    }, {
      threshold: 0.5
    });

    observerProductDescription.observe(productDescription);
    console.log("Intersection Observer added for product-description");
  } else {
    console.log("Product description section NOT found");
  }

  // 추가된 섹션: product-description-img에 대한 Observer
  const productDescriptionImgNew = document.querySelector(".product-description-img");
  if (productDescriptionImgNew) {
    console.log("Product description image section found");

    const observerProductDescriptionImgNew = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          productDescriptionImgNew.classList.add("scrolled");
          console.log("Scrolled class added to product-description-img");
        } else {
          productDescriptionImgNew.classList.remove("scrolled");
          console.log("Scrolled class removed from product-description-img");
        }
      });
    }, {
      threshold: 0.5
    });

    observerProductDescriptionImgNew.observe(productDescriptionImgNew);
    console.log("Intersection Observer added for product-description-img");
  } else {
    console.log("Product description image section NOT found");
  }

  // 추가된 섹션: product-description에 대한 Observer
  const productDescriptionNew = document.querySelector(".product-description");
  if (productDescriptionNew) {
    console.log("Product description section found");

    const observerProductDescriptionNew = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          productDescriptionNew.classList.add("scrolled");
          console.log("Scrolled class added to product-description");
        } else {
          productDescriptionNew.classList.remove("scrolled");
          console.log("Scrolled class removed from product-description");
        }
      });
    }, {
      threshold: 0.5
    });

    observerProductDescriptionNew.observe(productDescriptionNew);
    console.log("Intersection Observer added for product-description");
  } else {
    console.log("Product description section NOT found");
  }
  
    // 추가된 섹션: article-description-img에 대한 Observer
  const articleDescriptionImg = document.querySelector(".article-description-img");
  if (articleDescriptionImg) {
    console.log("Article description image section found");

    const observerArticleDescriptionImg = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          articleDescriptionImg.classList.add("scrolled");
          console.log("Scrolled class added to article-description-img");
        } else {
          articleDescriptionImg.classList.remove("scrolled");
          console.log("Scrolled class removed from article-description-img");
        }
      });
    }, {
      threshold: 0.5
    });

    observerArticleDescriptionImg.observe(articleDescriptionImg);
    console.log("Intersection Observer added for article-description-img");
  } else {
    console.log("Article description image section NOT found");
  }

  // 추가된 섹션: article-description에 대한 Observer
  const articleDescription = document.querySelector(".article-description");
  if (articleDescription) {
    console.log("Article description section found");

    const observerArticleDescription = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          articleDescription.classList.add("scrolled");
          console.log("Scrolled class added to article-description");
        } else {
          articleDescription.classList.remove("scrolled");
          console.log("Scrolled class removed from article-description");
        }
      });
    }, {
      threshold: 0.5
    });

    observerArticleDescription.observe(articleDescription);
    console.log("Intersection Observer added for article-description");
  } else {
    console.log("Article description section NOT found");
  }

    // 추가된 섹션: best-description-img에 대한 Observer
    const bestDescriptionImg = document.querySelector(".best-description-img");
  if (bestDescriptionImg) {
    console.log("Best description image section found");

    const observerBestDescriptionImg = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          bestDescriptionImg.classList.add("scrolled");
          console.log("Scrolled class added to best-description-img");
        } else {
          bestDescriptionImg.classList.remove("scrolled");
          console.log("Scrolled class removed from best-description-img");
        }
      });
    }, {
      threshold: 0.5
    });

    observerBestDescriptionImg.observe(bestDescriptionImg);
    console.log("Intersection Observer added for best-description-img");
  } else {
    console.log("Best description image section NOT found");
  }

  // 추가된 섹션: best-description에 대한 Observer
  const bestDescription = document.querySelector(".best-description");
  if (bestDescription) {
    console.log("Best description section found");

    const observerBestDescription = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          bestDescription.classList.add("scrolled");
          console.log("Scrolled class added to best-description");
        } else {
          bestDescription.classList.remove("scrolled");
          console.log("Scrolled class removed from best-description");
        }
      });
    }, {
      threshold: 0.5
    });

    observerBestDescription.observe(bestDescription);
    console.log("Intersection Observer added for best-description");
  } else {
    console.log("Best description section NOT found");
  }
});



</script>


<style scoped>
/* Introduce 섹션 스타일 */
.introduce {
  background-image: url('/pictures/소개.jpg'); /* 배경 이미지 */
  background-size: cover; /* 배경 이미지 크기 조정 */
  background-position: center; /* 배경 이미지 위치 */
  height: 500px; /* 높이 설정 */
  width: 100%; /* 너비 설정 */
  display: flex; /* Flexbox 사용 */
  justify-content: center; /* 텍스트 가로 중앙 정렬 */
  align-items: center; /* 텍스트 세로 중앙 정렬 */
  color: white; /* 텍스트 색상 */
  font-size: 4rem; /* 텍스트 크기 */
  font-weight: bold; /* 텍스트 굵게 */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7); /* 텍스트 그림자 */
  text-align: center; /* 텍스트 중앙 정렬 */
  opacity: 0; /* 초기 상태: 투명 */
  transform: translateY(50px); /* 아래쪽 위치 */
  transition: opacity 0.8s ease-out, transform 0.8s ease-out; /* 부드러운 전환 */
  margin-bottom: 150px;
}

/* Introduce 섹션이 화면에 등장했을 때 */
.introduce.scrolled {
  opacity: 1; /* 완전히 표시 */
  transform: translateY(0); /* 원래 위치로 이동 */
}

.intro-description {
  font-family: 'Noto Sans KR', sans-serif; /* Noto Sans KR 폰트 사용 */
  text-align: center;
  margin-top: 3rem;
  padding: 2rem 1rem;
  background-color: #ffffff;
  border-radius: 10px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  margin-bottom: 150px;
}

.intro-description.scrolled {
  opacity: 1;
  transform: translateY(0);
}

.intro-description .title {
  font-weight: 700;
  font-size: 2.5rem;
}

.intro-budget-image {
  width: 550px; /* 이미지의 너비를 설정 */
  margin: 20px auto; /* 수직 중앙 정렬, 여백 추가 */
  text-align: center; /* 이미지 중앙 정렬 */
  margin-bottom: 150px;
  opacity: 0; /* 초기 상태: 투명 */
  transform: translateY(50px); /* 아래쪽 위치 */
  transition: opacity 0.8s ease-out, transform 0.8s ease-out; /* 부드러운 전환 */
}

.intro-budget-image.scrolled {
  opacity: 1; /* 완전히 표시 */
  transform: translateY(0); /* 원래 위치로 이동 */
}

.intro-budget-image img {
  width: 100%; /* 부모 div에 맞춰 이미지 너비 조정 */
  height: 600px; /* 높이는 자동 조정 */
  display: block; /* 이미지 아래 공백 제거 */
  border-radius: 0; /* 모서리를 네모나게 설정 */
  box-shadow: none; /* 그림자 제거 */
}


.list-description {
  font-family: 'Noto Sans KR', sans-serif; /* Noto Sans KR 폰트 사용 */
  text-align: center;
  margin-top: 3rem;
  padding: 2rem 1rem;
  background-color: #ffffff;
  border-radius: 10px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  margin-bottom: 150px;
}

.list-description.scrolled {
  opacity: 1;
  transform: translateY(0);
}

.list-description .title {
  font-weight: 700;
  font-size: 2.5rem;
}

/* 부 타이틀 스타일 */
.list-description .subtitle {
  font-size: 1.2rem; /* 부 타이틀 글씨 크기 */
  color: #666; /* 회색으로 색상 변경 */
  font-weight: 400; /* 기본 굵기로 설정 */
  margin-top: 10px; /* 위쪽 여백 추가 */
  line-height: 1.5; /* 줄 간격 조절 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

.product-description-img {
  width: 550px; /* 이미지의 너비를 설정 */
  margin: 20px auto; /* 수직 중앙 정렬, 여백 추가 */
  text-align: center; /* 이미지 중앙 정렬 */
  margin-bottom: 150px;
  opacity: 0; /* 초기 상태: 투명 */
  transform: translateY(50px); /* 아래쪽 위치 */
  transition: opacity 0.8s ease-out, transform 0.8s ease-out; /* 부드러운 전환 */
}

.product-description-img.scrolled {
  opacity: 1; /* 완전히 표시 */
  transform: translateY(0); /* 원래 위치로 이동 */
}

.product-description-img img {
  width: 100%; /* 부모 div에 맞춰 이미지 너비 조정 */
  height: 600px; /* 높이는 자동 조정 */
  display: block; /* 이미지 아래 공백 제거 */
  border-radius: 0; /* 모서리를 네모나게 설정 */
  box-shadow: none; /* 그림자 제거 */
}

.product-description {
  font-family: 'Noto Sans KR', sans-serif; /* Noto Sans KR 폰트 사용 */
  text-align: center;
  margin-top: 3rem;
  padding: 2rem 1rem;
  background-color: #ffffff;
  border-radius: 10px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  margin-bottom: 150px;
}

.product-description.scrolled {
  opacity: 1;
  transform: translateY(0);
}

.product-description .title {
  font-weight: 700;
  font-size: 2.5rem;
}

/* 부 타이틀 스타일 */
.product-description .subtitle {
  font-size: 1.2rem; /* 부 타이틀 글씨 크기 */
  color: #666; /* 회색으로 색상 변경 */
  font-weight: 400; /* 기본 굵기로 설정 */
  margin-top: 10px; /* 위쪽 여백 추가 */
  line-height: 1.5; /* 줄 간격 조절 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

h2 {
  font-family: 'Noto Sans KR', sans-serif; /* Noto Sans KR 폰트 사용 */
  font-size: 2.5rem; /* 더 큰 텍스트 크기 */
  font-weight: 700; /* 두꺼운 텍스트 */
  text-align: center;
  color: black; /* 텍스트 색상 */
  margin-top: 2rem;
  padding: 1rem 0;
}

.article-description-img {
  width: 550px; /* 이미지의 너비를 설정 */
  margin: 20px auto; /* 수직 중앙 정렬, 여백 추가 */
  text-align: center; /* 이미지 중앙 정렬 */
  margin-top: 150px;
  margin-bottom: 150px;
  opacity: 0; /* 초기 상태: 투명 */
  transform: translateY(50px); /* 아래쪽 위치 */
  transition: opacity 0.8s ease-out, transform 0.8s ease-out; /* 부드러운 전환 */
}

.article-description-img.scrolled {
  opacity: 1; /* 완전히 표시 */
  transform: translateY(0); /* 원래 위치로 이동 */
}

.article-description-img img {
  width: 100%; /* 부모 div에 맞춰 이미지 너비 조정 */
  height: 600px; /* 높이는 자동 조정 */
  display: block; /* 이미지 아래 공백 제거 */
  border-radius: 0; /* 모서리를 네모나게 설정 */
  box-shadow: none; /* 그림자 제거 */
}

.article-description {
  font-family: 'Noto Sans KR', sans-serif; /* Noto Sans KR 폰트 사용 */
  text-align: center;
  margin-top: 3rem;
  padding: 2rem 1rem;
  background-color: #ffffff;
  border-radius: 10px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  margin-bottom: 100px;
}

.article-description.scrolled {
  opacity: 1;
  transform: translateY(0);
}

.article-description .title {
  font-weight: 700;
  font-size: 2.5rem;
}

/* 부 타이틀 스타일 */
.article-description .subtitle {
  font-size: 1.2rem; /* 부 타이틀 글씨 크기 */
  color: #666; /* 회색으로 색상 변경 */
  font-weight: 400; /* 기본 굵기로 설정 */
  margin-top: 10px; /* 위쪽 여백 추가 */
  line-height: 1.5; /* 줄 간격 조절 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

.best-description-img {
  width: 550px; /* 이미지의 너비를 설정 */
  margin: 20px auto; /* 수직 중앙 정렬, 여백 추가 */
  text-align: center; /* 이미지 중앙 정렬 */
  margin-top: 150px;
  margin-bottom: 150px;
  opacity: 0; /* 초기 상태: 투명 */
  transform: translateY(50px); /* 아래쪽 위치 */
  transition: opacity 0.8s ease-out, transform 0.8s ease-out; /* 부드러운 전환 */
}

.best-description-img.scrolled {
  opacity: 1; /* 완전히 표시 */
  transform: translateY(0); /* 원래 위치로 이동 */
}

.best-description-img img {
  width: 100%; /* 부모 div에 맞춰 이미지 너비 조정 */
  height: 600px; /* 높이는 자동 조정 */
  display: block; /* 이미지 아래 공백 제거 */
  border-radius: 0; /* 모서리를 네모나게 설정 */
  box-shadow: none; /* 그림자 제거 */
}

.best-description{
  font-family: 'Noto Sans KR', sans-serif; /* Noto Sans KR 폰트 사용 */
  text-align: center;
  margin-top: 3rem;
  padding: 2rem 1rem;
  background-color: #ffffff;
  border-radius: 10px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  margin-bottom: 100px;
}

.best-description.scrolled {
  opacity: 1;
  transform: translateY(0);
}

.best-description .title {
  font-weight: 700;
  font-size: 2.5rem;
}

/* 부 타이틀 스타일 */
.best-description .subtitle {
  font-size: 1.2rem; /* 부 타이틀 글씨 크기 */
  color: #666; /* 회색으로 색상 변경 */
  font-weight: 400; /* 기본 굵기로 설정 */
  margin-top: 10px; /* 위쪽 여백 추가 */
  line-height: 1.5; /* 줄 간격 조절 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

/* Jumbotron 스타일 */
.jumbotron {
  height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("/pictures/배경화면2.jpg");
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin-bottom: 200px;
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

/* 페이지 전체 배경 */
body {
  background: linear-gradient(to bottom, #f7f7f7, #e9ecef);
  font-family: 'Noto Sans KR', sans-serif;
  color: #ffffff
}

/* Product Section */
.product-section {
  padding: 3rem 0;
  background: linear-gradient(to bottom, #ffffff, #f7f7f7);
  border: 1px solid #ddd;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  animation: fadeIn 1s ease-in-out;
}

/* 섹션 제목 스타일 */
.section-title {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #343a40;
  margin-bottom: 2rem;
  position: relative;
}

.menu {
  padding-top: 100px;
}

.menu button {
  font-size: 1rem;
  padding: 1rem;
  border-radius: 5px;
  border: none;
  transition: all 0.3s ease-in-out;
}

.menu button:hover {
  transform: scale(1.05);
  background-color: lightgray;
  color: #fff;
}

.menu button:active {
  transform: scale(0.95);
  background-color: #e9ecef;
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


/* 베스트 상품 섹션 */
.top-liked-products {
  background-color: #f9f9f9;
  padding: 3rem 0;
}

#best-products {
  max-width: 1200px;
  margin: 0 auto;
}

/* 카드 스타일 */
.product-card {
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* 상품 유형 스타일 */
#title-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* 상품명 스타일 */
.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 0.5rem;
  text-align: center;
}

.card-body {
  padding: 1.5rem;
  text-align: center;
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

/* 회사명 스타일 */
.card-text {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 0.8rem;
}

/* 좋아요 스타일 */
.card-text strong {
  font-size: 1.2rem;
  color: #ff6b6b;
}

/* 컴포넌트 전용 스타일 */
.CreditLoanDiscussionView,
.JeonseDiscussionView,
.MortgageDiscussionView {
  margin-top: 1rem;
}

/* 메시지 없을 때 스타일 */
.text-muted {
  font-size: 1.2rem;
  color: #6c757d;
}

/* 카드의 애니메이션 효과 */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.product-card {
  animation: fadeInUp 1s ease-in-out;
}

/* 베스트 게시글 섹션 */
.top-liked-article {
  background-color: #f8f9fa; /* 배경색 */
  padding: 3rem 0; /* 위아래 패딩 */
}

.article-card {
  max-width: 600px; /* 카드 최대 너비 */
  border: 1px solid #eaeaea; /* 경계선 */
  border-radius: 15px; /* 부드러운 모서리 */
  background-color: #ffffff; /* 카드 배경 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  padding: 2rem; /* 내부 패딩 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 애니메이션 */
}

.article-card:hover {
  transform: translateY(-5px); /* 살짝 떠오르는 효과 */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); /* 강조된 그림자 */
}

.article-title {
  font-family: 'Noto Sans KR', sans-serif; /* 폰트 변경 */
  font-size: 1.8rem; /* 글씨 크기 */
  font-weight: 700; /* 두께 */
  color: #495057; /* 텍스트 색상 */
  text-align: center; /* 중앙 정렬 */
  margin-bottom: 1rem; /* 아래 여백 */
}

.article-content {
  font-family: 'Roboto', sans-serif; /* 콘텐츠용 폰트 */
  font-size: 1.2rem; /* 글씨 크기 */
  color: #6c757d; /* 회색 톤 */
  text-align: left; /* 좌측 정렬 */
  line-height: 1.6; /* 줄 간격 */
  margin-bottom: 2rem; /* 아래 여백 */
}

.article-likes {
  font-family: 'Noto Sans KR', sans-serif; /* 좋아요 텍스트 폰트 */
  font-size: 1.1rem; /* 글씨 크기 */
  color: #495057; /* 기본 텍스트 색상 */
  text-align: right; /* 우측 정렬 */
  font-weight: bold; /* 두껍게 */
  margin-bottom: 1.5rem; /* 아래 여백 */
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
  color: #495057;
  text-decoration: none;
  transition: color 0.3s ease-in-out;
}

.product-name:hover {
  color: #ff6b6b;
}

/* 푸터 스타일 */
.footer {
  background: #f1f3f5;
  text-align: center;
  padding: 20px 0;
  font-size: 0.9rem;
  color: #333;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.footer a {
  color: #007bff; /* 링크 색상 */
  text-decoration: none; /* 밑줄 제거 */
}

.footer a:hover {
  text-decoration: underline; /* 링크 호버 시 밑줄 */
}

/* ===== 애니메이션 효과 추가 ===== */

/* 섹션 등장 애니메이션 */
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

/* 버튼 클릭 효과 */
@keyframes buttonClickEffect {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

/* ===== 적용 ===== */

/* 섹션 전체에 슬라이드 애니메이션 */
#product-section {
  animation: slideInFromBottom 1s ease-in-out;
}

/* 버튼 클릭 애니메이션 */
.menu button {
  transition: transform 0.3s ease-in-out;
}

.menu button:active {
  animation: buttonClickEffect 0.3s ease-in-out;
}

/* 시작하기 버튼 스타일 */
.lightbutton h2 {
  color: white; /* 글씨 색상 흰색 */
  font-size: 2rem; /* 기본 글씨 크기 */
  font-weight: bold;
  text-align: center;
  cursor: pointer; /* 클릭 가능한 커서 */
  transition: transform 0.3s ease, color 0.3s ease; /* 부드러운 애니메이션 효과 */
}

.lightbutton h2:hover {
  transform: scale(1.2); /* 크기 10% 증가 */
  color: white; /* 호버 시 글씨 색상 변경 (금색) */
}
</style>
