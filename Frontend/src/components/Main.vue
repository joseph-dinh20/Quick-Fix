<script setup>
import { ref, computed } from 'vue'
import Footer from '@/components/Footer.vue'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'

// Importing Images
import drillImage from '@/assets/icons/drill.png'
import garden from '@/assets/icons/garden.png'

const showScroll = ref(false)
const value = ref('')
const jobs = [
  { name: 'Home Repair' },
  { name: 'Gardening' },
  // { name: 'Honeydew' },
  // { name: 'Grapes' },
  // { name: 'Watermelon' },
  // { name: 'Cantaloupe' },
  // { name: 'Pear' },
]

const pageOneText = [
  { text: "Problems around the house?", class: 'text-5xl font-bold text-green-700' },
  { text: 'Find local professionals near you!', class: 'text-4xl font-bold text-green-700' },
  { text: 'Schedule an appointment today.', class: 'text-3xl font-semibold text-center text-green-700' },
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
  <div class="flex flex-col items-center">
    <main class="min-h-screen w-full flex flex-col items-center gap-16">
      <!-- NOTE: PageOneText -->
      <div v-for="(text, i) in pageOneText"
        :key="i"
        :class="['animate__animated animate__fadeInUp', text.class]"
        :style="{ animationDelay: `${i * 0.3}s`}"
      >
        {{text.text}}
      </div>

      <!-- NOTE: Search Box -->
      <div class="w-full max-w-sm relative">
        <!-- Input Row -->
        <div class="flex items-center gap-2">
          <Input type="text" v-model="value" @focus="showScrollState" @blur="showScrollState"
            placeholder="Looking for something else?" />
          <!-- <a href="#/Form"> -->
            <Button type="submit"> Search </Button>
          <!-- </a> -->
        </div>

        <!-- NOTE: Floating Dropdown Wrapper -->
        <div v-if="showScroll" class="absolute mt-1 w-full z-1">
          <ScrollArea class="h-50 w-full rounded-md bg-background shadow-lg">
            <div class="p-6 space-y-3">
              <div v-for="job in filteredJobs" :key="job" @mousedown="selectjob(job)"
                class="cursor-pointer rounded px-2 py-1 hover:bg-muted transition">
                {{ job.name }}
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>

      <!-- NOTE: Job Type Buttons/Icons -->
      <div class="flex flex-wrap items-center justify-center scale-[2] p-6 rounded-lg">
        <div class="flex flex-col items-center">
          <a href="#/Form">
            <Button class="p-1" variant="outline" size="icon" aria-label="Submit"> <img :src="drillImage"> </Button>
          </a>
          <div class="scale-[0.5] mt-1"> Home Repair </div>
        </div>
        <div class="flex flex-col items-center">
          <a href="#/Form">
            <Button class="p-1" variant="outline" size="icon" aria-label="Submit"> <img :src="garden"> </Button>
          </a>
          <div class="scale-[0.5] mt-1"> Gardening </div>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<style scoped></style>
