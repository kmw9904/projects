<!-- src/views/ArticleCreateView.vue -->

<template>
  <div class="article-create-page">
    <h2>새 게시글 작성</h2>
    <form @submit.prevent="submitArticle">
      <div class="form-group">
        <label for="title">제목</label>
        <input id="title" v-model="title" required />
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model="content" required></textarea>
      </div>
      <button type="submit">작성 완료</button>
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
.article-create-page {
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

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button[type="submit"] {
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>
