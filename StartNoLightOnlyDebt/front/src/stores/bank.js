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

    // 로그인 요청
    const Login = function (payload) {
      const { username, password } = payload;

      return axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: { username, password },
      })
        .then((res) => {
          console.log("로그인 성공:", res.data);
          token.value = res.data.key; // 토큰 저장
          localStorage.setItem("token", res.data.key); // 로컬스토리지에 저장
          isLoggedIn.value = true; // 로그인 상태 갱신

          // 프로필 정보 가져오기
          return getUserProfile();
        })
        .then(() => {
          router.push({ name: "MainView" }); // 메인 페이지로 이동
        })
        .catch((err) => {
          console.error("로그인 실패:", err.response?.data || err.message);
          throw err; // 에러를 상위로 전달
        });
    };

    // 로그아웃 요청
    const Logout = function () {
      if (!token.value) {
        console.warn("로그아웃 실패: 토큰이 없습니다.");
        return;
      }

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
          // 추가 디버깅
          if (err.response) {
            console.log("에러 응답 데이터:", err.response.data);
          }
        });
    };

    // 유저 프로필 가져오기
    const getUserProfile = function () {
      if (!token.value) {
        console.warn("프로필 가져오기 실패: 토큰이 없습니다.");
        return Promise.reject(new Error("토큰이 없습니다.")); // 실패 시 에러 반환
      }

      return axios({
        method: "get",
        url: `${API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`, // 인증 토큰 추가
        },
      })
        .then((res) => {
          profile.value = res.data; // 프로필 데이터 저장
          return res.data; // 성공 데이터 반환
        })
        .catch((err) => {
          console.error("프로필 가져오기 실패:", err.response?.data || err.message);
          throw err; // 에러 던지기
        });
    };
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
          preferred_banks: preferred_banks || [], // 선호 은행 데이터
        },
      })
        .then((res) => {
          console.log("회원가입 성공:", res.data);

          // 회원가입 성공 후 자동 로그인
          const loginPayload = {
            username, // 회원가입 시 입력했던 사용자 이름
            password: password1, // 회원가입 시 사용한 비밀번호
          };

          // 로그인 호출
          Login(loginPayload)
            .then(() => {
              // 로그인 성공 후 프로필 데이터 가져오기
              return getUserProfile();
            })
            .then(() => {
              // 프로필 페이지로 이동
              router.push({ name: "AccountView" });
            })
            .catch((err) => {
              console.error("로그인 또는 프로필 가져오기 실패:", err.response?.data || err.message);
            });
        })
        .catch((err) => {
          console.error("회원가입 실패:", err.response?.data || err.message);
        });
    };

    // 비밀번호 변경
    const changePassword = function (payload) {
      return axios({
        method: "post",
        url: `${API_URL}/accounts/password/change/`,
        data: {
          old_password: payload.oldPassword,
          new_password1: payload.newPassword1,
          new_password2: payload.newPassword2,
        },
        headers: {
          Authorization: `Token ${token.value}`, // 인증 토큰 추가
        },
      })
        .then((res) => {
          console.log("비밀번호 변경 성공:", res.data);
          router.push({ name: "AccountView" });
          return res.data; // 성공 데이터 반환
        })
        .catch((err) => {
          console.error("비밀번호 변경 실패:", err.response?.data || err.message);
          throw err; // 에러 던지기
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
          console.log("은행 목록 가져오기 성공:", res.data);
          banks.value = res.data; // 받은 데이터를 저장
          return res.data; // 반환
        })
        .catch((err) => {
          console.error("은행 목록 가져오기 실패:", err.response?.data || err.message);
          throw err; // 에러 던지기
        });
    };

    // 사용자 선호 은행 가져오기
    const selectedBanks = ref([]); // 사용자 선호 은행 ID 리스트
    const getPreferredBanks = function () {
      return axios({
        method: "get",
        url: `${API_URL}/accounts/preferred-banks/`,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          console.log("전체 은행 목록 가져오기 성공:", res.data);
          return res.data; // 응답 데이터를 그대로 반환
        })
        .catch((err) => {
          console.error("전체 은행 목록 가져오기 실패:", err.response?.data || err.message);
          throw err; // 에러를 던져 상위에서 처리
        });
    };

    const updatePreferredBanks = function (newBanks) {
      return axios({
        method: "put",
        url: `${API_URL}/accounts/preferred-banks/`,
        data: {
          preferred_banks: newBanks,
        },
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          console.log("선호 은행 업데이트 성공:", res.data);
          return res.data; // 성공적으로 업데이트된 데이터 반환
        })
        .catch((err) => {
          console.error("선호 은행 업데이트 실패:", err.response?.data || err.message);
          throw err; // 에러를 던져 상위에서 처리
        });
    };
    // ------------------ 게시글 관리 기능 ------------------

    const creditLoans = ref(null);
    const getCreditLoan = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/credit-loans/`,
        headers: {
          Authorization: `Token ${token.value}`, // 인증 토큰 추가
        },
      })
        .then((res) => {
          creditLoans.value = res.data;
        })
        .catch((err) => console.error("Credit Loan 가져오기 실패:", err));
    };

    const jeonses = ref(null);
    const getJeonse = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/jeonse-loans/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          jeonses.value = res.data;
        })
        .catch((err) => console.error("Jeonse Loan 가져오기 실패:", err));
    };

    const mortgages = ref(null);
    const getMortgage = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/mortgage-loans/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          mortgages.value = res.data;
        })
        .catch((err) => console.error("Mortgage Loan 가져오기 실패:", err));
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
      creditLoans,
      getCreditLoan,
      jeonses,
      getJeonse,
      mortgages,
      getMortgage,
      changePassword,
      getPreferredBanks,
      updatePreferredBanks,
      selectedBanks,
    };
  },
  {
    persist: {
      key: "bank",
      storage: window.localStorage,
    },
  }
);
