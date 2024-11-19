<template>
  <div>
    <RouterLink :to="{ name: 'ArticleCreateView' }" class="article-create-link">
      <v-tooltip activator="parent" location="start">새 글 작성하기</v-tooltip>
      <v-chip size="x-large" class="article-create-btn mb-1" elevation="3">
        <strong>+</strong>
      </v-chip>
    </RouterLink>
  </div>
</template>

<script>
export default {};
</script>

<style scoped></style>
