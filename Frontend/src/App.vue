<script setup>
import { ref, computed } from 'vue'

import hello from './components/hello.vue'
import Header from '@/components/Header.vue'
import Payment from '@/components/Payment.vue'
import Main from '@/components/Main.vue'
import Login from '@/components/Login.vue'
import Test from '@/components/Test.vue'
import Signup from '@/components/Signup.vue'
import Form from '@/components/Form.vue'
import Form2 from '@/components/Form2.vue'
import ToastExample from '@/components/toastExample.vue'
import { toast } from 'vue-sonner'

const routes = {
  '/': Main,
  '/Payment': Payment,
  '/Login': Login,
  '/Signup': Signup,
  '/Form': Form,
  '/Form2': Form2,
  '/ToastExample': ToastExample,
  '/Test': Test,
  '/hello': hello,
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
  <Header />

  <div class="mt-[30px] text-green-800 min-w-screen min-h-screen flex flex-col items-center m-[30px]">
    <component :is="currentView" />
    <Toaster />
  </div>

</template>
