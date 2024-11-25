<template>
  <div class="article-detail-page">
    <div v-if="article" class="article-detail">
      <h2>{{ article.title }}</h2>
      <p class="article-content">{{ article.content }}</p>
      <button class="like-button" @click="toggleLike(article.id)">{{ article.is_liked ? "좋아요 취소" : "좋아요" }} ({{ article.likes_count }})</button>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h3>댓글</h3>

        <!-- 댓글 입력 폼 -->
        <form @submit.prevent="submitComment" class="comment-form">
          <textarea v-model="newComment.content" placeholder="댓글을 입력하세요" required></textarea>
          <button type="submit">댓글 작성</button>
        </form>

        <!-- 댓글 목록 -->
        <div v-if="article.comments.length" class="comment-list">
          <div v-for="comment in article.comments" :key="comment.id" class="comment-item">
            <p>{{ comment.content }}</p>
            <button @click="deleteComment(comment.id)">댓글 삭제</button>
          </div>
        </div>
        <div v-else>
          <p>댓글이 없습니다.</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>게시글을 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { onMounted, computed, reactive } from "vue";
import { useRoute } from "vue-router";

const store = useArticleStore();
const route = useRoute();

onMounted(() => {
  store.fetchArticleDetail(route.params.id);
});

const article = computed(() => store.selectedArticle);

const newComment = reactive({
  content: "",
});

const submitComment = () => {
  if (newComment.content.trim() === "") {
    alert("댓글을 입력해주세요.");
    return;
  }

  store.createComment(route.params.id, { content: newComment.content });
  newComment.content = "";
};

const deleteComment = (commentId) => {
  store.deleteComment(route.params.id, commentId);
};

const toggleLike = (articleId) => {
  store.toggleLike(articleId);
};
</script>

<style scoped>
.article-detail-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.article-detail h2 {
  font-size: 2rem;
  margin-bottom: 15px;
}

.article-content {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.like-button {
  padding: 10px 15px;
  font-size: 1rem;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 30px;
}

.comments-section h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.comment-form textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.comment-form button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
