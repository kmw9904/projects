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

    <!-- 챗봇 아이콘 및 채팅창 -->
    <div class="chatbot-container">
      <!-- 챗봇 아이콘 -->
      <button class="chatbot-icon" @click="toggleChatBot">
        <img src="/pictures/챗봇사진.png" alt="챗봇" />
      </button>
      <div v-if="isChatBotVisible" class="navigation-buttons">
        <AlgorithmView />
      </div>
    </div>

    <div class="list-container">
      <button class="chatbot-icon" @click="toggleMoveClone">
        <img src="/pictures/움직이기클론.png" alt="이동" />
      </button>
      <!-- 네비게이션 버튼들 -->
      <div v-if="isMoveCloneVisible" class="navigation-scroll-buttons">
        <button class="btn btn-link" @click="scrollToSection('top')">최상단</button>
        <button class="btn btn-link" @click="scrollToSection('product-section')">상품 조회</button>
        <button class="btn btn-link" @click="scrollToSection('best-products')">베스트 상품</button>
        <button class="btn btn-link" @click="scrollToSection('top-article')">베스트 게시글</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { ref } from "vue";
import { useBankStore } from "@/stores/bank";
import AlgorithmView from "./algorithm/AlgorithmView.vue";

// 상태 관리
const store = useBankStore();
const Logout = function () {
  store.Logout();
};

// 챗봇 상태 관리
const isChatBotVisible = ref(false);
const toggleChatBot = () => {
  isChatBotVisible.value = !isChatBotVisible.value;
};

// 움직이기 클론 상태 관리
const isMoveCloneVisible = ref(false);
const toggleMoveClone = () => {
  isMoveCloneVisible.value = !isMoveCloneVisible.value;
};

// 특정 섹션으로 부드럽게 스크롤하는 함수
const scrollToSection = (sectionId) => {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
};
</script>

<style scoped>
/* 전체 앱 영역 */
.app {
  font-family: "Noto Sans KR", sans-serif;
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
  font-family: "Noto Sans KR", sans-serif;
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

/* 챗봇 컨테이너 */
.chatbot-container {
  position: fixed;
  bottom: 70px; /* 화면 하단 */
  right: 100px; /* 화면 오른쪽 */
  z-index: 1100; /* 다른 콘텐츠 위에 표시 */
}

/* 리스트 컨테이너 */
.list-container {
  position: fixed;
  bottom: 150px; /* 화면 하단 */
  right: 100px; /* 화면 오른쪽 */
  z-index: 1000; /* 다른 콘텐츠 위에 표시 */
}

/* 챗봇 아이콘 */
.chatbot-icon {
  background-color: transparent; /* 배경 투명 */
  border: none; /* 테두리 제거 */
  border-radius: 50%;
  width: 70px; /* 크기 증가 */
  height: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  outline: none;
}

/* 아이콘 이미지 */
.chatbot-icon img {
  width: 100%; /* 크기를 아이콘 전체에 맞춤 */
  height: 100%;
  object-fit: contain; /* 이미지를 비율에 맞게 조정 */
}

/* 네비게이션 버튼들 */
.navigation-buttons {
  position: fixed;
  bottom: 145px; /* 버튼 위로 띄우기 */
  right: 37px;
  background-color: #ffffff;
  border: 2px solid #000000;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.navigation-scroll-buttons {
  position: fixed;
  bottom: 230px; /* 버튼 위로 띄우기 */
  right: 60px;
  background-color: #ffffff;
  border: 2px solid #000000;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

/* 스크롤 네비게이션 버튼 스타일 */
.navigation-scroll-buttons button {
  display: block;
  width: 100%;
  margin-bottom: 10px; /* 버튼 간 간격 */
  text-align: left;
  background: none; /* 배경 제거 */
  border: none; /* 테두리 제거 */
  color: #333; /* 텍스트 색상 (기본 색상으로 설정) */
  font-size: 16px; /* 글씨 크기 */
  font-weight: bold; /* 글씨 굵게 */
  cursor: pointer;
  padding: 5px 10px; /* 여백 추가 */
  transition: all 0.2s ease-in-out; /* 부드러운 호버 효과 */
  text-decoration: none; /* 밑줄 제거 */
}

.navigation-scroll-buttons button:hover {
  background-color: #f1f1f1; /* 호버 시 배경색 변경 */
  border-radius: 5px; /* 약간의 둥근 모서리 */
  color: #000; /* 호버 시 글씨 색상 유지 */
}

.navigation-buttons button:hover {
  text-decoration: underline;
}

/* 채팅창 */
.chatbot {
  position: fixed;
  bottom: 145px; /* 버튼 위로 띄우기 */
  right: 37px;
  width: 400px; /* 크기 증가 */
  height: 450px;
  background-color: #ffffff; /* 흰색 배경 */
  border: 2px solid #000000; /* 검은 테두리 */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* iframe 스타일 */
.chatbot-iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>
