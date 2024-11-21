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
        <strong>{{ comment.author }}</strong>
        : {{ comment.text }}
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

const likes = ref(0);
const isLiked = ref(false);
const comments = ref([]);
const newComment = ref("");

// 좋아요 조회 및 토글
const fetchLikes = async () => {
  try {
    const response = await axios.get(`${API_URL}/jeonse/${props.productId}/likes/`);
    likes.value = response.data.likes;
    isLiked.value = response.data.is_liked;
  } catch (error) {
    console.error("좋아요 조회 실패:", error);
  }
};

const toggleLike = async () => {
  try {
    const response = await axios.post(
      `${API_URL}/jeonse/${props.productId}/likes/toggle/`,
      {},
      {
        headers: { Authorization: `Token ${localStorage.getItem("token")}` },
      }
    );
    likes.value = response.data.likes;
    isLiked.value = response.data.is_liked;
  } catch (error) {
    console.error("좋아요 토글 실패:", error);
  }
};

// 댓글 조회, 추가, 삭제
const fetchComments = async () => {
  try {
    const response = await axios.get(`${API_URL}/jeonse/${props.productId}/comments/`);
    comments.value = response.data;
  } catch (error) {
    console.error("댓글 조회 실패:", error);
  }
};

const addComment = async () => {
  if (!newComment.value.trim()) return;

  try {
    const response = await axios.post(`${API_URL}/jeonse/${props.productId}/comments/`, { content: newComment.value }, { headers: { Authorization: `Token ${localStorage.getItem("token")}` } });
    comments.value.push(response.data);
    newComment.value = "";
  } catch (error) {
    console.error("댓글 추가 실패:", error);
  }
};

const deleteComment = async (commentId) => {
  try {
    await axios.delete(`${API_URL}/jeonse/${props.productId}/comments/${commentId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem("token")}` },
    });
    comments.value = comments.value.filter((comment) => comment.id !== commentId);
  } catch (error) {
    console.error("댓글 삭제 실패:", error);
  }
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
