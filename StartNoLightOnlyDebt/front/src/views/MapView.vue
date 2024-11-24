<template>
  <div class="map-page">
    <!-- 헤더 -->
    <div class="jumbotron map-jumbotron">
      <div class="text-container">
        <h1 class="text-title">내 주변 은행 찾기</h1>
        <p class="header-subtitle">가장 가까운 은행과 금융 상품 정보를 찾아보세요.</p>
      </div>
    </div>

    <!-- 검색 옵션 및 지도 -->
    <div id="map-search-section" class="search-section py-5 bg-light">
      <div class="container">
        <div class="row">
          <!-- 검색 옵션 -->
          <div class="col-md-4">
            <div class="card shadow-sm p-4 search-card">
              <h5 class="card-title text-center mb-4">검색 옵션</h5>
              <v-select
                v-model="province"
                :items="infos.map(info => info.prov)"
                label="도/시 선택"
                outlined
                dense
                class="mb-3"
                @change="updateCities"
              ></v-select>
              <v-select
                v-model="city"
                :items="cities"
                label="시/군/구 선택"
                outlined
                dense
                class="mb-3"
              ></v-select>
              <v-select
                v-model="bank"
                :items="banks"
                label="은행 선택"
                outlined
                dense
                class="mb-4"
              ></v-select>
              <button class="btn btn-primary btn-block" @click="triggerSearch">
                검색하기
              </button>
            </div>
          </div>

          <!-- 지도 및 검색 결과 -->
          <div class="col-md-8">
            <MapComponent :province="province" :city="city" :bank="bank" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import MapComponent from "@/components/MapComponent.vue";
import { useMapStore } from "@/stores/map";

const store = useMapStore();

const infos = store.infos;
const banks = store.banks;
const cities = ref<string[]>([]);

const province = ref("");
const city = ref("");
const bank = ref("");

const updateCities = () => {
  const selectedInfo = infos.find((info) => info.prov === province.value);
  cities.value = selectedInfo ? selectedInfo.city : [];
};

watch(province, updateCities);

const triggerSearch = () => {
  console.log("검색 트리거: ", { province: province.value, city: city.value, bank: bank.value });
};
</script>

<style scoped>
/* 스타일 그대로 유지 */
.map-page {
  background-color: #f9f9f9;
  min-height: 100vh;
}

.map-jumbotron {
  height: 30vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("/public/pictures/지도배경.jpg");
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.text-title {
  font-size: 3rem;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.header-subtitle {
  font-size: 1.2rem;
  margin-top: 1rem;
  color: #ddd;
}

.search-section {
  padding: 40px 0;
}

.search-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.search-card .btn {
  font-size: 1rem;
  font-weight: bold;
  padding: 10px;
  background-color: #1976d2;
  color: white;
  border-radius: 5px;
}

.search-card .btn:hover {
  background-color: #0056b3;
}
</style>
