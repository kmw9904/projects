<template>
  <div class="article-list-page">
    <h2>전체 카페 글</h2>

    <!-- 게시글 목록 -->
    <table class="article-table">
      <thead>
        <tr>
          <th class="title">제목</th>
          <th class="date">작성일</th>
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
          <td class="date">{{ article.created_at }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ active: page === currentPage }">
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

const articles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage;
  const end = start + articlesPerPage;
  return store.articles.slice(start, end); // 페이지에 해당하는 게시글만 보여줌
});

const totalPages = computed(() => Math.ceil(store.articles.length / articlesPerPage));

const goToPage = (page) => {
  currentPage.value = page;
};
</script>

<style scoped>
.article-list-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: left;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.article-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.article-table th,
.article-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  font-size: 1rem;
}

.article-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.article-table .title {
  width: 70%;
}

.article-table .date {
  width: 30%;
  text-align: center;
}

.article-table .comment-count {
  color: red;
  margin-left: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 5px;
}

.pagination button {
  padding: 5px 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  border-radius: 5px;
}

.pagination button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
</style>
