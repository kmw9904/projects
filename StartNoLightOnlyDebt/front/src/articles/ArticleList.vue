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
    <table class="article-table table table-hover shadow-sm">
      <thead class="table-header">
        <tr>
          <th class="title">제목</th>
          <th class="author">작성자</th>
          <th class="date">작성일</th>
          <th class="likes">좋아요</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in articles" :key="article.id">
          <td class="title">
            <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">
              {{ article.title }}
            </RouterLink>
            <span v-if="article.comments_count > 0" class="comment-count">[{{ article.comments_count }}]</span>
          </td>
          <td class="author">{{ article.user.username }}</td>
          <td class="date">{{ formatDate(article.created_at) }}</td>
          <td class="likes text-center">
            <strong>❤️</strong>
            {{ article.likes_count }}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div class="pagination d-flex justify-content-center mt-4">
      <button class="btn btn-pagination mx-1" v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ active: page === currentPage }">
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
/* 제목 스타일 */
.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 2rem;
}

/* 테이블 스타일 */
.article-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  background-color: #fff;
}

.article-table th,
.article-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  font-size: 1rem;
}

.article-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.article-table .title {
  width: 40%;
}

.article-table .author {
  width: 20%;
  text-align: center;
}

.article-table .date {
  width: 20%;
  text-align: center;
}

.article-table .likes {
  width: 10%;
  text-align: center;
}

.article-table .comment-count {
  color: red;
  margin-left: 5px;
}

/* 새 게시글 작성 버튼 스타일 */
.create-button .btn-create {
  background-color: #007bff; /* 기본 파란색 배경 */
  color: white; /* 텍스트 흰색 */
  font-size: 1rem;
  padding: 10px 20px; /* 버튼 패딩 */
  border: none;
  border-radius: 5px; /* 둥근 모서리 */
  cursor: pointer;
  transition: background-color 0.3s ease; /* 호버 애니메이션 */
}

.create-button .btn-create:hover {
  background-color: #0056b3; /* 호버 시 어두운 파란색 */
  transform: translateY(-2px); /* 살짝 떠오르는 효과 */
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
