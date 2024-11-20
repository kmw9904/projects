<template>
  <div>
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
    <button @click="toggleLike(article.id)">{{ article.is_liked ? "좋아요 취소" : "좋아요" }} ({{ article.likes_count }})</button>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { onMounted, computed } from "vue";
import { useRoute } from "vue-router";

// Pinia Store
const store = useArticleStore();
const route = useRoute();

// 게시글 상세 정보 가져오기
onMounted(() => {
  store.fetchArticleDetail(route.params.id);
});

const article = computed(() => store.selectedArticle);

// 좋아요 기능
const toggleLike = (articleId) => {
  store.toggleLike(articleId);
};
</script>

<style scoped>
button {
  margin-top: 10px;
}
</style>
