<template>
  <div class="article-detail-page">
    <div v-if="article" class="article-detail">
      <div class="article-header">
        <h2>{{ article.title }}</h2>
        <p class="article-info">
          <span>❤️ 좋아요 {{ article.likes_count }}</span>
          <span>💬 댓글 {{ article.comments.length }}</span>
        </p>
      </div>

      <p class="article-content">{{ article.content }}</p>

      <button class="like-button" @click="toggleLike(article.id)">
        {{ article.is_liked ? "좋아요 취소" : "좋아요" }}
      </button>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h3 class="comments-title">댓글</h3>

        <!-- 댓글 입력 폼 -->
        <form @submit.prevent="submitComment" class="comment-form">
          <textarea v-model="newComment.content" placeholder="댓글을 입력하세요" required></textarea>
          <button type="submit">댓글 작성</button>
        </form>

        <!-- 댓글 목록 -->
        <div class="comment-list">
          <div v-for="comment in article.comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
            <button class="delete-comment" @click="deleteComment(comment.id)">댓글 삭제</button>
          </div>
        </div>
      </div>

      <!-- 뒤로가기 버튼 -->
      <button class="back-button" @click="goBack">뒤로가기</button>
    </div>
    <div v-else>
      <p>게시글을 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { onMounted, computed, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";

const store = useArticleStore();
const route = useRoute();
const router = useRouter();

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

const goBack = () => {
  router.back();
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  const minute = String(date.getMinutes()).padStart(2, "0");
  return `${year}.${month}.${day} ${hour}:${minute}`;
};
</script>

<style scoped>
.article-detail-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.article-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.article-header h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.article-info {
  font-size: 0.9rem;
  color: #6c757d;
  display: flex;
  justify-content: space-between;
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

.comments-section {
  margin-top: 30px;
}

.comments-title {
  font-size: 1.5rem;
  font-weight: bold;
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
  margin-bottom: 15px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f8f9fa;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #6c757d;
}

.comment-author {
  font-weight: bold;
}

.comment-content {
  margin-bottom: 10px;
  font-size: 1rem;
}

.delete-comment {
  font-size: 0.8rem;
  background-color: transparent;
  color: #dc3545;
  border: none;
  cursor: pointer;
}

.back-button {
  margin-top: 20px;
  padding: 10px 15px;
  font-size: 1rem;
  border: none;
  background-color: #6c757d;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #5a6268;
}
</style>
