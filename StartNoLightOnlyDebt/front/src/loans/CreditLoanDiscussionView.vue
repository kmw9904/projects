<template>
  <div class="discussion-container">
    <h3 class="discussion-title">{{ productName }} 댓글 및 좋아요</h3>

    <!-- 좋아요 버튼 -->
    <div class="like-section">
      <button class="btn btn-like" @click="toggleLike">{{ isLiked ? "💔" : "❤️" }} {{ likes }}</button>
    </div>

    <!-- 댓글 입력 -->
    <div class="comment-input">
      <textarea v-model="newComment" class="form-control" placeholder="댓글을 입력하세요"></textarea>
      <button class="btn btn-primary mt-2" @click="addComment">댓글 달기</button>
    </div>

    <!-- 댓글 리스트 -->
    <ul class="comment-list list-group mt-3">
      <li v-for="(comment, index) in comments" :key="comment.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>
          <strong>{{ comment.username }}</strong>
          : {{ comment.content }}
        </span>
        <button v-if="profile.profile_user.username === comment.username" class="btn btn-sm btn-danger" @click="deleteComment(comment.id)">삭제</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useBankStore } from "@/stores/bank";

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
const store = useBankStore();
const profile = ref(null);

onMounted(() => {
  store.getUserProfile(); // 항상 최신 데이터를 가져오도록 설정
  profile.value = store.profile;
});

// 좋아요 조회
const fetchLikes = function () {
  axios({
    method: "get",
    url: `${API_URL}/credit/${props.productId}/like/`,
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
    url: `${API_URL}/credit/${props.productId}/like/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
  })
    .then((response) => {
      likes.value = response.data.likes;
      isLiked.value = response.data.is_liked;
      console.log(response.data);
    })
    .catch((error) => {
      console.error("좋아요 토글 실패:", error.response?.data || error.message);
    });
};

// 댓글 조회
const fetchComments = function () {
  axios({
    method: "get",
    url: `${API_URL}/credit/${props.productId}/comments/`,
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
  console.log("전송 전 데이터:", {
    content: newComment.value,
  });

  if (!newComment.value.trim()) {
    console.error("댓글 내용이 비어 있습니다.");
    return;
  }

  axios({
    method: "post",
    url: `${API_URL}/credit/${props.productId}/comments/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
    data: {
      content: newComment.value, // 댓글 내용
    },
  })
    .then((response) => {
      console.log("댓글 추가 성공:", response.data);
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
    url: `${API_URL}/credit/${props.productId}/comments/${commentId}/delete/`,
    headers: {
      Authorization: `Token ${token}`, // 인증 토큰 추가
    },
  })
    .then(() => {
      comments.value = comments.value.filter((comment) => comment.id !== commentId); // UI에서 제거
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
.discussion-container {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.discussion-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 15px;
}

.like-section {
  margin-bottom: 20px;
}

.btn-like {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.btn-like:hover {
  background-color: #fa5252;
}

.comment-input {
  margin-top: 20px;
}

.comment-list {
  margin-top: 15px;
}

.list-group-item {
  padding: 10px 15px;
  border-radius: 5px;
}
</style>
