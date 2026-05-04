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
import NavigationBar from "./components/NavigationBar.vue";

const user = ref(null);
const loadingUser = ref(true);

async function refreshUser() {
  try {
    const res = await me();
    user.value = res.data;
  } catch (err) {
    user.value = null;
  }
}

onMounted(async () => {
  try {
    await initCsrf();
    await refreshUser();
  } finally {
    loadingUser.value = false;
  }
});

async function logout() {
  try {
    await initCsrf();
    await apiLogout();
  } catch (err) {
    console.error("Logout error:", err);
  }

  localStorage.clear();
  user.value = null;
  window.location.hash = "/";
}

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
  "/ReportForm": ReportForm,
  "/DemoAssignedJobs": DemoAssignedJobs,
  "/ReviewProvider": ReviewProvider,
  "/NavigationBar": NavigationBar,
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
    <NavigationBar
      :is="currentView" 
      :is-logged-in="isLoggedIn"
      :user="user"
      @login-success="handleLoginSuccess"
      @logout-success="handleLogout" 
      />
    <div class="flex w-full flex-col items-center">
      <div class="w-full mt-10">
        <component 
          :is="currentView" 
          :is-logged-in="isLoggedIn"
          :user="user"
          @login-success="handleLoginSuccess"
          @logout-success="handleLogout" 
        />
      </div>
    </div>
    <Toaster />
  </div>
</template>

<style scoped></style>
