<script setup>
import { ref, computed } from "vue";
import Header from "@/components/Header.vue";
import Payment from "@/components/Payment.vue";
import PaymentSuccess from "@/components/PaymentSuccess.vue";
import OrderHistory from "@/components/OrderHistory.vue";
import ProviderOrderHistory from "@/components/ProviderOrderHistory.vue";
import Main from "@/components/Main.vue";
import Login from "@/components/Login.vue";
import Signup from "@/components/Signup.vue";
import Form from "@/components/Form.vue";
import Profile from "@/components/Profile.vue";
import Test from "@/components/Test.vue";
import Temp from "@/components/Temp.vue";
import ProviderList from "@/components/ProviderList.vue";
import FavoriteProvider from "@/components/FavoriteProvider.vue";
import { Toaster } from "@/components/ui/sonner";
import Scheduler from "@/components/Scheduler.vue";

const routes = {
  "/": Main,
  "/Payment": Payment,
  "/PaymentSuccess": PaymentSuccess,
  "/OrderHistory": OrderHistory,
  "/ProviderOrderHistory": ProviderOrderHistory,
  "/Login": Login,
  "/Signup": Signup,
  "/Form": Form,
  "/Profile": Profile,
  "/Test": Test,
  "/Temp": Temp,
  "/ProviderList": ProviderList,
  "/FavoriteProvider": FavoriteProvider,
  "/Scheduler": Scheduler,
};

const currentPath = ref(window.location.hash);

window.addEventListener("hashchange", () => {
  currentPath.value = window.location.hash;
});

const currentView = computed(() => {
  const path = currentPath.value.slice(1).split("?")[0] || "/";
  return routes[path];
});
</script>

<template>
  <div class="flex min-h-screen w-full flex-col items-center">
    <Header />
    <div class="flex w-full flex-col items-center">
      <div class="w-full">
        <component :is="currentView" />
      </div>
    </div>
    <Toaster />
  </div>
</template>

<style scoped></style>
