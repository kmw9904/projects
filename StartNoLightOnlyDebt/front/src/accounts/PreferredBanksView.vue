<template>
  <div>
    <h1>선호 은행 수정</h1>
    <form @submit.prevent="updatePreferredBanks">
      <div v-for="bank in banks" :key="bank.company_id">
        <!-- 체크박스: selectedBanks에 해당 은행의 ID가 포함되어 있으면 체크 -->
        <input type="checkbox" :value="bank.company_id" v-model="selectedBanks" />
        {{ bank.company_name }}
      </div>
      <button type="submit">수정하기</button>
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

<style scoped></style>
