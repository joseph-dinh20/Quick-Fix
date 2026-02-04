<script setup>
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'

const showScroll = ref(false)

const tags = Array.from({ length: 50 }).map(
  (_, i, a) => `Skibidi ${a.length - i}`,
)

function handleFocus() {
  showScroll.value = true
}

function handleBlur() {
  setTimeout(() => {
    showScroll.value = false
  }, 150)
}
</script>

<template>
  <main class="mt-[30px] text-green-800 min-w-screen min-h-screen flex flex-col items-center gap-[32px]">
    <h1 class="text-5xl">Get the job done today.</h1>
    <h1 class="text-5xl">No hassle.</h1>
    <h2 class="text-1xl">
      Schedule an appointment now and lets get your problems fixed!
    </h2>

    <div class="w-full max-w-sm space-y-2">
      <div class="flex w-full max-w-sm items-center space-x-2">
        <Input type="text" placeholder="Looking for something else?" @focus="handleFocus" @blur="handleBlur" />
        <Button type="submit"> search </Button>
      </div>
    </div>

    <!-- Scroll Area -->
    <ScrollArea v-if="showScroll" class="mt-1 w-xs h-[200px] rounded-md border bg-background shadow-md z-50">
      <div class="p-2 space-y-1">
        <div v-for="tag in tags" :key="tag"
          class="border border-red-300 cursor-pointer rounded px-2 py-1 hover:bg-muted">
          {{ tag }}
        </div>
      </div>
    </ScrollArea>

    <div class="flex flex-wrap items-center justify-center gap-3 md:flex-row scale-[2] mt-[100px] border">
      <div class="flex flex-col justify-center items-center">
        <Button variant="outline" size="icon" aria-label="Submit"></Button>
        <div class="scale-[0.8]">Title</div>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
