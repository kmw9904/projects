<template>
  <div class="preferred-banks-container">
    <h1 class="text-center mb-4">선호 은행 수정</h1>
    <form @submit.prevent="updatePreferredBanks" class="preferred-banks-form card shadow-sm p-4">
      <div class="preferred-banks-list row">
        <div v-for="bank in banks" :key="bank.company_id" class="col-lg-4 col-md-6 col-sm-12 mb-3">
          <div class="bank-card text-center p-3">
            <input type="checkbox" :value="bank.company_id" v-model="selectedBanks" class="form-check-input" :id="'bank_' + bank.company_id" />
            <label :for="'bank_' + bank.company_id" class="form-check-label">
              <div class="bank-img">
                <img :src="`/pictures/${bank.company_name}.png`" alt="선호 은행 이미지" />
              </div>
              <p class="mt-2">{{ bank.company_name }}</p>
            </label>
          </div>
        </div>
      </div>

      <!-- 제출 버튼 -->
      <div class="text-center">
        <button type="submit" class="btn btn-primary mt-3">수정하기</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useBankStore } from "@/stores/bank";
import { useRouter } from "vue-router";

const store = useBankStore();
const router = useRouter();
const banks = ref([]); // 전체 은행 목록
const selectedBanks = ref([]); // 사용자 선호 은행 ID 목록

onMounted(() => {
  // 전체 은행 목록 가져오기
  store
    .getBanks()
    .then((response) => {
      if (Array.isArray(response)) {
        banks.value = response;
      } else if (response.banks && Array.isArray(response.banks)) {
        banks.value = response.banks;
      } else {
        console.error("은행 데이터가 예상 형식과 다릅니다:", response);
      }
    })
    .catch((err) => console.error("은행 목록 가져오기 실패:", err));

  // 기존 선호 은행 가져오기
  store
    .getUserProfile()
    .then((profile) => {
      const preferredBanks = profile?.profile_user?.preferred_banks || [];
      selectedBanks.value = preferredBanks.map((bank) => bank.company_id);
      console.log("초기화된 선호 은행 목록:", selectedBanks.value);
    })
    .catch((err) => console.error("선호 은행 가져오기 실패:", err));
});

// 선호 은행 업데이트
const updatePreferredBanks = () => {
  store
    .updatePreferredBanks(selectedBanks.value)
    .then(() => {
      alert("선호 은행이 성공적으로 업데이트되었습니다!");
      return store.getUserProfile(); // 프로필 갱신
    })
    .then(() => {
      router.push({ name: "AccountView" }); // 프로필 페이지로 이동
    })
    .catch((err) => console.error("선호 은행 업데이트 실패:", err));
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.preferred-banks-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 15px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
}

/* 제목 스타일 */
h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #555;
  text-align: center;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

/* 폼 스타일 */
.preferred-banks-form {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

/* 선호 은행 리스트 */
.preferred-banks-list {
  display: flex;
  flex-wrap: wrap; /* 줄바꿈 허용 */
  gap: 15px; /* 카드 간격 */
  justify-content: center; /* 카드들을 가운데 정렬 */
}

/* 카드 기본 스타일 */
.bank-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
}

.bank-card:hover {
  transform: translateY(-5px); /* 호버 시 살짝 떠오르는 효과 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 호버 시 그림자 강조 */
}

/* 체크박스 숨기기 */
.form-check-input {
  display: none; /* 기본 체크박스 숨기기 */
}

/* 체크박스 라벨 기본 스타일 */
.form-check-label {
  cursor: pointer; /* 손 모양 커서 */
  display: block;
}

/* 선택된 카드 스타일 */
.form-check-input:checked + .form-check-label {
  border-color: #007bff; /* 선택된 카드 테두리 색상 */
  background-color: #e6f0ff; /* 선택된 카드 배경색 */
  box-shadow: 0 6px 12px rgba(0, 123, 255, 0.2); /* 선택된 카드 그림자 */
  transform: scale(1.02); /* 선택된 카드 확대 효과 */
}

/* 은행 이미지 */
.bank-img img {
  width: 70px;
  height: 70px;
  object-fit: contain; /* 비율 유지하며 축소 */
  margin-bottom: 10px;
  border-radius: 50%; /* 동그랗게 */
  border: 1px solid #eee;
}

/* 은행 이름 */
.bank-card p {
  font-size: 0.9rem;
  font-weight: bold;
  color: #333;
  margin: 0;
  text-align: center;
}

/* 버튼 스타일 */
.btn-primary {
  display: inline-block;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 0.95rem;
  border-radius: 25px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 */
}

/* 반응형 스타일 */
@media (min-width: 992px) {
  /* 큰 화면에서 한 줄에 3개 */
  .col-lg-4 {
    flex: 0 0 30%;
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
  .col-sm-12 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>
