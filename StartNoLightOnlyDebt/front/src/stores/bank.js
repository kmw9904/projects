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

    // CreditLoan 게시글 목록 데이터 저장
    const creditLoans = ref(null);
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

    // Jeonse 게시글 목록 데이터 저장
    const jeonses = ref(null);
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

    // CreditLoan 게시글 목록 데이터 저장
    const mortgages = ref(null);
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
          console.log("은행 목록 가져오기 성공:", res.data);
          banks.value = res.data; // 받은 데이터를 banks에 저장
          return res.data; // 명시적으로 데이터를 반환
        })
        .catch((err) => {
          console.error("은행 목록 가져오기 실패:", err);
          throw err; // 에러를 던져서 호출자에게 알림
        });
    };

    // 회원가입 요청 액션
    const SignUp = function (payload) {
      const { username, password1, password2, email, name } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
          email,
          name,
          preferred_banks, // 선택된 선호 은행 추가
        },
      })
        .then((res) => {
          console.log("회원가입이 완료 되었습니다.");
          const password = password1;
          Login({ username, password });
        })
        .catch((err) => console.log(err));
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
          console.log("로그인 완료");
          token.value = res.data.key;
          // 로그인 상태 업데이트
          isLoggedIn.value = true;
          // 메인 페이지로 이동
          router.push({ name: "MainView" });
        })
        .catch((err) => console.log(err.data));
    };

    const Logout = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
      })
        .then(() => {
          console.log("로그아웃 완료");
          // 로그인 상태 초기화
          isLoggedIn.value = false;
        })
        .catch((err) => {
          console.log("로그아웃 실패:", err.data);
        });
    };
    return { SignUp, Login, token, Logout, isLoggedIn, creditLoans, getCreditLoan, jeonses, getJeonse, mortgages, getMortgage, banks, getBanks };
  },
  {
    // 기본 설정으로 locakStorage에 데이터를 저장하도록 구성해야 함
    persist: {
      key: "bank", // localStorage에 저장될 키 이름
      storage: window.localStorage, // localStorage에 저장
    },
  }
);
