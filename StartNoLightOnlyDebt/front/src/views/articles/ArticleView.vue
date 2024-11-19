<template>
  <div class="article-view-wrapper d-flex flex-column my-3">
    <h1 class="mt-5 half-highlight">자유 게시판</h1>
    <v-container>
      <ArticleList />
    </v-container>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import ArticleList from "@/components/ArticleList.vue";
import { useCommunityStore } from "@/stores/community";

const store = useCommunityStore();

onMounted(() => {
  store.getArticles();
});
</script>

<style scoped></style>
