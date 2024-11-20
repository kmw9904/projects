import { defineStore } from "pinia";
import axios from "axios";

export const useArticleStore = defineStore("articles", {
  state: () => ({
    articles: [],
    selectedArticle: null,
  }),

  actions: {
    async fetchArticles() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/articles/");
        this.articles = response.data;
      } catch (error) {
        console.error("게시글을 불러오는 중 오류가 발생했습니다:", error);
      }
    },

    async fetchArticleDetail(articleId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/articles/${articleId}/`);
        this.selectedArticle = response.data;
      } catch (error) {
        console.error("게시글 상세 정보를 가져오는 중 오류가 발생했습니다:", error);
      }
    },

    async createArticle(articleData) {
      try {
        const response = await axios.post("http://127.0.0.1:8000/articles/", articleData, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`, // 인증 토큰 추가
          },
        });
        this.articles.push(response.data);
      } catch (error) {
        console.error("게시글 생성 중 오류가 발생했습니다:", error);
      }
    },

    async deleteArticle(articleId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/articles/${articleId}/`, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        });
        this.articles = this.articles.filter((article) => article.id !== articleId);
      } catch (error) {
        console.error("게시글 삭제 중 오류가 발생했습니다:", error);
      }
    },

    async createComment(articleId, commentData) {
      try {
        await axios.post(`http://127.0.0.1:8000/articles/${articleId}/comments/`, commentData, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        });
        await this.fetchArticleDetail(articleId); // 댓글 추가 후 게시글 상세 업데이트
      } catch (error) {
        console.error("댓글 작성 중 오류가 발생했습니다:", error);
      }
    },

    async deleteComment(articleId, commentId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/articles/${articleId}/comments/${commentId}/`, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        });
        await this.fetchArticleDetail(articleId); // 댓글 삭제 후 게시글 상세 업데이트
      } catch (error) {
        console.error("댓글 삭제 중 오류가 발생했습니다:", error);
      }
    },
  },
});
