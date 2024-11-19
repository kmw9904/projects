import axios from "axios";

// 환경 변수에서 API 키와 URL 가져오기
const API_KEY = import.meta.env.VITE_API_KEY;
const API_URL = "/api/site/program/financial/exchangeJSON"; // 프록시를 통해 전달


// 환율 데이터를 가져오는 함수
export const fetchExchangeRates = async () => {
  try {
    const response = await axios.get(API_URL, {
      params: {
        authkey: API_KEY, // API 키
        data: "AP01", // 요청 데이터 형식
      },
    });
    console.log("API 응답 데이터:", response.data); // 데이터 확인용
    return response.data; // 성공적으로 데이터를 반환
  } catch (err) {
    console.error("환율 데이터를 가져오는 중 오류:", err);
    throw new Error("환율 데이터를 가져오는 중 문제가 발생했습니다.");
  }
};
