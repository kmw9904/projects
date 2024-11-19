import { createRouter, createWebHistory } from "vue-router";

// Auth Views
import SignUpView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue";

// Main Views
import MainView from "@/views/MainView.vue";
import MapView from "@/views/MapView.vue";

// Financial Components
import JeonseView from "@/components/JeonseView.vue";
import CreditLoanView from "@/components/CreditLoanView.vue";
import MortgageView from "@/components/MortgageView.vue";

// Financial Detail Views
import MortgageDetailView from "@/components/MortgageDetailView.vue";
import JeonseDetailView from "@/components/JeonseDetailView.vue";
import CreditLoanDetailView from "@/components/CreditLoanDetailView.vue";

// Exchange and Algorithms
import ExchangeView from "@/components/ExchangeView.vue";
import AlgorithmView from "@/algorithm/AlgorithmView.vue";
import AccountView from "@/views/AccountView.vue";

// Community Components
import ArticleView from "@/views/ArticleView.vue";
import ArticleCreateView from "@/views/ArticleCreateView.vue";
import ArticleDetailView from "@/views/ArticleDetailView.vue";

const routes = [
  // Auth Routes
  {
    path: "/signup",
    name: "SignUpView",
    component: SignUpView,
    meta: { requiresAuth: false },
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView,
    meta: { requiresAuth: false },
  },

  // Main Page
  {
    path: "/",
    name: "MainView",
    component: MainView,
    meta: { requiresAuth: true },
  },

  // Financial Routes
  {
    path: "/jeonse",
    name: "JeonseView",
    component: JeonseView,
    meta: { requiresAuth: true },
  },
  {
    path: "/credit-loan",
    name: "CreditLoanView",
    component: CreditLoanView,
    meta: { requiresAuth: true },
  },
  {
    path: "/mortgage",
    name: "MortgageView",
    component: MortgageView,
    meta: { requiresAuth: true },
  },

  // Detail Routes
  {
    path: "/mortgage/detail",
    name: "MortgageDetailView",
    component: MortgageDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: "/jeonse/detail",
    name: "JeonseDetailView",
    component: JeonseDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: "/credit-loan/detail",
    name: "CreditLoanDetailView",
    component: CreditLoanDetailView,
    meta: { requiresAuth: true },
  },

  // Map and Exchange Routes
  {
    path: "/map",
    name: "MapView",
    component: MapView,
    meta: { requiresAuth: true },
  },
  {
    path: "/exchange",
    name: "ExchangeView",
    component: ExchangeView,
    meta: { requiresAuth: true },
  },

  // Algorithm
  {
    path: "/algorithm",
    name: "AlgorithmView",
    component: AlgorithmView,
    meta: { requiresAuth: true },
  },

  // Community Routes
  {
    path: "/articles",
    name: "ArticleView",
    component: ArticleView,
    meta: { requiresAuth: true },
  },
  {
    path: "/articles/create",
    name: "ArticleCreateView",
    component: ArticleCreateView,
    meta: { requiresAuth: true },
  },
  {
    path: "/articles/:id",
    name: "ArticleDetailView",
    component: ArticleDetailView,
    meta: { requiresAuth: true },
    props: true, // Allow route params to be passed as props
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
<<<<<<< HEAD
  routes,
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token"); // Simple token presence check
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: "LoginView" }); // Redirect to login if not authenticated
  } else {
    next(); // Proceed if authorized or route doesn't require auth
  }
=======
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
      path: "/account-detail",
      name: "AccountView",
      component: AccountView,
    },
  ],
>>>>>>> 45d47808643f6844e79a29e3441bff6838cf4c6a
});

export default router;
