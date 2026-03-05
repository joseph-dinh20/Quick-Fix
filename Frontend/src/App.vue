<script setup>
import { ref, computed onMounted} from 'vue'
import Header from '@/components/Header.vue'
import Payment from '@/components/Payment.vue'
import Main from '@/components/Main.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Form from '@/components/Form.vue'
import Profile from '@/components/Profile.vue'
import Test from '@/components/Test.vue'
import Hello from './components/hello.vue'
import Temp from '@/components/Temp.vue'
import Provider from '@/components/Provider.vue'
import ProviderList from '@/components/ProviderList.vue'


import { Toaster } from '@/components/ui/sonner'

const routes = {
  '/': Main,
  '/Payment': Payment,
  '/Login': Login,
  '/Signup': Signup,
  '/Form': Form,
  '/Profile': Profile,
  '/Test': Test,
  '/Temp': Temp,
  '/Provider': Provider,
  '/Hello': Hello,
  '/ProviderList': ProviderList
}

// const isLoggedIn = ref(false)
const isLoggedIn = ref(true)
function handleLoginSuccess() {
  isLoggedIn.value = true
  // window.location.hash = '/'
}

const currentPath = ref(window.location.hash)
window.addEventListener("hashchange", () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || "/"] || Main
})

// ✅ real login state based on session
const isLoggedIn = computed(() => !!user.value)

async function handleLoginSuccess() {
  await refreshUser()
}
</script>





<template>
  <div class="flex flex-col items-center m-[30px]">
    <div v-if="loadingUser">Loading...</div>

    <div v-else class="flex flex-col items-center m-[30px]">
      <!-- ✅ always show header -->
      <Header />

      <!-- ✅ show auth info only when logged in -->
      <div v-if="isLoggedIn" class="text-sm mb-3">Logged in as: {{ user.email }}</div>
      <button v-if="isLoggedIn" class="mb-6 underline" @click="logout">Logout</button>

      <!-- ✅ guest buttons (temporary) -->
      <div v-else class="mb-6 flex gap-3">
        <a class="underline" href="#/Login">Login</a>
        <a class="underline" href="#/Signup">Signup</a>
      </div>

      <div class="m-20">
        <component
          :is="currentView"
          @login-success="handleLoginSuccess"
        />
      </div>
    </div>

    <Toaster />
  </div>
</template>


