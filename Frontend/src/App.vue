<script setup>
import { ref, computed } from 'vue'

import Header from '@/components/Header.vue'
import Payment from '@/components/Payment.vue'
import Main from "@/components/Main.vue"
import Test from "@/components/Test.vue"

const routes = {
  '/': Main,
  '/Payment': Payment,
  '/Test': Test
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
  </div>
</template>
