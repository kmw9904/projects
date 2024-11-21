import { defineStore } from "pinia";
import axios from "axios";

export const useArticleStore = defineStore("articles", {
  state: () => ({
    articles: [],
    selectedArticle: null,
  }),

  actions: {
    fetchArticles() {
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/articles/",
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((response) => {
          console.log("게시글 목록 가져오기 성공:", response.data);
          this.articles = response.data;
        })
        .catch((error) => {
          console.error("게시글을 불러오는 중 오류가 발생했습니다:", error.response?.data || error.message);
        });
    },

    fetchArticleDetail(articleId) {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/articles/${articleId}/`,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((response) => {
          console.log("게시글 상세 정보 가져오기 성공:", response.data);
          this.selectedArticle = response.data;
        })
        .catch((error) => {
          console.error("게시글 상세 정보를 가져오는 중 오류가 발생했습니다:", error.response?.data || error.message);
        });
    },

    createArticle(articleData) {
      axios({
        method: "post",
        url: "http://127.0.0.1:8000/articles/",
        data: articleData,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((response) => {
          console.log("게시글 생성 성공:", response.data);
          this.articles.push(response.data);
        })
        .catch((error) => {
          console.error("게시글 생성 중 오류가 발생했습니다:", error.response?.data || error.message);
        });
    },

    deleteArticle(articleId) {
      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/articles/${articleId}/`,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then(() => {
          console.log("게시글 삭제 성공");
          this.articles = this.articles.filter((article) => article.id !== articleId);
        })
        .catch((error) => {
          console.error("게시글 삭제 중 오류가 발생했습니다:", error.response?.data || error.message);
        });
    },

    createComment(articleId, commentData) {
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/articles/${articleId}/comments/`,
        data: commentData,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then(() => {
          console.log("댓글 작성 성공");
          this.fetchArticleDetail(articleId); // 댓글 추가 후 게시글 상세 업데이트
        })
        .catch((error) => {
          console.error("댓글 작성 중 오류가 발생했습니다:", error.response?.data || error.message);
        });
    },

    deleteComment(articleId, commentId) {
      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/articles/${articleId}/comments/${commentId}/`,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then(() => {
          console.log("댓글 삭제 성공");
          this.fetchArticleDetail(articleId); // 댓글 삭제 후 게시글 상세 업데이트
        })
        .catch((error) => {
          console.error("댓글 삭제 중 오류가 발생했습니다:", error.response?.data || error.message);
        });
    },

    toggleLike(articleId) {
      axios
        .post(`http://127.0.0.1:8000/articles/${articleId}/toggle-like/`, null, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        })
        .then((response) => {
          console.log(response.data.message);
          const article = this.articles.find((a) => a.id === articleId);
          if (article) {
            article.likes_count = response.data.likes_count;
            article.is_liked = !article.is_liked;
          }
          if (this.selectedArticle?.id === articleId) {
            this.selectedArticle.likes_count = response.data.likes_count;
            this.selectedArticle.is_liked = !this.selectedArticle.is_liked;
          }
        })
        .catch((error) => {
          console.error("좋아요 기능 오류:", error.response?.data || error.message);
        });
    },
  },
  getters: {
    topLikedArticle(state) {
      return state.articles.length ? state.articles.reduce((top, current) => (current.likes_count > (top.likes_count || 0) ? current : top), {}) : null;
    },
  },
});
