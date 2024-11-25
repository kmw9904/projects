import { createRouter, createWebHistory } from "vue-router";

// 계정 관련 페이지
import SignUpView from "@/accounts/SignUpView.vue"; // POST: 회원가입 요청
import LoginView from "@/accounts/LoginView.vue"; // POST: 로그인 요청
import AccountView from "@/accounts/AccountView.vue"; // GET: 사용자 정보 요청
import PasswordChangeView from "@/accounts/PasswordChangeView.vue"; // POST: 비밀번호 변경 요청
import PreferredBanksView from "@/accounts/PreferredBanksView.vue"; // GET/POST: 선호 은행 조회 및 변경

// 메인 및 공통 페이지
import MainView from "@/views/MainView.vue"; // GET: 메인 페이지 정보
import MapView from "@/views/MapView.vue"; // GET: 지도 관련 데이터 요청
import ExchangeView from "@/components/ExchangeView.vue"; // GET: 환율 데이터 요청
import AlgorithmView from "@/algorithm/AlgorithmView.vue"; // GET: 알고리즘 관련 데이터 요청

// 대출 관련 페이지
import JeonseView from "@/loans/JeonseView.vue"; // GET: 전세 대출 상품 목록 요청
import CreditLoanView from "@/loans/CreditLoanView.vue"; // GET: 신용 대출 상품 목록 요청
import MortgageView from "@/loans/MortgageView.vue"; // GET: 주택담보대출 상품 목록 요청
import MortgageDetailView from "@/loans/MortgageDetailView.vue"; // GET: 특정 주택담보대출 상세 정보 요청
import JeonseDetailView from "@/loans/JeonseDetailView.vue"; // GET: 특정 전세 대출 상세 정보 요청
import CreditLoanDetailView from "@/loans/CreditLoanDetailView.vue"; // GET: 특정 신용 대출 상세 정보 요청

// 게시글 관련 페이지
import ArticleView from "@/views/ArticleView.vue"; // GET: 게시글 목록 요청
import ArticleCreate from "@/views/ArticleCreate.vue"; // POST: 게시글 생성 요청
import ArticleDetail from "@/views/ArticleDetail.vue"; // GET: 특정 게시글 상세 정보 요청

// 논의 페이지 (대출별)
import CreditLoanDiscussionView from "@/loans/CreditLoanDiscussionView.vue"; // GET/POST: 신용 대출 논의 게시판
import JeonseDiscussionView from "@/loans/JeonseDiscussionView.vue"; // GET/POST: 전세 대출 논의 게시판
import MortgageDiscussionView from "@/loans/MortgageDiscussionView.vue"; // GET/POST: 주택담보대출 논의 게시판

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 회원가입
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView, // POST: 회원가입 요청
    },
    // 로그인
    {
      path: "/login",
      name: "LoginView",
      component: LoginView, // POST: 로그인 요청
    },
    // 메인 페이지
    {
      path: "/",
      name: "MainView",
      component: MainView, // GET: 메인 페이지 정보
    },
    // 지도 페이지
    {
      path: "/map",
      name: "map",
      component: MapView, // GET: 지도 관련 데이터 요청
    },
    // 환율 페이지
    {
      path: "/exchange",
      name: "ExchangeView",
      component: ExchangeView, // GET: 환율 데이터 요청
    },
    // 알고리즘 페이지
    {
      path: "/algorithm",
      name: "AlgorithmView",
      component: AlgorithmView, // GET: 알고리즘 관련 데이터 요청
    },
    // 프로필 페이지
    {
      path: "/profile",
      name: "AccountView",
      component: AccountView, // GET: 사용자 정보 요청
    },
    // 비밀번호 변경
    {
      path: "/change-password",
      name: "PasswordChangeView",
      component: PasswordChangeView, // POST: 비밀번호 변경 요청
    },
    // 선호 은행 변경
    {
      path: "/change-preferredbanks",
      name: "PreferredBanksView",
      component: PreferredBanksView, // GET/POST: 선호 은행 조회 및 변경
    },
    // 게시글 목록
    {
      path: "/articles",
      name: "article",
      component: ArticleView, // GET: 게시글 목록 요청
    },
    // 게시글 생성
    {
      path: "/articles/create",
      name: "ArticleCreate",
      component: ArticleCreate, // POST: 게시글 생성 요청
    },
    // 게시글 상세 보기
    {
      path: "/articles/:id",
      name: "ArticleDetail",
      component: ArticleDetail, // GET: 특정 게시글 상세 정보 요청
    },
    // 금융 상품 상세 보기
    {
      path: "/product/:productId",
      name: "FinancialProductDetail",
      component: () => import("@/views/FinancialProductDetail.vue"),
      props: true, // GET: 특정 금융 상품 상세 정보 요청
    },
  ],
});

export default router;
