<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="8" offset="2">
          <v-sheet elevation="3" class="pa-5 article-list-sheet">
            <v-row class="mb-1 article-list-header">
              <v-col cols="2" align="center">
                <div>글 번호</div>
              </v-col>
              <v-col cols="10" align="center">
                <div>글 내용</div>
              </v-col>
              <v-divider class="article-divider"></v-divider>
            </v-row>
            <ArticleListItem v-for="article in sortedArticles" :key="article.id" :article="article" />
            <v-pagination v-model="page" :length="4" rounded="circle"></v-pagination>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
    <ArticleCreate />
  </div>
</template>

<script setup>
import ArticleListItem from "@/components/ArticleListItem.vue";
import ArticleCreate from "@/components/ArticleCreate.vue";
import { ref, onMounted, computed } from "vue";
import { useCommunityStore } from "@/stores/community";

// 스토어와 상태 관리
const store = useCommunityStore();
const page = ref(1);

// 게시글 정렬
const sortedArticles = computed(() => {
  return store.articles.sort((a, b) => b.id - a.id);
});

// 마운트 시점에서 데이터 가져오기
onMounted(() => {
  store.getArticles();
});
</script>

<style scoped></style>
