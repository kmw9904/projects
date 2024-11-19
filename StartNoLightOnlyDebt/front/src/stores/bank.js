import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

export const useBankStore = defineStore(
  "bank",
  () => {
    // URL 설정
    const API_URL = "http://127.0.0.1:8000";

    // 로그인 성공 후 자동으로 메인페이지로 이동하기 위한 router 변수 설정
    const router = useRouter();

    // 로그인 상태 관리
    const isLoggedIn = ref(false);

    // 반응형 변수 token 선언 및 토큰 저장
    const token = ref(null);

    // 게시글 목록 데이터 저장
    const creditLoans = ref(null);
    const jeonses = ref(null);
    const mortgages = ref(null);

    const getCreditLoan = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/fetch-financial-data/`,
      })
        .then((res) => {
          creditLoans.value = res.data;
        })
        .catch((err) => console.log(err));
    };

    const getJeonse = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/fetch-financial-data/`,
      })
        .then((res) => {
          jeonses.value = res.data;
        })
        .catch((err) => console.log(err));
    };

    const getMortgage = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/fetch-financial-data/`,
      })
        .then((res) => {
          mortgages.value = res.data;
        })
        .catch((err) => console.log(err));
    };

    // 은행 목록 가져오기
    const banks = ref([]);
    const getBanks = function () {
      return axios({
        method: "get",
        url: `${API_URL}/api/v1/banks/`,
      })
        .then((res) => {
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
    };

    // 로그인 요청 액션
    const Login = function (payload) {
      const { username, password } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          token.value = res.data.key;
          isLoggedIn.value = true;
          router.push({ name: "MainView" });
        })
        .catch((err) => console.error(err));
    };

    const Logout = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
      })
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
      creditLoans,
      getCreditLoan,
      jeonses,
      getJeonse,
      mortgages,
      getMortgage,
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
    };
  },
  {
    persist: {
      key: "bank",
      storage: window.localStorage,
    },
  }
);
