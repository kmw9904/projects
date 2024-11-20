<template>
  <div>
    <h1>프로필</h1>
    <div v-if="profile">
      <p>이름 : {{ profile.profile_user.name }}</p>
      <p>ID : {{ profile.profile_user.username }}</p>
      <p>PASSWORD : {{ profile.profile_user.password }}</p>
      <RouterLink :to="{ name: 'PasswordChangeView' }">비밀번호 변경</RouterLink>
      <p>Email : {{ profile.profile_user.email }}</p>
      <hr />
      <div>
        <strong>선호 은행</strong>
        <div v-for="bank in profile.profile_user.preferred_banks" :key="bank.id">
          <p>{{ bank.company_name }}</p>
        </div>
        <RouterLink :to="{ name: 'PreferredBanksView' }">수정</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useBankStore } from "@/stores/bank";

const store = useBankStore();
const profile = ref(null);

onMounted(() => {
  store.getUserProfile(); // 항상 최신 데이터를 가져오도록 설정
  profile.value = store.profile;
});
</script>

<style scoped></style>
