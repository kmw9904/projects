<template>
  <div class="map-component">
    <div id="mapContainer" class="map-container"></div>
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

<script setup>
import { ref, watch, onMounted } from "vue";

// Props 설정
const props = defineProps({
  province: String,
  city: String,
  bank: String,
});

// 상태 변수
const map = ref(null);
const infowindow = ref(null);
const markers = ref([]);
const results = ref([]);
const loaded = ref(false);

// 환경 변수에서 Kakao API 키 가져오기
const KAKAO_KEY = import.meta.env.VITE_KAKAO_MAP_KEY || ""; // 기본값으로 빈 문자열 설정

if (!KAKAO_KEY) {
  console.error("Kakao API Key가 설정되지 않았습니다. .env 파일을 확인하세요.");
}

// Kakao 지도 로드
const loadKakaoMap = () => {
  if (loaded.value) return;

  const script = document.createElement("script");
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_KEY}&autoload=false&libraries=services`;
  script.async = true;
  script.onload = () => {
    window.kakao.maps.load(() => {
      initializeKakaoMap();
      loaded.value = true;
    });
  };
  document.head.appendChild(script);
};

// Kakao 지도 초기화
const initializeKakaoMap = () => {
  const mapContainer = document.getElementById("mapContainer");
  const mapOption = {
    center: new window.kakao.maps.LatLng(37.566826, 126.9786567),
    level: 3,
  };

  map.value = new window.kakao.maps.Map(mapContainer, mapOption);
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });
};

// 장소 검색
const searchPlaces = () => {
  if (!map.value || !loaded.value) {
    console.error("지도 또는 Kakao API가 초기화되지 않았습니다.");
    return;
  }

  const keyword = `${props.province} ${props.city} ${props.bank}`;
  if (!keyword.trim()) {
    alert("검색어를 입력하세요.");
    return;
  }

  const ps = new window.kakao.maps.services.Places();
  ps.keywordSearch(keyword, placesSearchCB);
};

// 장소 검색 콜백
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

// 마커 표시
const displayMarker = (place) => {
  const marker = new window.kakao.maps.Marker({
    map: map.value,
    position: new window.kakao.maps.LatLng(place.y, place.x),
  });

  window.kakao.maps.event.addListener(marker, "click", () => {
    const content = `
      <div style="
        padding:10px; 
        font-size:14px; 
        width:200px; /* 박스 너비 고정 */
        overflow-wrap:break-word; /* 긴 단어 줄바꿈 */
        white-space:normal; /* 텍스트 줄바꿈 허용 */
        box-sizing:border-box; /* 패딩 포함한 크기 계산 */
        overflow:hidden; /* 넘치는 텍스트 숨기기 */
      ">
        <a href="${place.place_url}" target="_blank" style="
          color:blue; 
          font-weight:bold; 
          text-decoration:none;
          display:block; /* 텍스트가 박스 안에 있도록 블록으로 지정 */
        ">
          ${place.place_name}
        </a>
      </div>`;
    infowindow.value.setContent(content);
    infowindow.value.open(map.value, marker);
  });

  markers.value.push(marker);
};

// 모든 마커 제거
const removeAllMarkers = () => {
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];
};

// Props 변경 시 장소 검색 실행
watch([() => props.province, () => props.city, () => props.bank], searchPlaces);

// 지도 로드
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
  font-family: "Noto Sans KR", sans-serif;
  margin-top: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.results-title {
  font-family: "Noto Sans KR", sans-serif;
  font-size: 1.7rem;
  font-weight: bold;
  margin-bottom: 15px;
}
</style>
