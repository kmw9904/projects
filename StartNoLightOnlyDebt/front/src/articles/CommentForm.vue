<template>
  <form @submit.prevent="submitComment">
    <input v-model="content" type="text" placeholder="댓글 작성" required />
    <button type="submit">댓글 추가</button>
  </form>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";

const store = useArticleStore();
const content = ref("");
const props = defineProps({
  articleId: {
    type: Number,
    required: true,
  },
});

const submitComment = async () => {
  await store.createComment(props.articleId, { content: content.value });
  content.value = "";
  emit("refresh");
};
</script>

<style scoped>
form {
  margin-top: 10px;
}
input {
  width: 100%;
}
button {
  margin-top: 5px;
}
</style>
