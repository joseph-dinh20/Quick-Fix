// store/orderStore.js
import { defineStore } from "pinia";

export const useOrderStore = defineStore("order", {
  state: () => ({
    // NOTE: data from Main.vue
    serviceCategory: "",

    // NOTE: data from Form.vue
    address: "",
    apartment: "",
    plan: "",
    description: "",

    // NOTE: data from Scheduler.vue
    scheduledDate: null,
    scheduledTime: null,
    scheduledTimeText: null,

    // NOTE: data from ProviderList.vue -> to Scheduler.vue
    selectedProvider: null,
  }),
  actions: {
    setServiceCategory(category) {
      this.serviceCategory = category;
    },
    setFormData(values) {
      this.address = values.address;
      this.apartment = values.apartment || "";
      this.plan = values.plan;
      this.description = values.description;
    },
    setSchedule(date, time, timeText) {
      this.scheduledDate = date;
      this.scheduledTime = time;
      this.scheduledTimeText = timeText;
    },
    setSelectedProvider(provider) {
      this.selectedProvider = provider;
    },
    reset() {
      this.serviceCategory = "";
      this.address = "";
      this.apartment = "";
      this.plan = "";
      this.description = "";
      this.scheduledDate = null;
      this.scheduledTime = null;
      this.scheduledTimeText = null;
      this.selectedProvider = null;
    },
  },
  persist: true,
});
