<template>
  <div class="chatbot">
    <div class="chatbot-icon" @click="toggleChat">
      <!-- 챗봇 아이콘 이미지 또는 SVG -->
    </div>
    <div class="chat-window" v-if="isChatOpen">
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
          <p v-html="message.text"></p>
        </div>
      </div>
      <input type="text" v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요..." />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import { useBankStore } from "@/stores/bank";

export default {
  setup() {
    const isChatOpen = ref(false);
    const userInput = ref("");
    const messages = ref([]);
    const conversationStage = ref(0);
    const selectedLoanType = ref("");
    const bankStore = useBankStore();

    const products = ref({
      creditLoans: {}, // 개인 대출 상품 목록
      jeonseLoans: {}, // 전세 대출 상품 목록
      mortgageLoans: {}, // 담보 대출 상품 목록
    });

    const mergedLoanProducts = ref([]);
    const selectedProductInfo = ref({});

    // 초기 데이터 로드
    onMounted(() => {
      bankStore.getCreditLoan();
      bankStore.getJeonse();
      bankStore.getMortgage();

      console.log("Credit Loans:", bankStore.creditLoans);
      console.log("Jeonse Loans:", bankStore.jeonses);
      console.log("Mortgage Loans:", bankStore.mortgages);
    });

    // 데이터 변경 감지하여 업데이트
    watch(
      () => bankStore.creditLoans,
      (newVal) => {
        products.value.creditLoans = newVal;
      }
    );
    watch(
      () => bankStore.jeonses,
      (newVal) => {
        products.value.jeonseLoans = newVal;
      }
    );
    watch(
      () => bankStore.mortgages,
      (newVal) => {
        products.value.mortgageLoans = newVal;
      }
    );

    const toggleChat = () => {
      isChatOpen.value = !isChatOpen.value;
      if (isChatOpen.value) {
        // 챗봇 환영 메시지 및 대출 종류 질문
        messages.value.push({
          text: "안녕하세요! 금융 상품 추천 챗봇입니다. 어떤 대출이 필요하신가요?<br/>1. 개인대출<br/>2. 전세대출<br/>3. 담보대출<br/>아니면 일상 대화를 나누고 싶으시면 말씀해주세요!",
          sender: "bot",
        });
        conversationStage.value = 1;
      }
    };

    const sendMessage = () => {
      if (userInput.value.trim() !== "") {
        // 사용자 메시지 추가
        messages.value.push({ text: userInput.value, sender: "user" });
        // 입력 처리
        processUserInput(userInput.value);
        // 입력 필드 초기화
        userInput.value = "";
      }
    };

    const processUserInput = (input) => {
      // 입력을 소문자로 변환하여 처리
      const lowerInput = input.toLowerCase();

      // 일반 대화 처리
      if (isSmallTalk(lowerInput)) {
        handleSmallTalk(lowerInput);
        return;
      }

      switch (conversationStage.value) {
        case 1:
          handleLoanTypeSelection(lowerInput);
          break;
        case 2:
          // 상품 추천 후 단계는 3으로 진행되므로 이 부분은 생략합니다.
          break;
        case 3:
          handleProductSelection(lowerInput);
          break;
        case 4:
          handleProductConfirmation(lowerInput);
          break;
        case 5:
          handlePersonalInfo(lowerInput);
          break;
        default:
          messages.value.push({
            text: "죄송하지만 이해하지 못했습니다. 다시 한 번 말씀해주시겠어요?",
            sender: "bot",
          });
          break;
      }
    };

    const isSmallTalk = (input) => {
      return (
        input.includes("날씨") ||
        input.includes("안녕") ||
        input.includes("고마워") ||
        input.includes("농담") ||
        input.includes("기분") ||
        input.includes("시간") ||
        input.includes("이름") ||
        input.includes("몇 살") ||
        input.includes("취미") ||
        input.includes("도움") ||
        input.includes("사랑") ||
        input.includes("오늘") ||
        input.includes("주말") ||
        input.includes("음식") ||
        input.includes("음악") ||
        input.includes("영화") ||
        input.includes("취업") ||
        input.includes("좋아하는")
      );
    };

    const handleSmallTalk = (input) => {
      if (input.includes("날씨")) {
        messages.value.push({
          text: "오늘 날씨는 정말 좋네요! 산책하기 좋은 날입니다. 😊",
          sender: "bot",
        });
      } else if (input.includes("안녕")) {
        messages.value.push({
          text: "안녕하세요! 무엇을 도와드릴까요?",
          sender: "bot",
        });
      } else if (input.includes("고마워")) {
        messages.value.push({
          text: "별말씀을요! 더 도와드릴 것이 있으면 말씀해주세요.",
          sender: "bot",
        });
      } else if (input.includes("농담")) {
        messages.value.push({
          text: '은행원이 농담하면 뭐라고 할까요? "금융 웃음!" 😂',
          sender: "bot",
        });
      } else if (input.includes("기분")) {
        messages.value.push({
          text: "저는 항상 사용자를 도울 수 있어서 기분이 좋아요! 😄",
          sender: "bot",
        });
      } else if (input.includes("시간")) {
        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        messages.value.push({
          text: `현재 시간은 ${hours}시 ${minutes}분입니다.`,
          sender: "bot",
        });
      } else if (input.includes("이름")) {
        messages.value.push({
          text: "저는 금융 도우미 챗봇입니다. 편하게 불러주세요!",
          sender: "bot",
        });
      } else if (input.includes("몇 살")) {
        messages.value.push({
          text: "저는 나이가 없는 인공지능이랍니다! 🤖",
          sender: "bot",
        });
      } else if (input.includes("취미")) {
        messages.value.push({
          text: "저의 취미는 사용자분들을 돕는 것이에요!",
          sender: "bot",
        });
      } else if (input.includes("도움")) {
        messages.value.push({
          text: "네, 어떤 도움이 필요하신가요?",
          sender: "bot",
        });
      } else if (input.includes("사랑")) {
        messages.value.push({
          text: "사랑은 참 아름다운 감정이죠! ❤️",
          sender: "bot",
        });
      } else if (input.includes("오늘")) {
        messages.value.push({
          text: "오늘 하루도 좋은 일들만 가득하시길 바랄게요! 😊",
          sender: "bot",
        });
      } else if (input.includes("주말")) {
        messages.value.push({
          text: "주말 계획이 어떻게 되시나요? 즐거운 시간 보내세요! 🎉",
          sender: "bot",
        });
      } else if (input.includes("음식")) {
        messages.value.push({
          text: "맛있는 음식은 언제나 기분을 좋게 만들죠! 🍔",
          sender: "bot",
        });
      } else if (input.includes("음악")) {
        messages.value.push({
          text: "좋아하는 음악이 있으신가요? 음악은 마음의 비타민이죠! 🎵",
          sender: "bot",
        });
      } else if (input.includes("영화")) {
        messages.value.push({
          text: "최근에 재미있는 영화 보셨나요? 🎬",
          sender: "bot",
        });
      } else if (input.includes("취업")) {
        messages.value.push({
          text: "취업 준비 중이신가요? 좋은 결과 있기를 응원할게요! 💪",
          sender: "bot",
        });
      } else if (input.includes("좋아하는")) {
        messages.value.push({
          text: "저는 사용자분들을 돕는 것이 가장 좋아요! 😊",
          sender: "bot",
        });
      } else {
        messages.value.push({
          text: "네! 그렇군요. 혹시 필요한 대출이 있으시면 알려주세요.",
          sender: "bot",
        });
      }
    };

    const handleLoanTypeSelection = (input) => {
      if (input.includes("1") || input.includes("개인")) {
        selectedLoanType.value = "credit";
        messages.value.push({
          text: "개인대출을 선택하셨군요! 잠시만 기다려주세요. 😄",
          sender: "bot",
        });
        recommendProducts();
      } else if (input.includes("2") || input.includes("전세")) {
        selectedLoanType.value = "jeonse";
        messages.value.push({
          text: "전세대출을 선택하셨네요! 좋은 선택입니다. 😊",
          sender: "bot",
        });
        recommendProducts();
      } else if (input.includes("3") || input.includes("담보")) {
        selectedLoanType.value = "mortgage";
        messages.value.push({
          text: "담보대출을 선택하셨군요! 안정적인 선택이시네요. 👍",
          sender: "bot",
        });
        recommendProducts();
      } else {
        messages.value.push({
          text: "죄송하지만 선택하신 대출 종류를 이해하지 못했습니다. 1, 2, 3 중에서 선택해주세요.",
          sender: "bot",
        });
      }
    };

    const recommendProducts = () => {
      let loanProducts = [];
      let productTypeName = "";

      if (selectedLoanType.value === "credit") {
        loanProducts = mergeProducts(products.value.creditLoans.credit?.result.baseList || [], products.value.creditLoans.credit?.result.optionList || []);
        productTypeName = "개인신용대출";
      } else if (selectedLoanType.value === "jeonse") {
        loanProducts = mergeProducts(products.value.jeonseLoans.jeonse?.result.baseList || [], products.value.jeonseLoans.jeonse?.result.optionList || []);
        productTypeName = "전세자금대출";
      } else if (selectedLoanType.value === "mortgage") {
        loanProducts = mergeProducts(products.value.mortgageLoans.mortgage?.result.baseList || [], products.value.mortgageLoans.mortgage?.result.optionList || []);
        productTypeName = "주택담보대출";
      }

      if (loanProducts.length > 0) {
        // 상위 3개의 상품 추천
        const topProducts = loanProducts.slice(0, 3);

        mergedLoanProducts.value = topProducts; // 선택된 상품 목록 저장

        let productListText = topProducts.map((product, index) => `${index + 1}. ${product.fin_prdt_nm}`).join("<br/>");

        messages.value.push({
          text: `추천 ${productTypeName} 상품입니다:<br/>${productListText}<br/>원하시는 상품 번호를 입력해주세요.`,
          sender: "bot",
        });

        conversationStage.value = 3; // 다음 단계로 진행
      } else {
        messages.value.push({
          text: "죄송하지만 조건에 맞는 상품이 없습니다. 다른 대출 종류를 선택해보시겠어요?",
          sender: "bot",
        });
        conversationStage.value = 1; // 다시 대출 종류 선택 단계로 이동
      }
    };

    const handleProductSelection = (input) => {
      const selectedNumber = parseInt(input.trim());
      if (isNaN(selectedNumber)) {
        messages.value.push({
          text: "죄송하지만 상품 번호를 이해하지 못했습니다. 1, 2, 3 중에서 선택해주세요.",
          sender: "bot",
        });
        return;
      }

      const selectedProduct = mergedLoanProducts.value[selectedNumber - 1];

      if (!selectedProduct) {
        messages.value.push({
          text: "죄송하지만 해당 번호의 상품이 없습니다. 다시 선택해주세요.",
          sender: "bot",
        });
        return;
      }

      selectedProductInfo.value = selectedProduct;

      // 옵션 텍스트 준비
      const optionsText = selectedProduct.options
        .map((option) => {
          if (selectedLoanType.value === "credit") {
            return `금리 유형: ${option.crdt_lend_rate_type_nm}, 평균 금리: ${option.crdt_grad_avg}%`;
          } else {
            return `금리 유형: ${option.lend_rate_type_nm}, 평균 금리: ${option.lend_rate_avg}%`;
          }
        })
        .join("<br/>");

      messages.value.push({
        text: `선택하신 상품의 상세 정보입니다:<br/>상품명: ${selectedProduct.fin_prdt_nm}<br/>은행명: ${selectedProduct.kor_co_nm}<br/>대출한도: ${
          selectedProduct.loan_lmt || "정보 없음"
        }<br/>대출금리:<br/>${optionsText}`,
        sender: "bot",
      });

      messages.value.push({
        text: '해당 상품으로 진행을 원하시면 "진행"이라고 입력해주세요. 다른 상품을 보시려면 번호를 다시 입력해주세요.',
        sender: "bot",
      });

      conversationStage.value = 4; // 다음 단계로 진행
    };

    const handleProductConfirmation = (input) => {
      if (input.includes("진행")) {
        messages.value.push({
          text: "대출 신청 절차를 도와드리겠습니다. 고객님의 성함과 연락처를 알려주시겠어요?",
          sender: "bot",
        });
        conversationStage.value = 5; // 다음 단계로 진행
      } else {
        messages.value.push({
          text: "다른 상품을 원하시면 상품 번호를 다시 입력해주세요.",
          sender: "bot",
        });
        conversationStage.value = 3; // 상품 선택 단계로 돌아감
      }
    };

    const handlePersonalInfo = (input) => {
      // 개인정보 수집 없이 대화 진행
      messages.value.push({
        text: "감사합니다. 입력하신 정보로 대출 신청을 진행하겠습니다. 😊<br/>추가로 궁금하신 점이 있으시면 언제든 문의해주세요.",
        sender: "bot",
      });
      conversationStage.value = 1; // 대화 단계 초기화
    };

    const mergeProducts = (baseList, optionList) => {
      // baseList와 optionList를 fin_prdt_cd 기준으로 매핑
      return baseList.map((base) => {
        const options = optionList.filter((option) => option.fin_prdt_cd === base.fin_prdt_cd);
        return { ...base, options };
      });
    };

    return {
      isChatOpen,
      userInput,
      messages,
      toggleChat,
      sendMessage,
    };
  },
};
</script>

<style scoped>
.chatbot {
  position: fixed;
  bottom: 20px;
  right: 20px;
}
.chatbot-icon {
  width: 60px;
  height: 60px;
  background-color: #007bff;
  border-radius: 50%;
  cursor: pointer;
}
.chat-window {
  width: 300px;
  height: 400px;
  background-color: #fff;
  border: 1px solid #ccc;
  display: flex;
  flex-direction: column;
}
.messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}
.message {
  margin-bottom: 10px;
}
.message.user {
  text-align: right;
}
.message.bot {
  text-align: left;
}
input[type="text"] {
  border: none;
  border-top: 1px solid #ccc;
  padding: 10px;
  font-size: 16px;
}
</style>
v
