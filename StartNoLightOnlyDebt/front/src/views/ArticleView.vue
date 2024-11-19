<template>
  <div class="article-view-wrapper d-flex flex-column my-3">
    <h1 class="mt-5 half-highlight">자유 게시판</h1>
    <v-container>
      <ArticleList />
    </v-container>
  </div>
</template>

<script>
import { onMounted } from "vue";
import ArticleList from "@/components/ArticleList.vue";
import { useBankStore } from "@/stores/bank";

const store = useBankStore();

export default {
  setup() {
    onMounted(() => {
      store.getArticles();
    });
  },
};
</script>

<style scoped></style>
