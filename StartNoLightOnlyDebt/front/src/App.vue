<template>
  <div class="app">
    <!-- 헤더 -->
    <header class="header">
      <div class="container d-flex justify-content-between align-items-center">
        <!-- 로고 -->
        <div class="logo">
          <a href="/" class="logo-link">
            <h1 class="logo-text fw-bold">
              Start
              <br />
              No Light
              <br />
              Only Debt
            </h1>
          </a>
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
                <RouterLink class="dropdown-item" :to="{ name: 'map' }">
                  <p class="menu-name">
                    <img src="/public/pictures/은행찾기.png" alt="은행찾기" />
                    은행찾기
                  </p>
                </RouterLink>
                <RouterLink class="dropdown-item" :to="{ name: 'ExchangeView' }">
                  <p class="menu-name">
                    <img src="/public/pictures/환율.png" alt="환율" />
                    환율
                  </p>
                </RouterLink>
                <RouterLink class="dropdown-item" :to="{ name: 'article' }">
                  <p class="menu-name">
                    <img src="/public/pictures/커뮤니티.png" alt="커뮤니티" />
                    커뮤니티
                  </p>
                </RouterLink>
                <RouterLink class="dropdown-item" :to="{ name: 'AlgorithmView' }">chatbot</RouterLink>
              </nav>
            </div>
          </template>
          <!-- 비로그인 상태 -->
          <template v-else>
            <RouterLink class="btn btn-outline-dark" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
            <RouterLink class="btn btn-outline-dark" :to="{ name: 'LoginView' }">로그인</RouterLink>
            <RouterLink :to="{ name: 'MainView' }">
              <img src="/public/pictures/홈버튼.png" alt="홈버튼" />
            </RouterLink>
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

.logo-link {
  color: black; /* 링크 텍스트를 검은색으로 설정 */
  text-decoration: none; /* 밑줄 제거 */
}

.logo-link:hover {
  color: black; /* 호버 시에도 검은색 유지 */
  text-decoration: none; /* 호버 시에도 밑줄 제거 */
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

.menu-name {
  font-size: 20px;
  font-weight: bold;
}
</style>
