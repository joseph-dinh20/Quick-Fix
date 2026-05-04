// store/orderHistoryStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useOrderHistoryStore = defineStore(
  "orderHistory",
  () => {
    const orders = ref([]);

    function addOrder(order) {
      orders.value.unshift({
        id: `ord_${Date.now()}`,
        createdAt: new Date().toISOString(),
        ...order,
      });
    }

    function removeOrder(id) {
      orders.value = orders.value.filter((o) => o.id !== id);
    }

    function markAsRated(orderId, { userRated, userComment }) {
      const order = orders.value.find((o) => o.id === orderId);
      if (!order) return;
      order.userRated = userRated;
      order.userComment = userComment;
      order.ratedAt = new Date().toISOString();
    }

    // Provider marks the job complete with hours worked and an optional review
    function markComplete(orderId, { hoursWorked, providerComment }) {
      const order = orders.value.find((o) => o.id === orderId);
      if (!order) return;
      order.hoursWorked = hoursWorked;
      order.providerComment = providerComment || "";
      order.completedAt = new Date().toISOString();
    }

    return { orders, addOrder, removeOrder, markAsRated, markComplete };
  },
  {
    persist: true,
  },
);
