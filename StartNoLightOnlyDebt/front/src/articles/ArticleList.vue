<template>
  <div class="article-list-page container">
    <h2 class="section-title text-center mb-4">게시글 목록</h2>

    <!-- 새 게시글 작성 버튼 -->
    <div class="create-button text-end mb-4">
      <RouterLink :to="{ name: 'ArticleCreate' }">
        <button class="btn btn-create">새 게시글 작성</button>
      </RouterLink>
    </div>

    <!-- 게시글 목록 -->
    <div class="article-list">
      <div v-for="article in articles" :key="article.id" class="article-item shadow-sm">
        <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }" class="article-title">
          <h3>{{ article.title }}</h3>
        </RouterLink>
        <p class="article-info">
          <span class="author">작성자: {{ article.user.username }}</span>
          <span class="date">작성일: {{ formatDate(article.created_at) }}</span>
        </p>
        <p class="likes">
          <strong>❤️</strong> {{ article.likes_count }}
        </p>
        <p v-if="article.comments_count > 0" class="comment-count">
          댓글 {{ article.comments_count }}개
        </p>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination d-flex justify-content-center mt-4">
      <button
        class="btn btn-pagination mx-1"
        v-for="page in totalPages"
        :key="page"
        @click="goToPage(page)"
        :class="{ active: page === currentPage }"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, computed } from "vue";
import { useArticleStore } from "@/stores/articles";
import { RouterLink } from "vue-router";

const store = useArticleStore();

// 상태 데이터
const currentPage = reactive({ value: 1 });
const articlesPerPage = 10;

onMounted(() => {
  store.fetchArticles(); // 게시글 가져오기
});

// 게시글을 정렬 (최신순)
const sortedArticles = computed(() => {
  return [...store.articles].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
});

const articles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage;
  const end = start + articlesPerPage;
  return sortedArticles.value.slice(start, end); // 페이지에 해당하는 게시글만 보여줌
});

const totalPages = computed(() => Math.ceil(store.articles.length / articlesPerPage));

const goToPage = (page) => {
  currentPage.value = page;
};

// 작성일 형식 변환 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear(); // 4자리 연도
  const month = String(date.getMonth() + 1).padStart(2, "0"); // 월 (2자리)
  const day = String(date.getDate()).padStart(2, "0"); // 일 (2자리)
  return `${year}-${month}-${day}`; // YYYY-MM-DD 형식으로 반환
};
</script>

<style scoped>
/* 페이지 스타일 */
.article-list-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 2rem;
}

/* 게시글 목록 스타일 */
.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-item {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.article-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.article-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #007bff;
  text-decoration: none;
  margin-bottom: 10px;
  display: block;
}

.article-title:hover {
  color: #0056b3;
}

.article-info {
  font-size: 0.9rem;
  color: #757575;
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.likes {
  font-size: 1rem;
  color: #ff6f61;
  margin-bottom: 5px;
}

.comment-count {
  font-size: 0.9rem;
  color: #ff6f61;
}

/* 새 게시글 작성 버튼 */
.create-button .btn-create {
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.create-button .btn-create:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 페이지네이션 스타일 */
.pagination .btn-pagination {
  padding: 8px 16px;
  font-size: 1rem;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: all 0.2s ease;
}

.pagination .btn-pagination.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.pagination .btn-pagination:hover {
  background-color: #0056b3;
  color: white;
}
</style>
