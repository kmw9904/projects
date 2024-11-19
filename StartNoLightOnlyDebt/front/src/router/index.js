import { createRouter, createWebHistory } from "vue-router";
import SignUpView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue";
import MainView from "@/views/MainView.vue";
import JeonseView from "@/components/JeonseView.vue";
import CreditLoanView from "@/components/CreditLoanView.vue";
import MortgageView from "@/components/MortgageView.vue";
import MapView from "@/views/MapView.vue";
import MortgageDetailView from "@/components/MortgageDetailView.vue";
import JeonseDetailView from "@/components/JeonseDetailView.vue";
import CreditLoanDetailView from "@/components/CreditLoanDetailView.vue";
import ExchangeView from "@/components/ExchangeView.vue";

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
  ],
});

export default router;
