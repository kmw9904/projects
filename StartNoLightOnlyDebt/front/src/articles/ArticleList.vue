<template>
  <div>
    <h2>게시글 목록</h2>

    <!-- 게시글 작성 폼 -->
    <form @submit.prevent="submitArticle">
      <input v-model="newArticle.title" type="text" placeholder="제목을 입력하세요" required />
      <textarea v-model="newArticle.content" placeholder="내용을 입력하세요" required></textarea>
      <button type="submit">게시글 작성</button>
    </form>

    <!-- 게시글 목록 -->
    <div v-if="articles.length">
      <div v-for="article in articles" :key="article.id">
        <!-- 제목 클릭 시 상세 페이지로 이동 -->
        <h3>
          <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">
            {{ article.title }}
          </RouterLink>
        </h3>
        <p>{{ article.content }}</p>
        <div>
          <button @click="toggleLike(article.id)">{{ article.is_liked ? "좋아요 취소" : "좋아요" }} ({{ article.likes_count }})</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>게시글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { onMounted, computed, reactive } from "vue";
import { RouterLink } from "vue-router";

// Pinia Store
const store = useArticleStore();

// 게시글 목록 가져오기
onMounted(() => {
  store.fetchArticles();
});

// 상태 데이터
const articles = computed(() => store.articles);
const newArticle = reactive({
  title: "",
  content: "",
});

// 게시글 작성
const submitArticle = () => {
  store.createArticle({
    title: newArticle.title,
    content: newArticle.content,
  });

  // 작성 후 입력값 초기화
  newArticle.title = "";
  newArticle.content = "";
};

// 좋아요 기능
const toggleLike = (articleId) => {
  store.toggleLike(articleId);
};
</script>

<style scoped>
h2 {
  margin-bottom: 10px;
}
form {
  margin-bottom: 20px;
}
form input,
form textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
}
form button {
  display: block;
}
button {
  margin-top: 10px;
}
</style>
