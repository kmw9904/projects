<template>
  <div id="app">
    <div class="chatbot">
      <!-- 채팅 메시지 리스트 -->
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" :class="message.type">
          <span>{{ message.text }}</span>
        </div>
      </div>

      <!-- 메시지 입력 및 전송 -->
      <div class="input-container">
        <input v-model="userInput" type="text" placeholder="메시지를 입력하세요" @keyup.enter="sendMessage" />
        <button @click="sendMessage">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useArticleStore } from "@/stores/articles";

// 상태 관리
const userInput = ref("");
const messages = ref([]);
const chatHistory = ref([]); // 대화 기록 관리
const topLikedProducts = ref([]);

// Store 관련
const store = useArticleStore();
const topLikedArticle = computed(() => store.topLikedArticle);

// API URL
const API_URL = "http://127.0.0.1:8000";

// 최고 좋아요 상품 가져오기
const fetchTopLikedProducts = async () => {
  try {
    const creditResponse = await axios.get(`${API_URL}/interactions/credit/top-liked/`);
    const jeonseResponse = await axios.get(`${API_URL}/interactions/jeonse/top-liked/`);
    const mortgageResponse = await axios.get(`${API_URL}/interactions/mortgage/top-liked/`);

    topLikedProducts.value = [creditResponse.data, jeonseResponse.data, mortgageResponse.data].filter((product) => product.likes);
  } catch (error) {
    console.error("최고 좋아요 상품 가져오기 실패:", error.response?.data || error.message);
  }
};

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// OpenAI API 호출
const fetchOpenAIResponse = async (userMessage) => {
  const apiUrl = "https://api.openai.com/v1/chat/completions";
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
  };

  const defaultProducts = [
    { company_name: "없음", product_name: "없음" },
    { company_name: "없음", product_name: "없음" },
    { company_name: "없음", product_name: "없음" },
  ];

  const products = topLikedProducts.value.length ? topLikedProducts.value : defaultProducts;

  // 대화 기록 추가
  chatHistory.value.push({ role: "user", content: userMessage });

  const data = {
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `
        당신은 Start No Light Only Debt(편리한 대출 정보 제공 프로그램)이라는 회사의 대출 상품 및 상담 및 은행원 역할의 챗봇입니다.
        다음은 가장 인기 있는 대출 상품 목록입니다:
        1. 신용 대출: ${products[0]?.company_name}의 ${products[0]?.product_name}.
        2. 전세 대출: ${products[1]?.company_name}의 ${products[1]?.product_name}.
        3. 담보 대출: ${products[2]?.company_name}의 ${products[2]?.product_name}.
        사용자의 요청에 따라 적절한 상품을 추천하세요.
        `,
      },
      ...chatHistory.value, // 대화 기록 추가
    ],
    max_tokens: 150,
  };

  return axios
    .post(apiUrl, data, { headers })
    .then((response) => {
      const botResponse = response.data.choices[0].message.content.trim();
      chatHistory.value.push({ role: "assistant", content: botResponse }); // 대화 기록에 챗봇 응답 추가
      return botResponse;
    })
    .catch((error) => {
      console.error("OpenAI API 호출 실패:", error.response?.data || error.message);
      return "죄송합니다, 응답을 생성하지 못했습니다. 다시 시도해주세요.";
    });
};

// 메시지 전송
const sendMessage = async () => {
  if (userInput.value.trim() === "") return;

  // 현재 입력값 저장
  const currentInput = userInput.value;

  // 사용자 메시지 추가
  messages.value.push({ text: currentInput, type: "user" });
  chatHistory.value.push({ role: "user", content: currentInput }); // 대화 기록에 사용자 메시지 추가
  messages.value.push({ text: "잠시만 기다려주세요...", type: "bot" });

  try {
    const response = await fetchOpenAIResponse(currentInput);
    messages.value[messages.value.length - 1] = { text: response, type: "bot" }; // 로딩 메시지 대체
  } catch (error) {
    messages.value.push({ text: "오류가 발생했습니다. 다시 시도해주세요.", type: "bot" });
  }

  userInput.value = "";
};

// Mount 시 데이터 가져오기
onMounted(() => {
  fetchTopLikedProducts();
  store.fetchArticles();
});
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin: 0 auto;
  max-width: 400px;
}

.chatbot {
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  max-height: 500px;
}

.messages .user {
  text-align: right;
  margin: 5px 0;
  color: white;
  background: #007bff;
  padding: 5px 10px;
  border-radius: 10px;
  display: inline-block;
}

.messages .bot {
  text-align: left;
  margin: 5px 0;
  color: #333;
  background: #f1f1f1;
  padding: 5px 10px;
  border-radius: 10px;
  display: inline-block;
}

.input-container {
  display: flex;
  border-top: 1px solid #ccc;
  padding: 10px;
}

.input-container input {
  flex: 1;
  padding: 5px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.input-container button {
  margin-left: 10px;
  padding: 5px 15px;
  font-size: 14px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.input-container button:hover {
  background-color: #0056b3;
}
</style>
