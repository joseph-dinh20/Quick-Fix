<script setup>
import { ref, computed } from 'vue'
import Footer from '@/components/Footer.vue'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'

// Importing Images
import drillImage from '@/assets/drill.png'
import garden from '@/assets/garden.png'

const showScroll = ref(false)
const value = ref('')
const jobs = [
  { name: 'Home Repair' },
  { name: 'Gardening' },
  { name: 'Honeydew' },
  { name: 'Grapes' },
  { name: 'Watermelon' },
  { name: 'Cantaloupe' },
  { name: 'Pear' },
]

// computed() is a vue function that updates
// whenever ANYTHING in it changes.
const filteredJobs = computed(() => {
  const query = value.value.toLowerCase()
  // console.log(query)
  return jobs.filter(job => job.name.toLowerCase().includes(query))
})

function showScrollState() {
  showScroll.value = !showScroll.value
  // console.log("showScroll state is now " + showScroll.value)
}

function selectjob(item) {
  // console.log(item.name)
  value.value = item.name
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
        <Input type="text" v-model="value" @focus="showScrollState" @blur="showScrollState"
          placeholder="Looking for something else?" />
        <Button type="submit"> Search </Button>
      </div>

      <!-- Floating Dropdown Wrapper -->
      <div v-if="showScroll" class="absolute mt-1 w-full z-1">
        <ScrollArea class="h-[200px] w-full rounded-md bg-background shadow-lg">
          <div class="p-6 space-y-3">
            <div v-for="job in filteredJobs" :key="job" @mousedown="selectjob(job)"
              class="cursor-pointer rounded px-2 py-1 border hover:bg-muted transition">
              {{ job.name }}
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
  <Footer />
</template>

<style scoped></style>
