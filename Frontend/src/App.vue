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
import Hello from "./components/hello.vue"
import Temp from "@/components/Temp.vue"
import Provider from "@/components/Provider.vue"
import ProviderList from '@/components/ProviderList.vue'
import Hello2 from '@/components/hello2.vue'
import Hello3 from '@/components/hello3.vue'
import Hello4 from '@/components/hello4.vue'
import Join from './components/Join.vue'

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
  "/Join": Join,
  "/Form": Form,
  "/Profile": Profile,
  "/Test": Test,
  "/Temp": Temp,
  "/Provider": Provider,
  "/Hello": Hello,
  "/ProviderList": ProviderList,
  "/Hello2": Hello2,
  "/Hello3": Hello3,
  "/Hello4": Hello4,
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
  <div class="flex flex-col items-center m-[30px]">
    <div v-if="loadingUser">Loading...</div>

    <div v-else class="flex flex-col items-center m-[30px]">
      <Header/>

      <div v-if="isLoggedIn" class="text-sm mb-3">Logged in as: {{ user.email }}</div>
      <button v-if="isLoggedIn" class="mb-6 underline" @click="logout">Logout</button>

      <div v-else class="mb-6 flex gap-3">
        <a class="underline" href="#/Login">Login</a>
        <a class="underline" href="#/Hello">Signup</a>
      </div>

      <div class="m-20">
        <component
            :is="currentView"
            @login-success="handleLoginSuccess"
        />
      </div>
    </div>

    <Toaster/>
  </div>
</template>