// store/reportsStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useReportsStore = defineStore(
  "reports",
  () => {
    // Reports keyed by `${orderId}:${direction}` so each direction is unique per order.
    // direction is either "customer-to-provider" or "provider-to-customer"
    // Shape: { [key]: { orderId, direction, reason, description, reporterId, reporterName, reportedId, reportedName, createdAt } }
    const reports = ref({});

    function reportKey(orderId, direction) {
      return `${orderId}:${direction}`;
    }

    function addReport(orderId, direction, payload) {
      const key = reportKey(orderId, direction);
      // Don't overwrite — one report per order per direction
      if (reports.value[key]) return false;
      reports.value = {
        ...reports.value,
        [key]: {
          orderId,
          direction,
          ...payload,
          createdAt: new Date().toISOString(),
        },
      };
      return true;
    }

    function getReport(orderId, direction) {
      return reports.value[reportKey(orderId, direction)] || null;
    }

    function hasReported(orderId, direction) {
      return !!reports.value[reportKey(orderId, direction)];
    }

    return { reports, addReport, getReport, hasReported };
  },
  {
    persist: true,
  },
);
