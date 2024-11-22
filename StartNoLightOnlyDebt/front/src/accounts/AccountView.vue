<template>
  <div class="profile-container">
    <h1 class="profile-title text-center mb-4">프로필</h1>
    <div v-if="profile" class="profile-details card shadow-sm p-4">
      <!-- 사용자 정보 -->
      <div class="mb-4">
        <p>
          <strong>이름:</strong>
          {{ profile.profile_user.name }}
        </p>
        <p>
          <strong>ID:</strong>
          {{ profile.profile_user.username }}
        </p>
        <p>
          <strong>Password:</strong>
          {{ profile.profile_user.password }}
          <RouterLink :to="{ name: 'PasswordChangeView' }" class="btn btn-link p-0">비밀번호 변경</RouterLink>
        </p>
        <p>
          <strong>Email:</strong>
          {{ profile.profile_user.email }}
        </p>
      </div>
      <hr />
      <!-- 선호 은행 -->
      <div>
        <strong>선호 은행</strong>
        <ul class="preferred-banks-list list-group mt-3">
          <li v-for="bank in profile.profile_user.preferred_banks" :key="bank.id" class="list-group-item">
            <div class="bank-img">
              <img :src="`/pictures/${bank.company_name}.png`" alt="선호 은행 이미지" />
            </div>
            {{ bank.company_name }}
          </li>
        </ul>
        <RouterLink :to="{ name: 'PreferredBanksView' }" class="btn btn-primary mt-3">수정</RouterLink>
      </div>
    </div>
    <div v-else class="text-center text-muted">프로필 정보를 불러오는 중입니다...</div>
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

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-title {
  font-size: 2rem;
  font-weight: bold;
  color: gray;
}

.profile-details {
  background-color: #ffffff;
  border-radius: 10px;
}

.preferred-banks-list {
  margin-top: 15px;
}

.list-group-item {
  padding: 10px;
  font-size: 1rem;
}

.btn-link {
  font-size: 0.9rem;
  color: #007bff;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}

.btn-primary {
  display: inline-block;
  margin-top: 15px;
  background-color: #007bff;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.bank-img {
  width: 100px; /* 이미지 컨테이너의 너비 */
  height: 100px;
  flex-shrink: 0; /* 크기를 줄이지 않음 */
}

.bank-img img {
  width: 100px; /* 이미지 컨테이너의 너비 */
  height: 100px;
  object-fit: contain; /* 이미지가 비율에 맞게 축소되며 잘리지 않음 */
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
}
</style>
