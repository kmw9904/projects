<template>
  <div>
    <h1>프로필</h1>
    <div v-if="profile">
      <p>ID : {{ profile.profile_user.username }}</p>
      <p>PASSWORD</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useBankStore } from "@/stores/bank";
const profile = ref(null);
const store = useBankStore();

onMounted(() => {
  store.getUserProfile();
  profile.value = store.profile;
});
</script>

<style scoped></style>
