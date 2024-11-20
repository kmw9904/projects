<template>
  <div>
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    <p>
      <strong>작성자:</strong>
      {{ article.user }}
    </p>
    <hr />
    <h2>댓글</h2>
    <ul>
      <li v-for="comment in article.comments" :key="comment.id">
        {{ comment.content }} -
        <strong>{{ comment.user }}</strong>
        <button @click="deleteComment(comment.id)">삭제</button>
      </li>
    </ul>
    <CommentForm :article-id="article.id" @refresh="fetchArticle" />
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import CommentForm from "@/articles/CommentForm.vue";
import { onMounted, computed } from "vue";
import { useRoute } from "vue-router";

const store = useArticleStore();
const route = useRoute();

const fetchArticle = () => {
  store.fetchArticleDetail(route.params.id);
};

onMounted(fetchArticle);

const article = computed(() => store.selectedArticle);

const deleteComment = async (commentId) => {
  await store.deleteComment(article.value.id, commentId);
  fetchArticle();
};
</script>

<style scoped>
h1 {
  margin-bottom: 10px;
}
hr {
  margin: 20px 0;
}
</style>
