<template>
  <div class="signup-container">
    <h1 class="signup-title text-center mb-4">Sign Up</h1>
    <form @submit.prevent="SignUp" class="signup-form card shadow-sm p-4">
      <!-- Username -->
      <div class="form-group mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" id="username" class="form-control" v-model="username" placeholder="Enter your username" />
      </div>

      <!-- Name -->
      <div class="form-group mb-3">
        <label for="name" class="form-label">Name</label>
        <input type="text" id="name" class="form-control" v-model="name" placeholder="Enter your name" />
      </div>

      <!-- Email -->
      <div class="form-group mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" id="email" class="form-control" v-model="email" placeholder="Enter your email" />
      </div>

      <!-- Password -->
      <div class="form-group mb-3">
        <label for="password1" class="form-label">Password</label>
        <input type="password" id="password1" class="form-control" v-model="password1" placeholder="Enter your password" />
      </div>

      <!-- Confirm Password -->
      <div class="form-group mb-3">
        <label for="password2" class="form-label">Confirm Password</label>
        <input type="password" id="password2" class="form-control" v-model="password2" placeholder="Confirm your password" />
      </div>

      <!-- Preferred Banks -->
      <div class="form-group mb-3">
        <label class="form-label">선호 은행</label>
        <div v-for="bank in banks" :key="bank.company_id" class="form-check">
          <input type="checkbox" :value="bank.company_id" v-model="selectedBanks" class="form-check-input" :id="'bank_' + bank.company_id" />
          <label :for="'bank_' + bank.company_id" class="form-check-label">
            {{ bank.company_name }}
          </label>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="text-center">
        <input type="submit" value="Sign Up" class="btn btn-secondary w-100" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useBankStore } from "@/stores/bank";

const username = ref(null);
const name = ref(null); // 추가된 name 필드
const email = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const banks = ref([]); // 은행 목록 저장
const selectedBanks = ref([]); // 선택된 은행 ID 저장

const store = useBankStore();

onMounted(() => {
  // 회원가입 페이지에서 은행 데이터를 미리 가져옵니다.
  store
    .getBanks()
    .then((response) => {
      console.log("받은 은행 데이터:", response);
      banks.value = response;
    })
    .catch((error) => {
      console.error("은행 목록 로드 실패:", error);
    });
});

// 회원가입 요청
const SignUp = function () {
  // 은행 목록이 로드된 후에만 회원가입 진행
  if (banks.value.length === 0) {
    console.warn("은행 목록을 먼저 불러오세요.");
    return;
  }

  const payload = {
    username: username.value,
    name: name.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    preferred_banks: [...selectedBanks.value],
  };
  store.SignUp(payload);
};
</script>

<style scoped>
.signup-container {
  font-family: "Noto Sans KR", sans-serif;
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.signup-title {
  font-size: 2rem;
  font-weight: bold;
  color: gray;
}

.signup-form {
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

.form-check-input {
  margin-right: 10px;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 10px 20px;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
