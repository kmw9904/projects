<template>
  <div class="article-detail-wrapper">
    <v-container>
      <v-row>
        <v-col cols="8" offset="2">
          <v-sheet elevation="3" class="article-detail-sheet pa-10">
            <v-chip @click="goBack" class="mb-5">뒤로 가기</v-chip>
            <div v-if="article">
              <p class="article-detail-title mb-7">{{ article.article.title }}</p>
              <div class="d-flex mb-7">
                <p class="article-detail-detail mr-5">
                  <strong>작성자</strong>
                  <div>{{ article.article.user.nickname }}</div>
                </p>
                <p class="article-detail-detail mr-5">
                  <strong>작성일시</strong>
                  <div>
                    {{ article.article.created_at.slice(0, 4) }}년
                    {{ article.article.created_at.slice(5, 7) }}월
                    {{ article.article.created_at.slice(8, 10) }}일
                    {{ article.article.created_at.slice(11, 13) }}시
                    {{ article.article.created_at.slice(14, 16) }}분
                  </div>
                </p>
                <p class="article-detail-detail">
                  <strong> 마지막 수정일시 </strong>
                  <div>
                    {{ article.article.updated_at.slice(0, 4) }}년
                    {{ article.article.updated_at.slice(5, 7) }}월
                    {{ article.article.updated_at.slice(8, 10) }}일
                    {{ article.article.updated_at.slice(11, 13) }}시
                    {{ article.article.updated_at.slice(14, 16) }}분
                  </div>
                </p>
              </div>
              <p class="article-detail-content mb-5 pa-3">{{ article.article.content }}</p>
              <div class="d-flex flex-row-reverse">
                <v-chip elevation="2" @click="deleteArticle" color="red" class="ml-2"> 글 삭제 </v-chip>
                <v-chip elevation="2" color="primary"> 글 수정 </v-chip>
              </div>
            </div>
            <!-- 댓글 작성 폼 -->
            <div class="mt-6">
              <div class="text-xl font-bold mb-3">댓글</div>
              <div class="d-flex">
                <v-text-field
                  v-model.trim="newComment"
                  class="article-detail-comment-input mr-4"
                  placeholder="댓글을 입력하세요"
                ></v-text-field>
                <v-chip @click="submitComment(0)" elevation="2" class="mt-2 text-black font-bold py-2 px-4">
                  작성
                </v-chip>
              </div>
            </div>
            <div v-if="article">
              <p v-for="comment in article.comments" class="mb-5">
                <div class="article-detail-comment-user">
                  <strong>{{ comment.user.nickname }}</strong>
                </div>
                <div class="d-flex justify-space-between">
                  <div>{{ comment.content }}</div>
                  <v-chip size="small" @click="deleteComment(comment)">x</v-chip>
                </div>
              </p>
            </div>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useBankStore } from "@/stores/bank";
import { useRoute, useRouter } from "vue-router";

export default {
  setup() {
    const store = useBankStore();
    const route = useRoute();
    const router = useRouter();
    const article = ref();
    const newComment = ref("");

    onMounted(() => {
      axios({
        method: "get",
        url: `${store.API_URL}/articles/${route.params.id}/`,
        headers: {
          Authorization: `Token ${store.token}`,
        },
      })
        .then((res) => {
          article.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    });

    const goBack = () => {
      router.go(-1);
    };

    const deleteArticle = () => {
      axios({
        method: "delete",
        url: `${store.API_URL}/articles/${route.params.id}/`,
        headers: { Authorization: `Token ${store.token}` },
      })
        .then(() => {
          store.getArticles();
          router.push({ name: "article" });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const submitComment = (parent_pk) => {
      if (!newComment.value.trim()) {
        alert("댓글 내용을 입력해주세요.");
        return;
      }
      store.createComments({
        article_pk: route.params.id,
        content: newComment.value,
        parent_pk,
      });
      newComment.value = "";
    };

    const deleteComment = (comment) => {
      if (confirm("댓글을 삭제하시겠습니까?")) {
        const payload = {
          article_pk: article.value.article.id,
          comment_pk: comment.id,
        };

        store.deleteComment(payload)
          .then(() => {
            return axios({
              method: "get",
              url: `${store.API_URL}/articles/${route.params.id}/`,
              headers: {
                Authorization: `Token ${store.token}`,
              },
            });
          })
          .then((res) => {
            article.value = res.data;
          })
          .catch((err) => {
            console.error(err);
          });
      }
    };

    return { article, newComment, goBack, deleteArticle, submitComment, deleteComment };
  },
};
</script>

<style scoped></style>
