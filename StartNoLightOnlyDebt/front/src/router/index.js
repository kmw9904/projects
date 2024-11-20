import { createRouter, createWebHistory } from "vue-router";
import SignUpView from "@/accounts/SignUpView.vue";
import LoginView from "@/accounts/LoginView.vue";
import MainView from "@/views/MainView.vue";
import JeonseView from "@/loans/JeonseView.vue";
import CreditLoanView from "@/loans/CreditLoanView.vue";
import MortgageView from "@/loans/MortgageView.vue";
import MapView from "@/views/MapView.vue";
import MortgageDetailView from "@/loans/MortgageDetailView.vue";
import JeonseDetailView from "@/loans/JeonseDetailView.vue";
import CreditLoanDetailView from "@/loans/CreditLoanDetailView.vue";
import ExchangeView from "@/components/ExchangeView.vue";
import AlgorithmView from "@/algorithm/AlgorithmView.vue";
import AccountView from "@/accounts/AccountView.vue";
import PasswordChangeView from "@/accounts/PasswordChangeView.vue";
import PreferredBanksView from "@/accounts/PreferredBanksView.vue";
import ArticleView from "@/views/ArticleView.vue";
import ArticleDetail from "@/views/ArticleDetail.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LoginView",
      component: LoginView,
    },
    {
      path: "/",
      name: "MainView",
      component: MainView,
    },
    {
      path: "/jeonse",
      name: "JeonseView",
      component: JeonseView,
    },
    {
      path: "/credit-loan",
      name: "CreditLoanView",
      component: CreditLoanView,
    },
    {
      path: "/mortgage",
      name: "MortgageView",
      component: MortgageView,
    },
    {
      path: "/map",
      name: "map",
      component: MapView,
    },
    {
      path: "/mortgage/detail",
      name: "MortgageDetailView",
      component: MortgageDetailView,
    },
    {
      path: "/jeonse/detail",
      name: "JeonseDetailView",
      component: JeonseDetailView,
    },
    {
      path: "/credit-loan/detail",
      name: "CreditLoanDetailView",
      component: CreditLoanDetailView,
    },
    {
      path: "/exchange",
      name: "ExchangeView",
      component: ExchangeView,
    },
    {
      path: "/algorithm",
      name: "AlgorithmView",
      component: AlgorithmView,
    },
    {
      path: "/profile",
      name: "AccountView",
      component: AccountView,
    },
    {
      path: "/change-password",
      name: "PasswordChangeView",
      component: PasswordChangeView,
    },
    {
      path: "/change-preferredbanks",
      name: "PreferredBanksView",
      component: PreferredBanksView,
    },
    {
      path: "/articles",
      name: "article",
      component: ArticleView,
    },
    {
      path: "/articles/:id",
      name: "ArticleDetail",
      component: ArticleDetail,
    }, // 게시글 상세 보기
  ],
});

export default router;
