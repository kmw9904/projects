<template>
  <div>
    <h2>게시글 목록</h2>
    <div v-for="article in articles" :key="article.id">
      <h3>{{ article.title }}</h3>
      <p>{{ article.content }}</p>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { onMounted, computed } from "vue";

const store = useArticleStore();

onMounted(() => {
  store.fetchArticles();
});

const articles = computed(() => store.articles);
</script>

<style scoped>
h2 {
  margin-bottom: 10px;
}
</style>
