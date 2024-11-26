<template>
  <div class="login-container">
    <h1 class="login-title text-center mb-4">Login Page</h1>
    <form @submit.prevent="Login" class="login-form card shadow-sm p-4">
      <!-- Username -->
      <div class="form-group mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" id="username" v-model="username" class="form-control" placeholder="Enter your username" />
      </div>

      <!-- Password -->
      <div class="form-group mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" placeholder="Enter your password" />
      </div>

      <!-- Submit Button -->
      <div class="text-center">
        <input type="submit" value="Login" class="btn btn-secondary w-100" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useBankStore } from "@/stores/bank";

const username = ref(null);
const password = ref(null);
const store = useBankStore();

const Login = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.Login(payload);
};
</script>

<style scoped>
.login-container {
  font-family: "Noto Sans KR", sans-serif;
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  color: gray;
}

.login-form {
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
  color: white;
  border: none;
  padding: 10px 20px;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
