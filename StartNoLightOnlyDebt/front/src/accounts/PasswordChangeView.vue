<template>
  <div class="password-change-container">
    <h2 class="text-center mb-4">비밀번호 변경</h2>
    <form @submit.prevent="changePasswordHandler" class="password-change-form card shadow-sm p-4">
      <!-- 현재 비밀번호 -->
      <div class="form-group mb-3">
        <label for="old-password" class="form-label">현재 비밀번호</label>
        <input type="password" id="old-password" v-model="oldPassword" class="form-control" placeholder="Enter your current password" required />
      </div>

      <!-- 새 비밀번호 -->
      <div class="form-group mb-3">
        <label for="new-password" class="form-label">새 비밀번호</label>
        <input type="password" id="new-password" v-model="newPassword1" class="form-control" placeholder="Enter your new password" required />
      </div>

      <!-- 새 비밀번호 확인 -->
      <div class="form-group mb-3">
        <label for="new-password-confirm" class="form-label">새 비밀번호 확인</label>
        <input type="password" id="new-password-confirm" v-model="newPassword2" class="form-control" placeholder="Confirm your new password" required />
      </div>

      <!-- 제출 버튼 -->
      <div class="text-center">
        <button type="submit" class="btn btn-secondary w-100">비밀번호 변경</button>
      </div>
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

<style scoped>
.password-change-container {
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.password-change-form {
  background-color: #ffffff;
  border-radius: 10px;
}

.form-label {
  font-weight: bold;
}

.form-control {
  padding: 10px;
  border-radius: 5px;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
