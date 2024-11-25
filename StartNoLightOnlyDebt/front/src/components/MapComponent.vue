<template>
  <div class="map-component">
    <!-- 지도 -->
    <div id="mapContainer" class="map-container"></div>

    <!-- 검색 결과 -->
    <div class="search-results">
      <h4 class="results-title">검색 결과</h4>
      <ul v-if="results.length > 0">
        <li v-for="(place, index) in results" :key="index">
          <strong>{{ place.place_name }}</strong>
          -
          <a :href="place.place_url" target="_blank">자세히 보기</a>
        </li>
      </ul>
      <p v-else>검색 결과가 없습니다.</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
declare global {
  interface Window {
    kakao: any;
  }
}

import { ref, watch, onMounted } from "vue";

const props = defineProps({
  province: String,
  city: String,
  bank: String,
});

const map = ref(null);
const infowindow = ref(null);
const markers = ref([]);
const results = ref([]);
const loaded = ref(false); // 지도 로드 완료 상태 확인

// Kakao 지도 로드 및 초기화
const loadKakaoMap = () => {
  if (loaded.value) return;

  const script = document.createElement("script");
  const KAKAO_KEY = "b94dc4c8f7f1f5db7aec4e20ccf8d234";
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_KEY}&autoload=false&libraries=services`;
  script.async = true;
  script.onload = () => {
    window.kakao.maps.load(() => {
      initializeKakaoMap();
      loaded.value = true; // 로드 완료
    });
  };
  document.head.appendChild(script);
};

const initializeKakaoMap = () => {
  const mapContainer = document.getElementById("mapContainer");
  const mapOption = {
    center: new window.kakao.maps.LatLng(37.566826, 126.9786567), // 기본 좌표
    level: 3, // 확대 레벨
  };

  map.value = new window.kakao.maps.Map(mapContainer, mapOption);
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });
};

// 장소 검색 실행
const searchPlaces = () => {
  if (!map.value || !loaded.value) {
    console.error("지도 또는 Kakao API가 아직 초기화되지 않았습니다.");
    return;
  }

  const keyword = `${props.province} ${props.city} ${props.bank}`;
  if (!keyword.trim()) {
    alert("검색어를 입력해주세요.");
    return;
  }

  const ps = new window.kakao.maps.services.Places();
  ps.keywordSearch(keyword, placesSearchCB);
};

const placesSearchCB = (data, status) => {
  if (status === window.kakao.maps.services.Status.OK) {
    results.value = data;
    removeAllMarkers();

    const bounds = new window.kakao.maps.LatLngBounds();
    data.forEach((place) => {
      displayMarker(place);
      bounds.extend(new window.kakao.maps.LatLng(place.y, place.x));
    });

    map.value.setBounds(bounds);
  } else {
    results.value = [];
    alert("검색 결과가 없습니다.");
  }
};

const displayMarker = (place) => {
  const marker = new window.kakao.maps.Marker({
    map: map.value,
    position: new window.kakao.maps.LatLng(place.y, place.x),
  });

  window.kakao.maps.event.addListener(marker, "click", () => {
    // 인포윈도우에 HTML 스타일 적용
    const content = `
      <div style="
        padding:10px;
        font-size:14px;
        width:200px; /* 너비 고정 */
        overflow-wrap:break-word; /* 긴 단어 줄바꿈 */
        white-space:normal; /* 텍스트 자동 줄바꿈 */
        box-sizing:border-box; /* 패딩 포함한 박스 크기 계산 */
        overflow:hidden; /* 오버플로우 숨김 */
      ">
        <a href="${place.place_url}" target="_blank" style="
          color:blue;
          font-weight:bold;
          text-decoration:none;
        ">
          ${place.place_name}
        </a>
      </div>`;
    infowindow.value.setContent(content);
    infowindow.value.open(map.value, marker);
  });

  markers.value.push(marker);
};

const removeAllMarkers = () => {
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];
  markers.value = [];
};

// Props 값이 변경되면 장소 검색 실행
watch([() => props.province, () => props.city, () => props.bank], searchPlaces);

// 초기 지도 로드
onMounted(loadKakaoMap);
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 400px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.search-results {
  margin-top: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.results-title {
  font-size: 1.7rem;
  font-weight: bold;
  margin-bottom: 15px;
}
</style>
