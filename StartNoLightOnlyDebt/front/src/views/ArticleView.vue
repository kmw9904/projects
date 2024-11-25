<template>
  <div class="community-page">
    <h1 class="page-title">커뮤니티</h1>
    <div class="content-wrapper">
      <ArticleList />
    </div>
  </div>
</template>

<script>
import ArticleList from "@/articles/ArticleList.vue";

export default {
  components: {
    ArticleList,
  },
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
.community-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #343a40;
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

/* 콘텐츠 래퍼 스타일 */
.content-wrapper {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
