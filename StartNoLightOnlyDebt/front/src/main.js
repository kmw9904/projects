import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // Vuetify 기본 스타일

import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import App from "./App.vue";
import router from "./router";
import axios from "./api/axios"; // Axios 설정 파일 가져오기

const app = createApp(App);

const vuetify = createVuetify({
    components,
    directives,
});

// Pinia 설정 및 플러그인 등록
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(vuetify); // Vuetify 등록
app.use(pinia); // Pinia 등록
app.use(router); // Router 등록

// Axios를 전역에서 사용할 수 있도록 설정
app.config.globalProperties.$axios = axios;

app.mount("#app"); // Vue 앱 마운트
