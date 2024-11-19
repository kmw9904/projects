import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

export const useBankStore = defineStore(
  "bank",
  () => {
    // URL 설정
    const API_URL = "http://127.0.0.1:8000";

    // Vue Router 설정
    const router = useRouter();

    // 상태 관리
    const isLoggedIn = ref(false); // 로그인 상태
    const token = ref(localStorage.getItem("token") || null); // 로컬스토리지에서 토큰 확인
    const profile = ref(null); // 유저 프로필 데이터

    // ------------------ 주요 기능들 ------------------

<<<<<<< HEAD
    // 게시글 목록 데이터 저장
    const creditLoans = ref(null);
    const jeonses = ref(null);
    const mortgages = ref(null);

    const getCreditLoan = function () {
=======
    // 로그인 요청
    const Login = function (payload) {
      const { username, password } = payload;
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: { username, password },
      })
        .then((res) => {
          console.log("로그인 성공:", res.data);
          token.value = res.data.key; // 토큰 저장
          localStorage.setItem("token", res.data.key); // 로컬스토리지에 저장
          isLoggedIn.value = true; // 로그인 상태 갱신
          router.push({ name: "MainView" }); // 메인 페이지로 이동
        })
        .catch((err) => {
          console.error("로그인 실패:", err.response?.data || err.message);
        });
    };

<<<<<<< HEAD
    const getJeonse = function () {
=======
    // 로그아웃 요청
    const Logout = function () {
      if (!token.value) {
        console.warn("로그아웃 실패: 토큰이 없습니다.");
        return;
      }
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
        headers: {
          Authorization: `Token ${token.value}`, // 인증 토큰 추가
        },
      })
        .then(() => {
          console.log("로그아웃 성공");
          token.value = null; // 토큰 제거
          localStorage.removeItem("token"); // 로컬스토리지에서 삭제
          isLoggedIn.value = false; // 로그인 상태 초기화
          profile.value = null; // 프로필 데이터 초기화
          router.push({ name: "LoginView" }); // 로그인 페이지로 이동
        })
        .catch((err) => {
          console.error("로그아웃 실패:", err.response?.data || err.message);
        });
    };

<<<<<<< HEAD
    const getMortgage = function () {
=======
    // 유저 프로필 가져오기
    const getUserProfile = function () {
      if (!token.value) {
        console.warn("프로필 가져오기 실패: 토큰이 없습니다.");
        return;
      }
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
      axios({
        method: "get",
        url: `${API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`, // 인증 토큰 추가
        },
      })
        .then((res) => {
          console.log("프로필 가져오기 성공:", res.data);
          profile.value = res.data; // 프로필 데이터 저장
        })
        .catch((err) => {
          console.error("프로필 가져오기 실패:", err.response?.data || err.message);
        });
    };

    // 회원가입 요청
    const SignUp = function (payload) {
      const { username, password1, password2, email, name, preferred_banks } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
          email,
          name, // name 데이터 포함
          preferred_banks, // 선호 은행 포함
        },
      })
        .then((res) => {
          console.log("회원가입 성공");
        })
        .catch((err) => {
          console.error("회원가입 실패:", err.response?.data || err.message);
        });
    };

    // 은행 목록 가져오기
    const banks = ref([]);
    const getBanks = function () {
      return axios({
        method: "get",
        url: `${API_URL}/api/v1/banks/`,
      })
        .then((res) => {
<<<<<<< HEAD
          banks.value = res.data;
          return res.data;
        })
        .catch((err) => {
          console.error("은행 목록 가져오기 실패:", err);
          throw err;
        });
    };

    // 회원가입 요청 액션
    const SignUp = function (payload) {
      const { username, password1, password2, email, name, preferred_banks } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
          email,
          name,
          preferred_banks,
        },
      })
        .then(() => {
          const password = password1;
          Login({ username, password });
        })
        .catch((err) => console.error(err));
=======
          console.log("은행 목록 가져오기 성공:", res.data);
          banks.value = res.data; // 받은 데이터를 저장
          return res.data; // 반환
        })
        .catch((err) => {
          console.error("은행 목록 가져오기 실패:", err.response?.data || err.message);
          throw err; // 에러 던지기
        });
    };

    // ------------------ 게시글 관리 기능 ------------------

    const creditLoans = ref(null);
    const getCreditLoan = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/fetch-financial-data/`,
      })
        .then((res) => {
          creditLoans.value = res.data;
        })
        .catch((err) => console.error("Credit Loan 가져오기 실패:", err));
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
    };

    const jeonses = ref(null);
    const getJeonse = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/fetch-financial-data/`,
      })
        .then((res) => {
<<<<<<< HEAD
          token.value = res.data.key;
          isLoggedIn.value = true;
          router.push({ name: "MainView" });
        })
        .catch((err) => console.error(err));
=======
          jeonses.value = res.data;
        })
        .catch((err) => console.error("Jeonse 가져오기 실패:", err));
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
    };

    const mortgages = ref(null);
    const getMortgage = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/fetch-financial-data/`,
      })
<<<<<<< HEAD
        .then(() => {
          isLoggedIn.value = false;
        })
        .catch((err) => console.error(err));
    };

    // Community 관련 추가
    const articles = ref([]);
    const search_username = ref(null);
    const user_data = ref(null);

    const isLogin = computed(() => {
      return token.value !== null;
    });

    const signUpCommunity = function (payload) {
      const { username, nickname, email, password1, password2 } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          nickname,
          email,
          password1,
          password2,
        },
      })
        .then(() => {
          Login({ username, password: password1 });
        })
        .catch((err) => console.error(err));
    };

    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          articles.value = res.data;
        })
        .catch((err) => console.error(err));
    };

    const editProfile = function (payload) {
      const { nickname, email } = payload;
      axios({
        method: "put",
        url: `${API_URL}/accounts/profile/edit/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: {
          nickname,
          email,
        },
      })
        .then(() => {
          router.go(-1);
        })
        .catch((err) => console.error(err));
    };

    const changePassword = function (payload) {
      const { old_password, new_password1, new_password2 } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/password/change/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: {
          old_password,
          new_password1,
          new_password2,
        },
      })
        .then(() => {
          Logout();
        })
        .catch(() => console.error("비밀번호 변경 실패"));
    };

    const createComments = function (payload) {
      axios({
        method: "post",
        url: `${API_URL}/articles/comment/${payload.article_pk}/${payload.parent_pk}/`,
        data: { content: payload.content },
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then(() => router.go(-1))
        .catch((err) => console.error(err));
    };

    const deleteComment = function (payload) {
      axios({
        method: "delete",
        url: `${API_URL}/articles/comment/${payload.article_pk}/${payload.comment_pk}/delete/`,
        headers: { Authorization: `Token ${token.value}` },
      })
        .then(() => router.go(-1))
        .catch((err) => console.error(err));
    };

    return {
      // Bank 관련
      SignUp,
      Login,
      Logout,
      isLoggedIn,
=======
        .then((res) => {
          mortgages.value = res.data;
        })
        .catch((err) => console.error("Mortgage 가져오기 실패:", err));
    };

    // ------------------ 초기화 ------------------
    const initializeState = function () {
      const storedToken = localStorage.getItem("token");
      if (storedToken) {
        token.value = storedToken;
        isLoggedIn.value = true;
      } else {
        token.value = null;
        isLoggedIn.value = false;
      }
    };

    // 초기 상태 설정
    initializeState();

    return {
      Login,
      Logout,
      SignUp,
      getUserProfile,
      token,
      isLoggedIn,
      profile,
      banks,
      getBanks,
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
      creditLoans,
      getCreditLoan,
      jeonses,
      getJeonse,
      mortgages,
      getMortgage,
<<<<<<< HEAD
      banks,
      getBanks,
      // Community 관련
      articles,
      isLogin,
      search_username,
      user_data,
      signUpCommunity,
      getArticles,
      editProfile,
      changePassword,
      createComments,
      deleteComment,
=======
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
    };
  },
  {
    persist: {
      key: "bank",
      storage: window.localStorage,
    },
  }
);
