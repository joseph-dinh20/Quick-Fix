<script setup>
import { ref, computed } from 'vue'
import Footer from '@/components/Footer.vue'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'

import drillImage from '@/assets/icons/drill.png'
import garden from '@/assets/icons/garden.png'

const showScroll = ref(false)
const value = ref('')

const jobs = [
  { name: 'Home Repair' },
  { name: 'Gardening' },
  { name: 'Plumbing' },
  { name: 'Electrical' },
  { name: 'Cleaning' },
  { name: 'Moving Help' },
]

const featuredCategories = [
  { name: 'Home Repair', image: drillImage, query: 'Home Repair' },
  { name: 'Gardening', image: garden, query: 'Gardening' },
  { name: 'Plumbing', image: drillImage, query: 'Plumbing' },
  { name: 'Cleaning', image: garden, query: 'Cleaning' },
]

const filteredJobs = computed(() => {
  const query = value.value.toLowerCase().trim()

  if (!query) return jobs

  return jobs.filter(job =>
    job.name.toLowerCase().includes(query)
  )
})

function openScroll() {
  showScroll.value = true
}

function closeScroll() {
  setTimeout(() => {
    showScroll.value = false
  }, 120)
}

function selectJob(item) {
  value.value = item.name
  showScroll.value = false
}

function handleSearch() {
  if (!value.value.trim()) return
  window.location.hash = `/ProviderList?service=${encodeURIComponent(value.value.trim())}`
}
</script>

<template>
  <div class="flex flex-col min-h-screen items-center">
    <main class="w-full flex flex-col items-center px-6 pt-8 pb-16 text-green-800 flex-grow">
      <section class="w-full max-w-5xl flex flex-col items-center text-center gap-6 mt-4">
        <p class="text-sm uppercase tracking-[0.25em] text-green-700">
          QuickFix
        </p>

        <h1 class="text-5xl md:text-6xl font-bold leading-tight max-w-3xl">
          Get the job done today.
        </h1>

        <h2 class="text-4xl md:text-5xl font-bold leading-tight">
          No hassle.
        </h2>

        <p class="text-lg text-center max-w-2xl text-green-700">
          Find trusted help for everyday tasks, home projects, and quick fixes near you.
        </p>

        <div class="flex flex-wrap justify-center gap-3 pt-2">
          <a href="#/ProviderList">
            <Button>Find Services</Button>
          </a>

          <a href="#/Signup">
            <Button variant="outline">Join as Provider</Button>
          </a>
        </div>
      </section>

      <section class="w-full max-w-xl mt-14 relative">
        <div class="flex items-center gap-2">
          <Input
            type="text"
            v-model="value"
            @focus="openScroll"
            @blur="closeScroll"
            placeholder="Search services like plumbing, cleaning, or gardening"
          />

          <Button type="button" @click="handleSearch">
            Search
          </Button>
        </div>

        <div v-if="showScroll" class="absolute mt-2 w-full z-10">
          <ScrollArea class="h-[220px] w-full rounded-md border bg-background shadow-lg">
            <div class="p-3 space-y-2">
              <div
                v-for="job in filteredJobs"
                :key="job.name"
                @mousedown="selectJob(job)"
                class="cursor-pointer rounded px-3 py-2 hover:bg-muted transition"
              >
                {{ job.name }}
              </div>

              <div
                v-if="filteredJobs.length === 0"
                class="px-3 py-2 text-sm text-muted-foreground"
              >
                No matching services found.
              </div>
            </div>
          </ScrollArea>
        </div>
      </section>

      <section class="w-full max-w-4xl mt-16">
        <div class="text-center mb-6">
          <h3 class="text-2xl font-semibold">
            Popular Categories
          </h3>

          <p class="text-sm text-green-700 mt-2">
            Browse common services people book most often.
          </p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 place-items-center">
          <a
            v-for="category in featuredCategories"
            :key="category.name"
            :href="`#/ProviderList?service=${encodeURIComponent(category.query)}`"
            class="flex flex-col items-center gap-3 transition hover:scale-105"
          >
            <Button
              class="p-3 h-16 w-16 rounded-2xl"
              variant="outline"
              size="icon"
              aria-label="Category"
            >
              <img
                :src="category.image"
                :alt="category.name"
                class="h-8 w-8 object-contain"
              />
            </Button>

            <div class="text-sm font-medium text-center">
              {{ category.name }}
            </div>
          </a>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<style scoped></style>