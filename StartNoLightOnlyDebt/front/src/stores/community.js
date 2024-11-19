import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import axios from "axios";

export const useCommunityStore = defineStore("community", () => {
  const API_URL = "http://127.0.0.1:8000";
  const router = useRouter();
  const articles = ref([]);
  const token = ref(null);
  const search_username = ref(null);
  const user_data = ref(null); // TypeScript 타입 제거

  // 로그인 여부 확인
  const isLogin = computed(() => {
    return token.value !== null;
  });

  // 회원가입
  const signUp = (payload) => {
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
        console.log("가입 성공");
        logIn({ username, password: password1 });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  // 로그인
  const logIn = (payload) => {
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
        console.log(res.data);
        token.value = res.data.key;
        search_username.value = username;
        router.push({ name: "home" });
      })
      .catch((err) => {
        console.error(err);
        alert("아이디 또는 비밀번호가 틀렸습니다.");
      });
  };

  // 로그아웃
  const logOut = () => {
    axios({
      method: "post",
      url: `${API_URL}/accounts/logout/`,
    })
      .then(() => {
        token.value = null;
        router.push({ name: "home" });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  // 프로필 수정
  const editProfile = (payload) => {
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
        alert("프로필이 수정되었습니다.");
        router.go(-1);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  // 비밀번호 변경
  const changePassword = (payload) => {
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
        alert("비밀번호가 변경되었습니다. 다시 로그인해주세요.");
        logOut();
      })
      .catch(() => {
        alert("비밀번호 변경에 실패했습니다. 다시 시도해주세요.");
      });
  };

  // 사용자 데이터 가져오기
  const get_user_data = (search_username, errorCallback) => {
    axios({
      method: "get",
      url: `${API_URL}/accounts/profile/get_user_data/${search_username}`,
    })
      .then((res) => {
        user_data.value = res.data;
      })
      .catch(() => {
        alert("없는 사용자입니다.");
        if (errorCallback) errorCallback();
      });
  };

  // 게시글 가져오기
  const getArticles = () => {
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
      .catch((err) => {
        console.error(err);
      });
  };

  // 댓글 생성
  const createComments = (payload) => {
    axios({
      method: "post",
      url: `${API_URL}/articles/comment/${payload.article_pk}/${payload.parent_pk}/`,
      data: {
        content: payload.content,
      },
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((res) => {
        console.log(res.data.message);
        router.go(-1);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  // 댓글 삭제
  const deleteComment = (payload) => {
    axios({
      method: "delete",
      url: `${API_URL}/articles/comment/${payload.article_pk}/${payload.comment_pk}/delete/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then(() => {
        alert("댓글이 삭제되었습니다.");
        router.go(-1);
      })
      .catch((err) => {
        console.error(err);
        alert("댓글 삭제에 실패했습니다.");
      });
  };

  return {
    articles,
    API_URL,
    token,
    isLogin,
    search_username,
    user_data,
    signUp,
    logIn,
    logOut,
    get_user_data,
    editProfile,
    changePassword,
    getArticles,
    createComments,
    deleteComment,
  };
});
