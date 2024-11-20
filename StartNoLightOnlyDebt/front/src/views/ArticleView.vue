<template>
  <div>
    <h1>커뮤니티</h1>
    <ArticleList />
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
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>
