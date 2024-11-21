<template>
  <div>
    <h3>{{ productName }} 댓글 및 좋아요</h3>

    <!-- 좋아요 버튼 -->
    <button @click="toggleLike">{{ isLiked ? "💔 좋아요 취소" : "❤️ 좋아요" }} {{ likes }}</button>

    <!-- 댓글 입력 -->
    <div>
      <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
      <button @click="addComment">댓글 달기</button>
    </div>

    <!-- 댓글 리스트 -->
    <ul>
      <li v-for="(comment, index) in comments" :key="comment.id">
        <strong>{{ comment.user }}</strong>
        : {{ comment.content }}
        <button @click="deleteComment(comment.id)">삭제</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// Props
const props = defineProps({
  productId: String,
  productName: String,
});

const API_URL = "http://127.0.0.1:8000/interactions";
const token = localStorage.getItem("token");

const likes = ref(0);
const isLiked = ref(false);
const comments = ref([]);
const newComment = ref("");

// 좋아요 조회
const fetchLikes = function () {
  axios({
    method: "get",
    url: `${API_URL}/mortgage/${props.productId}/like/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
  })
    .then((response) => {
      likes.value = response.data.likes;
      isLiked.value = response.data.is_liked;
    })
    .catch((error) => {
      console.error("좋아요 조회 실패:", error.response?.data || error.message);
    });
};

// 좋아요 토글
const toggleLike = function () {
  axios({
    method: "post",
    url: `${API_URL}/mortgage/${props.productId}/like/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
  })
    .then((response) => {
      likes.value = response.data.likes;
      isLiked.value = response.data.is_liked;
    })
    .catch((error) => {
      console.error("좋아요 토글 실패:", error.response?.data || error.message);
    });
};

// 댓글 조회
const fetchComments = function () {
  axios({
    method: "get",
    url: `${API_URL}/mortgage/${props.productId}/comments/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
  })
    .then((response) => {
      comments.value = response.data;
    })
    .catch((error) => {
      console.error("댓글 조회 실패:", error.response?.data || error.message);
    });
};

// 댓글 추가
const addComment = function () {
  if (!newComment.value.trim()) {
    console.error("댓글 내용이 비어 있습니다.");
    return;
  }

  axios({
    method: "post",
    url: `${API_URL}/mortgage/${props.productId}/comments/add/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
    data: {
      content: newComment.value, // 댓글 내용
    },
  })
    .then((response) => {
      comments.value.push(response.data);
      newComment.value = ""; // 입력 필드 초기화
    })
    .catch((error) => {
      console.error("댓글 추가 실패:", error.response?.data || error.message);
    });
};

// 댓글 삭제
const deleteComment = function (commentId) {
  axios({
    method: "delete",
    url: `${API_URL}/mortgage/${props.productId}/comments/${commentId}/delete/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
  })
    .then(() => {
      comments.value = comments.value.filter((comment) => comment.id !== commentId);
    })
    .catch((error) => {
      console.error("댓글 삭제 실패:", error.response?.data || error.message);
    });
};

// 초기 데이터 로드
onMounted(() => {
  fetchLikes();
  fetchComments();
});
</script>

<style scoped>
textarea {
  width: 100%;
  margin-bottom: 10px;
}

button {
  margin: 5px 0;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 5px;
  border-bottom: 1px solid #ddd;
  padding: 5px 0;
}
</style>
