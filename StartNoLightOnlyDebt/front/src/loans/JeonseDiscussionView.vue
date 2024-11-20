<template>
    <div>
      <h3>댓글 및 좋아요</h3>
  
      <!-- 좋아요 버튼 -->
      <button @click="toggleLike">👍 좋아요 {{ likes }}</button>
  
      <!-- 댓글 입력 -->
      <div>
        <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
        <button @click="addComment">댓글 달기</button>
      </div>
  
      <!-- 댓글 리스트 -->
      <ul>
        <li v-for="(comment, index) in comments" :key="index">
          <strong>{{ comment.author }}</strong>
          : {{ comment.text }}
          <button @click="deleteComment(index)">삭제</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const likes = ref(0); // 좋아요 카운트
  const isLiked = ref(false); // 좋아요 여부
  const comments = ref([]); // 댓글 목록
  const newComment = ref(""); // 새 댓글
  
  // 좋아요 토글
  const toggleLike = () => {
    if (isLiked.value) {
      likes.value--;
    } else {
      likes.value++;
    }
    isLiked.value = !isLiked.value;
  };
  
  // 댓글 추가
  const addComment = () => {
    if (newComment.value.trim() === "") {
      alert("댓글 내용을 입력하세요.");
      return;
    }
    comments.value.push({
      author: "익명", // 기본 작성자 이름 (사용자 시스템과 연동 가능)
      text: newComment.value.trim(),
    });
    newComment.value = "";
  };
  
  // 댓글 삭제
  const deleteComment = (index) => {
    comments.value.splice(index, 1);
  };
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
  