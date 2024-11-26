<template>
  <div class="article-create-page">
    <h2 class="section-title">새 게시글 작성</h2>
    <form @submit.prevent="submitArticle" class="form-container shadow-sm">
      <div class="form-group">
        <label for="title">제목</label>
        <input id="title" v-model="title" type="text" required />
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model="content" rows="10" required></textarea>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn-submit">작성 완료</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useArticleStore } from "@/stores/articles";
import { useRouter } from "vue-router";

const title = ref("");
const content = ref("");
const articleStore = useArticleStore();
const router = useRouter();

const submitArticle = async () => {
  const articleData = {
    title: title.value,
    content: content.value,
  };
  try {
    await articleStore.createArticle(articleData);
    // 게시글 작성 후 목록 페이지로 이동
    router.push({ name: "article" });
  } catch (error) {
    console.error("게시글 작성 중 오류 발생:", error.response?.data || error.message);
    // 에러 처리 로직 추가 가능
  }
};
</script>

<style scoped>
/* 페이지 전체 스타일 */
.article-create-page {
  font-family: "Noto Sans KR", sans-serif;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: "Noto Sans KR", sans-serif;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 20px;
  text-align: center;
}

/* 폼 컨테이너 */
.form-container {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input[type="text"]:focus,
textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  outline: none;
}

/* 버튼 스타일 */
.form-actions {
  text-align: center;
  margin-top: 20px;
}

.btn-submit {
  padding: 10px 20px;
  font-size: 1.2rem;
  font-weight: bold;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-submit:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
