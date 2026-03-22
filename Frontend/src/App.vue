<script setup>
import { ref, computed, onMounted } from "vue"

import Header from "@/components/Header.vue"
import Payment from "@/components/Payment.vue"
import Main from "@/components/Main.vue"
import Login from "@/components/Login.vue"
import Signup from "@/components/Signup.vue"
import Form from "@/components/Form.vue"
import Profile from "@/components/Profile.vue"
import Test from "@/components/Test.vue"
import Hello from "@/components/Hello.vue"
import Temp from "@/components/Temp.vue"
import Provider from "@/components/Provider.vue"
import ProviderList from '@/components/ProviderList.vue'
import ProviderTest from '@/components/ProviderTest.vue'
import Hello1 from '@/components/hello1.vue'
import Hello2 from '@/components/hello2.vue'
import Hello3 from '@/components/hello3.vue'
import Hello4 from '@/components/hello4.vue'
import JoinUs from './components/JoinUs.vue'
import Settings from './components/Settings.vue'
import DemoLocation from './components/DemoLocation.vue'
import DemoCreateJob from './components/DemoCreateJob.vue'
import DemoMyJobs from './components/DemoMyJobs.vue'
import DemoJobListings from './components/DemoJobListings.vue'

import { me, initCsrf, logout as apiLogout } from "@/services/api.js"
import { Toaster } from "@/components/ui/sonner"

const user = ref(null)
const loadingUser = ref(true)

async function refreshUser() {
  try {
    const res = await me()
    user.value = res.data
  } catch (err) {
    user.value = null
  }
}

onMounted(async () => {
  try {
    await initCsrf()
    await refreshUser()
  } finally {
    loadingUser.value = false
  }
})

async function logout() {
  try {
    await initCsrf()
    await apiLogout()
  } catch (err) {
    console.error("Logout error:", err)
  }

  localStorage.clear()
  user.value = null
  window.location.hash = "/"
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
  "/Hello3": Hello3,
  "/Hello4": Hello4,
  "/JoinUs": JoinUs,
  "/Settings": Settings,
  "/DemoLocation": DemoLocation,
  "/DemoCreateJob": DemoCreateJob,
  "/DemoMyJobs": DemoMyJobs,
  "/DemoJobListings": DemoJobListings

}

const currentPath = ref(window.location.hash)

window.addEventListener("hashchange", () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  const path = currentPath.value.replace(/^#/, '').split('?')[0] || "/"
  return routes[path] || Main
})

const isLoggedIn = computed(() => !!user.value)

async function handleLoginSuccess() {
  await refreshUser()
}
</script>

<template>
  <div class="flex flex-col items-center min-h-screen m-[30px] w-full">
    <div v-if="loadingUser">Loading...</div>

    <div v-else class="flex flex-col items-center m-[30px] w-full">
      <Header :user="user" @logout="logout" />

      <div v-if="!isLoggedIn" class="mb-6 flex gap-3">
        <a class="underline" href="#/Login">Login</a>
        <a class="underline" href="#/Signup">Signup</a>
      </div>

      <div class="mt-8 mb-20">
        <component
            :is="currentView"
            @login-success="handleLoginSuccess"
        />
      </div>
    </div>

    <Toaster/>
  </div>
</template>
