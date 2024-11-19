<template>
  <div>
    <h1>SignUp Page</h1>
    <form @submit.prevent="SignUp">
      <label for="username">Username</label>
      :
      <input type="text" id="username" v-model="username" />
      <br />

      <label for="name">Name</label>
      :
      <input type="text" id="name" v-model="name" />
      <br />

      <label for="email">Email</label>
      :
      <input type="email" id="email" v-model="email" />
      <br />

      <label for="password1">Password</label>
      :
      <input type="password" id="password1" v-model="password1" />
      <br />

      <label for="password2">Confirm Password</label>
      :
      <input type="password" id="password2" v-model="password2" />
      <br />

      <label>선호 은행</label>
      <br />
      <div v-for="bank in banks" :key="bank.company_id">
        <input type="checkbox" :value="bank.company_id" v-model="selectedBanks" />
        {{ bank.company_name }}
      </div>

      <input type="submit" value="Sign Up" />
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
  store.getBanks()
    .then((response) => {
      console.log("받은 데이터:", response); // 데이터가 제대로 왔는지 확인
      banks.value = response; // banks 변수 업데이트
    })
    .catch((error) => {
      console.error("은행 데이터 로드 실패:", error);
    });
});

// 회원가입 요청
const SignUp = function () {
  const payload = {
    username: username.value,
    name: name.value, // name 필드를 포함
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    preferred_banks: selectedBanks.value,
  };
  store.SignUp(payload);
};
</script>

<style scoped></style>
