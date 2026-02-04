<script setup>
import { ref } from 'vue'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'

// Importing Images
import drillImage from '@/assets/drill.png'
import garden from '@/assets/garden.png'

const showScroll = ref(false)

const tags = Array.from({ length: 50 }).map(
  (_, i) => `Skibidi ${i + 1}`,
)

function handleFocus() {
  showScroll.value = true
}

function handleBlur() {
  // Delay so clicking dropdown doesn't instantly close it
  setTimeout(() => {
    showScroll.value = false
  }, 200)
}

function selectTag(tag) {
  console.log('Selected:', tag)
  showScroll.value = false
}
</script>

<template>
  <main class="mt-10 min-h-screen w-full flex flex-col items-center gap-16 text-green-800">
    <h1 class="text-5xl font-bold">Get the job done today.</h1>
    <h1 class="text-5xl font-bold">No hassle.</h1>
    <h2 class="text-xl text-center max-w-xl">
      Schedule an appointment now and lets get your problems fixed!
    </h2>

    <!-- Search Box -->
    <div class="w-full max-w-sm relative">
      <!-- Input Row -->
      <div class="flex items-center gap-2">
        <Input type="text" placeholder="Looking for something else?" @focus="handleFocus" @blur="handleBlur" />
        <Button type="submit"> Search </Button>
      </div>

      <!-- Floating Dropdown Wrapper -->
      <div v-if="showScroll" class="absolute mt-1 w-full z-1">
        <ScrollArea class="h-[200px] w-full rounded-md bg-background shadow-lg">
          <div class="p-2 space-y-2">
            <div v-for="tag in tags" :key="tag" @mousedown="selectTag(tag)"
              class="cursor-pointer rounded px-2 py-1 border hover:bg-muted transition">
              {{ tag }}
            </div>
          </div>
        </ScrollArea>
      </div>
    </div>

    <!-- Job Type Buttons/Icons -->
    <div class="flex flex-wrap items-center justify-center scale-[2] p-6 rounded-lg">
      <div class="flex flex-col items-center">
        <Button variant="outline" size="icon" aria-label="Submit"> <img :src="drillImage"> </Button>
        <div class="scale-[0.5] mt-1"> Home Repair </div>
      </div>
      <div class="flex flex-col items-center">
        <Button variant="outline" size="icon" aria-label="Submit"> <img :src="garden"> </Button>
        <div class="scale-[0.5] mt-1"> Gardening </div>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
