<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="2" class="d-flex justify-center align-center">
          {{ article?.id }}
        </v-col>
        <v-col cols="10">
          <div>
            <div class="article-list-title">
              <RouterLink :to="{ name: 'ArticleDetailView', params: { id: article?.id } }" class="article-list-title">
                {{ article?.title }}
              </RouterLink>
            </div>
            <div class="d-flex">
              <div class="mr-2">{{ article?.user.nickname }}</div>
              <div>|</div>
              <div class="ml-2">{{ article?.created_at.substr(0, 10) }}</div>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { RouterLink } from "vue-router";

export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
