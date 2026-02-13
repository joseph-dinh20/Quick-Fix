<script setup>
import { ref, computed } from 'vue'
<<<<<<< HEAD
=======

import hello from './components/hello.vue'
>>>>>>> 1498e9df7c91b8cbf19da56783f9fb2a5df42354
import Header from '@/components/Header.vue'
import Payment from '@/components/Payment.vue'
import Main from '@/components/Main.vue'
import Login from '@/components/Login.vue'
import Test from '@/components/Test.vue'
import Signup from '@/components/Signup.vue'
import Form from '@/components/Form.vue'
import Profile from '@/components/Profile.vue'
import SampleForm from '@/components/SampleForm.vue'

const routes = {
  '/': Main,
  '/Payment': Payment,
  '/Login': Login,
  '/Signup': Signup,
  '/Form': Form,
  '/Profile': Profile,
  '/Test': Test,
<<<<<<< HEAD
  '/SampleForm': SampleForm,
}

const isLoggedIn = ref(false)
function handleLoginSuccess() {
  isLoggedIn.value = true
  // window.location.hash = '/'
=======
  '/hello': hello,
>>>>>>> 1498e9df7c91b8cbf19da56783f9fb2a5df42354
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
  <div class="flex flex-col items-center m-[30px]">
    <div v-if='isLoggedIn' class="flex flex-col items-center m-[30px]">
      <Header v-show="isLoggedIn" />
      <!-- <Header /> -->
      <component class="m-20" :is="currentView" />
    </div>
    <Login v-else @login-success="handleLoginSuccess" />
  </div>
</template>
