import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

// Pinia 설정 및 플러그인 등록
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia); // Pinia 등록
app.use(router); // Router 등록

app.mount("#app"); // Vue 앱 마운트
