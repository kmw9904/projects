import axios from "axios";

// Axios 인스턴스 생성
const instance = axios.create({
  baseURL: "http://127.0.0.1:8000", // Django 서버 주소
  xsrfCookieName: "csrftoken", // Django 기본값
  xsrfHeaderName: "X-CSRFToken", // Django 기본값
});

// CSRF 토큰 설정
if (window.csrfToken) {
  instance.defaults.headers.common["X-CSRFToken"] = window.csrfToken;
}

export default instance;
