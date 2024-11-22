<template>
  <div class="preferred-banks-container">
    <h1 class="text-center mb-4">선호 은행 수정</h1>
    <form @submit.prevent="updatePreferredBanks" class="preferred-banks-form card shadow-sm p-4">
      <div class="row">
        <div class="col-sm-6 mb-3 mb-sm-0">
          <div v-for="bank in banks" :key="bank.company_id" class="form-check mb-2">
            <input type="checkbox" :value="bank.company_id" v-model="selectedBanks" class="form-check-input" :id="'bank_' + bank.company_id" />
            <label :for="'bank_' + bank.company_id" class="form-check-label">
              <div class="bank-img">
                <img :src="`/pictures/${bank.company_name}.png`" alt="선호 은행 이미지" />
              </div>
              {{ bank.company_name }}
            </label>
          </div>
        </div>
      </div>

      <!-- 제출 버튼 -->
      <div class="text-center">
        <button type="submit" class="btn btn-secondary w-100">수정하기</button>
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
.preferred-banks-container {
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.preferred-banks-form {
  background-color: #ffffff;
  border-radius: 10px;
}

.form-check-label {
  margin-left: 5px;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.bank-img {
  width: 100px; /* 이미지 컨테이너의 너비 */
  height: 100px;
  flex-shrink: 0; /* 크기를 줄이지 않음 */
  margin-right: 10px;
}

.bank-img img {
  width: 100px; /* 이미지 컨테이너의 너비 */
  height: 100px;
  object-fit: contain; /* 이미지가 비율에 맞게 축소되며 잘리지 않음 */
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
}
</style>
