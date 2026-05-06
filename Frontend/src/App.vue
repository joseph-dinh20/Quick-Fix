<script setup>
import { ref, computed, onMounted, watch } from "vue";
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
import ReportForm from "./components/ReportForm.vue";
import DemoAssignedJobs from "./components/DemoAssignedJobs.vue";
import DemoSavedJobs from "./components/DemoSavedJobs.vue";
import DemoJobListings from "./components/DemoJobListings.vue";
import JoinUs from "./components/JoinUs.vue";
import DemoCreateJob from "./components/DemoCreateJob.vue";
import DemoMyJobs from "./components/DemoMyJobs.vue";
import ReviewProvider from "./components/ReviewProvider.vue";
import ChatMessages from "./components/ChatMessages.vue";
import Settings from "./components/Settings.vue";
import Scheduler from "./components/Scheduler.vue";
import DemoMap from "./components/DemoMap.vue";
import BecomeFixer from "./components/BecomeFixer.vue";
import { useUserStore } from "@/store/userStore";

const userStore = useUserStore();
const user = ref(null);
const loadingUser = ref(true);
const isLoggedIn = ref(false);

// Watch the userStore for changes
watch(
  () => userStore.currentUser,
  (newUser) => {
    user.value = newUser;
    isLoggedIn.value = !!newUser;
  },
  { immediate: true }
);

async function refreshUser() {
  try {
    const res = await me();
    user.value = res.data;
    isLoggedIn.value = true;
  } catch (err) {
    user.value = null;
  }
}

onMounted(async () => {
  try {
    // await initCsrf();
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

function handleLoginSuccess() {
  // Update local state when login succeeds
  user.value = userStore.currentUser;
  isLoggedIn.value = true;
}

function handleLogout() {
  // Update local state when logout succeeds
  user.value = null;
  isLoggedIn.value = false;
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
  "/JoinUs": JoinUs,
  "/ProviderList": ProviderList,
  "/FavoriteProvider": FavoriteProvider,
  "/Scheduler": Scheduler,
  "/ReportForm": ReportForm,
  "/DemoAssignedJobs": DemoAssignedJobs,
  "/ReviewProvider": ReviewProvider,
  "/ChatMessages": ChatMessages,
  "/DemoSavedJobs": DemoSavedJobs,
  "/DemoCreateJob": DemoCreateJob,
  "/DemoJobListings": DemoJobListings,
  "/DemoMyJobs": DemoMyJobs,
  "/ReviewProvider": ReviewProvider,
  "/NavigationBar": NavigationBar,
  "/DemoMap": DemoMap,
  "/Settings": Settings,
  "/BecomeFixer": BecomeFixer,
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
