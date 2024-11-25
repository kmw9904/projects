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
        <div class="preferred-banks-list row mt-3">
          <div v-for="bank in profile.profile_user.preferred_banks" :key="bank.id" class="col-lg-4 col-md-6 col-12 mb-3">
            <div class="bank-card text-center p-2">
              <div class="bank-img">
                <img :src="`/pictures/${bank.company_name}.png`" alt="선호 은행 이미지" />
              </div>
              <p class="mt-2">{{ bank.company_name }}</p>
            </div>
          </div>
        </div>
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
/* 프로필 컨테이너 스타일 */
.profile-container {
  padding: 20px;
  max-width: 800px; /* 전체 컨테이너 크기 조정 */
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 15px; /* 모서리를 조금 더 둥글게 */
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1); /* 그림자 강조 */
}

/* 프로필 제목 스타일 */
.profile-title {
  font-size: 2rem;
  font-weight: bold;
  color: #555;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* 텍스트 그림자 */
}

/* 프로필 상세 정보 */
.profile-details {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* 은은한 그림자 */
}

/* 선호 은행 리스트 스타일 */
.preferred-banks-list {
  display: flex;
  flex-wrap: wrap; /* 줄바꿈 허용 */
  gap: 10px; /* 카드 간격 줄임 */
  margin-top: 15px;
  justify-content: center; /* 카드들을 가운데 정렬 */
}

/* 카드 스타일 */
.bank-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 8px; /* 카드 크기 줄이기 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.bank-card:hover {
  transform: translateY(-5px); /* 호버 시 살짝 떠오르는 효과 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 호버 시 그림자 강조 */
}

/* 은행 이미지 */
.bank-img img {
  width: 60px; /* 이미지 크기 줄이기 */
  height: 60px;
  object-fit: contain; /* 비율 유지하며 축소 */
  margin-bottom: 10px;
  border-radius: 50%; /* 동그랗게 */
  border: 1px solid #eee; /* 이미지 테두리 */
}

/* 은행 이름 스타일 */
.bank-card p {
  font-size: 0.8rem; /* 글씨 크기 줄이기 */
  font-weight: bold;
  color: #333;
  margin: 0;
  text-align: center;
}

/* 공통 버튼 스타일 */
.btn-primary {
  display: inline-block;
  margin-top: 15px;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 0.95rem;
  border-radius: 20px;
  transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.btn-primary:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 */
}

/* 링크 스타일 */
.btn-link {
  font-size: 0.9rem;
  color: #007bff;
  text-decoration: none;
  margin-left: 10px;
}

.btn-link:hover {
  text-decoration: underline;
}

/* 반응형 스타일 */
@media (min-width: 992px) {
  /* 큰 화면에서 한 줄에 3개 */
  .col-lg-4 {
    flex: 0 0 30%; /* 한 줄에 3개로 조정 */
    max-width: 30%;
  }
}

@media (min-width: 768px) and (max-width: 991px) {
  /* 중간 화면에서 한 줄에 2개 */
  .col-md-6 {
    flex: 0 0 45%;
    max-width: 45%;
  }
}

@media (max-width: 767px) {
  /* 작은 화면에서 한 줄에 1개 */
  .col-12 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>
