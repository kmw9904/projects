import { defineStore } from "pinia";
import { fetchExchangeRates } from "@/api/index";

export const useCurrencyStore = defineStore("currency", {
  state: () => ({
    rates: {}, // 환율 데이터
    isLoading: false, // 로딩 상태
    error: null,
  }),

  actions: {
    loadExchangeRates() {
      this.isLoading = true;
      this.error = null;

      fetchExchangeRates()
        .then((data) => {
          // API 데이터에서 필요한 정보만 추출
          this.rates = data.reduce((acc, item) => {
            acc[item.cur_unit] = {
              deal_bas_r: parseFloat(item.deal_bas_r.replace(",", "")), // 기준 환율
            };
            return acc;
          }, {});
        })
        .catch((error) => {
          this.error = error.message || "Failed to load exchange rates";
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
});
