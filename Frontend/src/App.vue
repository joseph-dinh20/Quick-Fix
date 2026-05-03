<script setup>
import { ref, computed, onMounted } from "vue";

import Header from "@/components/Header.vue";
import Payment from "@/components/Payment.vue";
import Main from "@/components/Main.vue";
import Login from "@/components/Login.vue";
import Signup from "@/components/Signup.vue";
import Form from "@/components/Form.vue";
import Profile from "@/components/Profile.vue";
import Test from "@/components/Test.vue";
import Hello from "@/components/Hello.vue";
import Temp from "@/components/Temp.vue";
import Provider from "@/components/Provider.vue";
import ProviderList from "@/components/ProviderList.vue";
import ProviderTest from "@/components/ProviderTest.vue";
import Hello1 from "@/components/Hello1.vue";
import Hello2 from "@/components/Hello2.vue";
import DemoProfile from "@/components/DemoProfile.vue";
import Hello4 from "@/components/Hello4.vue";
import JoinUs from "./components/JoinUs.vue";
import Settings from "./components/Settings.vue";
import DemoLocation from "./components/DemoLocation.vue";
import DemoMap from "./components/DemoMap.vue"; // ✅ ADDED
import DemoCreateJob from "./components/DemoCreateJob.vue";
import DemoCreateJob2 from "./components/DemoCreateJob2.vue";
import DemoMyJobs from "./components/DemoMyJobs.vue";
import DemoJobListings from "./components/DemoJobListings.vue";
import FavoriteProvider from "@/components/FavoriteProvider.vue";
import DemoProvider from "./components/DemoProvider.vue";
import DemoSavedJobs from "./components/DemoSavedJobs.vue";
import DemoProviderList from "./components/DemoProviderList.vue";
import DemoFavoriteProvider from "./components/DemoFavoriteProvider.vue";
import Scheduler from "./components/Scheduler.vue";
import ReportForm from "./components/ReportForm.vue";
import BecomeFixer from './components/BecomeFixer.vue';
import DemoAssignedJobs from './components/DemoAssignedJobs.vue';
import ReviewProvider from "./components/ReviewProvider.vue";

import { me, initCsrf, logout as apiLogout } from "@/services/api.js";
import { Toaster } from "@/components/ui/sonner";

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
  "/Login": Login,
  "/Signup": Signup,
  "/Form": Form,
  "/Profile": Profile,
  "/Test": Test,
  "/Temp": Temp,
  "/Provider": Provider,
  "/ProviderList": ProviderList,
  "/ProviderTest": ProviderTest,
  "/Hello": Hello,
  "/Hello1": Hello1,
  "/Hello2": Hello2,
  "/DemoProfile": DemoProfile,
  "/Hello4": Hello4,
  "/JoinUs": JoinUs,
  "/Settings": Settings,
  "/DemoLocation": DemoLocation,
  "/DemoMap": DemoMap, // ✅ ADDED
  "/DemoCreateJob": DemoCreateJob,
  "/DemoCreateJob2": DemoCreateJob2,
  "/DemoMyJobs": DemoMyJobs,
  "/DemoJobListings": DemoJobListings,
  "/FavoriteProvider": FavoriteProvider,
  "/DemoFavoriteProvider": DemoFavoriteProvider,
  "/DemoProvider": DemoProvider,
  "/BecomeFixer": BecomeFixer,
  "/DemoSavedJobs": DemoSavedJobs,
  "/DemoProviderList": DemoProviderList,
  "/Scheduler": Scheduler,
  "/ReportForm": ReportForm,
  "/DemoAssignedJobs": DemoAssignedJobs,
  "/ReviewProvider": ReviewProvider
};

const currentPath = ref(window.location.hash);

window.addEventListener("hashchange", () => {
  currentPath.value = window.location.hash;
});

const currentView = computed(() => {
  const path = currentPath.value.replace(/^#/, "").split("?")[0] || "/";
  return routes[path] || Main;
});

const isLoggedIn = computed(() => !!user.value);

async function handleLoginSuccess() {
  await refreshUser();
}
</script>

<template>
  <div class="flex flex-col items-center min-h-screen w-full">
    <div v-if="loadingUser">Loading...</div>

    <div v-else class="flex flex-col items-center w-full">
      <Header />

      <div v-if="!isLoggedIn" class="mb-6 flex gap-3">
      </div>

      <div v-else class="mb-6 flex gap-3 items-center">
        <span class="text-sm">{{ user.email }}</span>
        <a class="underline cursor-pointer" @click="logout">Logout</a>
      </div>

      <div class="w-full">
        <component :is="currentView" @login-success="handleLoginSuccess" />
      </div>
    </div>

    <Toaster />
  </div>
</template>