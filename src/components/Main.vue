<script setup>
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import combobox from '@/components/combobox.vue'
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
  setTimeout(() => { showScroll.value = false }, 150)
}
</script>

<template>
  <main class="mt-[30px] text-green-800 min-h-screen">
    <h1 class="text-5xl">Get the job done today.</h1>
    <h1 class="text-5xl">No hassle.</h1>
    <h2 class="text-3xl">Schedule an appointment now and lets get your problems fixed!</h2>
    <div class="relative w-full max-w-sm space-y-2">
      <div class="flex w-full max-w-sm items-center space-x-2">
        <Input type="text" placeholder="Looking for something else?" @focus="handleFocus" @blur='handleBlur' />
        <Button type="submit">
          search
        </Button>
      </div>
      <!-- Scroll Area -->
      <ScrollArea v-if="showScroll"
        class="absolute top-full mt-1 w-full h-[300px] rounded-md border bg-background shadow-md z-50">
        <div class="p-2 space-y-1">
          <div v-for="tag in tags" :key="tag" class="cursor-pointer rounded px-2 py-1 hover:bg-muted">
            {{ tag }}
          </div>
        </div>
      </ScrollArea>
    </div>
  </main>
</template>

<style scoped>
main {
  /* border: black solid 1px; */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

main h2 {
  font-size: 16px;
}
</style>
