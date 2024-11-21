<template>
  <div class="app">
    <!-- 헤더 -->
    <header class="header">
      <div class="container d-flex justify-content-between align-items-center">
        <!-- 로고 -->
        <div class="logo">
          <h1 class="logo-text fw-bold">
            Start
            <br />
            No Light
            <br />
            Only Debt
          </h1>
        </div>

        <!-- 네비게이션 -->
        <div class="navigation">
          <!-- 로그인 상태 -->
          <template v-if="store.isLoggedIn">
            <button @click="Logout" class="btn btn-outline-dark">로그아웃</button>
            <RouterLink :to="{ name: 'AccountView' }">
              <img src="/public/pictures/프로필.png" alt="프로필" />
            </RouterLink>
            <RouterLink :to="{ name: 'MainView' }">
              <img src="/public/pictures/홈버튼.png" alt="홈버튼" />
            </RouterLink>
            <div class="btn-group">
              <img class="btn dropdown-toggle" data-bs-toggle="dropdown" data-bs-display="static" aria-expanded="false" src="/public/pictures/토글이미지.png" alt="토글 메뉴" />
              <nav class="dropdown-menu dropdown-menu-end dropdown-menu-lg-start">
                <RouterLink class="dropdown-item" :to="{ name: 'map' }">은행찾기</RouterLink>
                |
                <RouterLink class="dropdown-item" :to="{ name: 'ExchangeView' }">환율</RouterLink>
                |
                <RouterLink class="dropdown-item" :to="{ name: 'article' }">커뮤니티</RouterLink>
                |
                <RouterLink class="dropdown-item" :to="{ name: 'AlgorithmView' }">chatbot</RouterLink>
              </nav>
            </div>
          </template>
          <!-- 비로그인 상태 -->
          <template v-else>
            <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
            |
            <RouterLink :to="{ name: 'LoginView' }">로그인</RouterLink>
            |
            <RouterLink :to="{ name: 'MainView' }">홈</RouterLink>
          </template>
        </div>
      </div>
    </header>

    <!-- 메인 콘텐츠 -->
    <main ref="mainContent">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { useBankStore } from "@/stores/bank";

const store = useBankStore();

const Logout = function () {
  store.Logout();
};
</script>

<style scoped>
/* 전체 앱 영역 */
.app {
  width: 100%;
  height: 100vh; /* 뷰포트 전체 높이 */
  display: flex;
  flex-direction: column; /* 헤더와 메인 콘텐츠를 세로로 배치 */
}

/* 헤더 스타일 */
.header {
  position: fixed; /* 상단 고정 */
  top: 0;
  left: 0;
  width: 100%; /* 화면 너비 100% */
  height: 63px; /* 헤더 높이 */
  background: #ffffff; /* 배경색 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  z-index: 1000; /* 위계 설정 */
  display: flex;
  align-items: center;
}

/* 로고 스타일 */
.logo {
  display: flex;
  align-items: center;
}

.logo-text {
  margin: 0;
  font-size: 1rem;
  line-height: 1.2;
}

/* 네비게이션 스타일 */
.navigation {
  display: flex;
  align-items: center;
  gap: 15px; /* 메뉴 간격 */
}

.nav-link {
  text-decoration: none;
  color: #000;
  font-weight: bold;
}

.nav-link:hover {
  color: #007bff;
}

/* 메인 콘텐츠 스타일 */
main {
  flex: 1; /* 헤더를 제외한 모든 공간 차지 */
  padding-top: 63px; /* 헤더 높이만큼 아래로 이동 */
  overflow-y: auto; /* 콘텐츠가 길어질 경우 스크롤 활성화 */
}
</style>
