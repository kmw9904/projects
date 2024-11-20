<template>
  <div>
    <h2>비밀번호 변경</h2>
    <form @submit.prevent="changePasswordHandler">
      <label for="old-password">현재 비밀번호</label>
      <input type="password" id="old-password" v-model="oldPassword" required />
      <br />
      <label for="new-password">새 비밀번호</label>
      <input type="password" id="new-password" v-model="newPassword1" required />
      <br />

      <label for="new-password-confirm">새 비밀번호 확인</label>
      <input type="password" id="new-password-confirm" v-model="newPassword2" required />
      <br />

      <button type="submit">비밀번호 변경</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useBankStore } from "@/stores/bank";

const oldPassword = ref("");
const newPassword1 = ref("");
const newPassword2 = ref("");

const store = useBankStore();

const changePasswordHandler = () => {
  const payload = {
    oldPassword: oldPassword.value,
    newPassword1: newPassword1.value,
    newPassword2: newPassword2.value,
  };

  store
    .changePassword(payload)
    .then(() => {
      alert("비밀번호가 성공적으로 변경되었습니다!");
      oldPassword.value = ""; // 입력값 초기화
      newPassword1.value = "";
      newPassword2.value = "";
    })
    .catch((error) => {
      console.error("비밀번호 변경 실패:", error.response?.data || error.message);
      alert("비밀번호 변경 중 오류가 발생했습니다.");
    });
};
</script>

<style scoped></style>
