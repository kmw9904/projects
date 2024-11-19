<template>
  <div>
    <v-container>
      <v-row class="d-flex justify-center mt-4">
        <h1 class="article-create-header mb-7 mt-1 half-highlight">새 글 작성</h1>
      </v-row>
      <v-row>
        <v-col cols="8" offset="2">
          <v-sheet elevation="2" class="article-create-wrapper py-10 px-10">
            <v-text-field v-model="title" label="제목" variant="solo-filled" />
            <v-textarea v-model="content" label="내용" variant="solo-filled" />
            <v-file-input v-model="img" label="파일 첨부하기" variant="solo-filled" />
            <div class="d-flex flex-row-reverse">
              <v-chip elevation="1" color="primary" @click="createArticle">게시하기</v-chip>
              <v-chip elevation="1" class="mr-2" color="red" @click="goBack">취소하기</v-chip>
            </div>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { ref } from "vue";
import { useBankStore } from "@/stores/bank";
import { useRouter } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const store = useBankStore();
    const router = useRouter();
    const title = ref("");
    const content = ref("");
    const img = ref([]);

    const goBack = () => {
      if (title.value || content.value) {
        if (confirm("작성 중인 글이 저장되지 않습니다. 정말 떠나시겠습니까?")) {
          router.go(-1);
        }
      } else {
        router.go(-1);
      }
    };

    const createArticle = () => {
      axios({
        method: "post",
        url: `${store.API_URL}/articles/`,
        data: {
          title: title.value,
          content: content.value,
        },
        headers: {
          Authorization: `Token ${store.token}`,
        },
      })
        .then(() => {
          store.getArticles();
          router.push({ name: "article" });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return { title, content, img, goBack, createArticle };
  },
};
</script>

<style scoped></style>
