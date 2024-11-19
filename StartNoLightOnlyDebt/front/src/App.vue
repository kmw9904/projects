<template>
  <header>
    <div>
      <template v-if="store.isLoggedIn">
        <button @click="Logout">로그아웃</button>
        |
        <RouterLink :to="{ name: 'AccountView' }">프로필</RouterLink>
        |
        <RouterLink :to="{ name: 'MainView' }">홈</RouterLink>
        |
        <RouterLink :to="{ name: 'map' }">은행찾기</RouterLink>
        |
        <RouterLink :to="{ name: 'ExchangeView' }">환율</RouterLink>
      </template>
      <template v-else>
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
        |
        <RouterLink :to="{ name: 'LoginView' }">로그인</RouterLink>
        |
        <RouterLink :to="{ name: 'MainView' }">홈</RouterLink>
        |
        <RouterLink :to="{ name: 'article' }" v-if="storecommunity.isLogin">커뮤니티</RouterLink>
      </template>
    </div>
    <div>
      <RouterLink :to="{ name: 'AlgorithmView' }">chatbot</RouterLink>
    </div>
    <RouterView />
  </header>
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { useBankStore } from "@/stores/bank";
import { useCommunityStore } from "@/stores/community";

const store = useBankStore();
const storecommunity = useCommunityStore();

const Logout = function () {
  store.Logout();
};
</script>

<style scoped></style>
