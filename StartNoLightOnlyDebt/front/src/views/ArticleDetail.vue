<template>
  <div v-if="article">
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
    <button @click="toggleLike(article.id)">
      {{ article.is_liked ? "좋아요 취소" : "좋아요" }} ({{ article.likes_count }})
    </button>

    <!-- 댓글 입력 폼 -->
    <form @submit.prevent="submitComment">
      <textarea v-model="newComment" placeholder="댓글을 입력하세요" required></textarea>
      <button type="submit">댓글 작성</button>
    </form>

    <!-- 댓글 목록 -->
    <div v-if="article.comments.length">
      <div v-for="comment in article.comments" :key="comment.id">
        <p>{{ comment.content }}</p>
        <button @click="deleteComment(comment.id)">댓글 삭제</button>
      </div>
    </div>
    <div v-else>
      <p>댓글이 없습니다.</p>
    </div>
  </div>
  <div v-else>
    <p>게시글을 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { onMounted, computed, reactive } from "vue";
import { useRoute } from "vue-router";

// Pinia Store
const store = useArticleStore();
const route = useRoute();

// 게시글 상세 정보 가져오기
onMounted(() => {
  store.fetchArticleDetail(route.params.id);
});

const article = computed(() => store.selectedArticle);

// 댓글 입력 데이터
const newComment = reactive({
  content: "",
});

// 댓글 작성
const submitComment = () => {
  if (newComment.content.trim() === "") {
    alert("댓글을 입력해주세요."); // 댓글이 비어있는 경우, 경고 메시지 표시
    return;
  }
  
  store.createComment(route.params.id, { content: newComment.content });
  newComment.content = ""; // 댓글 작성 후 초기화
};

// 댓글 삭제
const deleteComment = (commentId) => {
  store.deleteComment(route.params.id, commentId);
};

// 좋아요 기능
const toggleLike = (articleId) => {
  store.toggleLike(articleId);
};
</script>

<style scoped>
button {
  margin-top: 10px;
}
textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
}
</style>
