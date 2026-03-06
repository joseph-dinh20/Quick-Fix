<script setup>
import { ref, computed } from 'vue'
import Header from '@/components/Header.vue'
import Payment from '@/components/Payment.vue'
import Main from '@/components/Main.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Form from '@/components/Form.vue'
import Profile from '@/components/Profile.vue'
import Test from '@/components/Test.vue'
import Hello from './components/Hello.vue'
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
  // '/Provider': Provider,
  '/Hello': Hello,
  '/ProviderList': ProviderList,
}

const isLoggedIn = ref(true)
function handleLoginSuccess() {
  isLoggedIn.value = true
  // window.location.hash = '/'
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/']
})
</script>

<template>
  <div class="flex flex-col items-center">
    <div v-if='isLoggedIn' class="flex flex-col items-center">
      <Header v-show="isLoggedIn" />
      <!-- <Header /> -->
      <div class="m-20">
        <component :is="currentView" />
      </div>
    </div>
    <Login v-else @login-success="handleLoginSuccess" />
    <Toaster />
  </div>
</template>
