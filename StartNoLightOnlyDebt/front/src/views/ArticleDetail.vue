<template>
  <div class="article-detail-page">
    <div v-if="article" class="article-detail">
      <div class="article-header">
        <div class="header-content">
          <h2>{{ article.title }}</h2>
          <p class="article-info">
            <span>❤️ {{ article.likes_count }}</span>
            <span>💬 댓글 {{ article.comments.length }}</span>
          </p>
        </div>
        <button v-if="profile?.profile_user?.username === article?.user?.username" class="delete-article-header" @click="deleteArticle">삭제</button>
      </div>

      <p class="article-content">{{ article.content }}</p>

      <button class="like-button" @click="toggleLike(article.id)">
        {{ article.is_liked ? "💔" : "❤️" }}
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
            <button v-if="profile?.profile_user?.username === comment.user.username" class="delete-comment" @click="deleteComment(comment.id)">댓글 삭제</button>
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
import { onMounted, computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBankStore } from "@/stores/bank";

const store = useArticleStore();
const route = useRoute();
const router = useRouter();
const userstore = useBankStore();
const profile = ref(null);

onMounted(async () => {
  await store.fetchArticleDetail(route.params.id);
  await userstore.getUserProfile(); // 항상 최신 데이터를 가져오도록 설정
  profile.value = userstore.profile;
});

const article = computed(() => store.selectedArticle);

const deleteArticle = async () => {
  if (confirm("정말로 이 게시글을 삭제하시겠습니까?")) {
    await store.deleteArticle(route.params.id);
    alert("게시글이 삭제되었습니다.");
    router.push("/articles"); // 게시글 목록 페이지로 이동
  }
};

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
  if (profile.value?.profile_user?.username) {
    store.deleteComment(route.params.id, commentId);
  } else {
    alert("권한이 없습니다.");
  }
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
  font-family: "Noto Sans KR", sans-serif;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.article-header {
  position: relative;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-header h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
  font-weight: bold;
}

.article-info {
  font-size: 0.9rem;
  color: #757575;
  display: flex;
  justify-content: space-between;
}

.article-content {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #555;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.like-button,
.delete-article,
.back-button {
  padding: 10px 15px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
  font-weight: bold;
}

.like-button {
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.like-button:hover {
  background-color: #ff4a3d;
}

.delete-article-header {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 5px 10px;
  font-size: 0.9rem;
  background-color: transparent;
  color: #d9534f;
  border: 1px solid #d9534f;
  border-radius: 5px;
  cursor: pointer;
}

.delete-article-header:hover {
  background-color: #d9534f;
  color: white;
}

.back-button {
  background-color: #6c757d;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  background-color: #5a6268;
}

.comments-section {
  margin-top: 30px;
}

.comments-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.comment-form textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: "Noto Sans KR", sans-serif;
}

.comment-form button {
  padding: 10px 15px;
  background-color: #5bc0de;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-form button:hover {
  background-color: #31b0d5;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  margin-bottom: 15px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #555;
}

.comment-author {
  font-weight: bold;
  color: #333;
}

.comment-content {
  margin-bottom: 10px;
  font-size: 1rem;
  line-height: 1.5;
  color: #555;
}

.delete-comment {
  font-size: 0.8rem;
  background-color: transparent;
  color: #d9534f;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.delete-comment:hover {
  color: #c9302c;
}
</style>
