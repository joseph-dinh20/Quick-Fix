<script setup>
import { ref, computed, onMounted } from "vue";
import Footer from "@/components/Footer.vue";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
// Importing Images
import drillImage from "@/assets/icons/drill.png";
import garden from "@/assets/icons/garden.png";

const showScroll = ref(false);
const value = ref("");

const jobs = [{ name: "Home Maintenance" }, { name: "Gardening" }];

// NOTE: first 2 lines of the Main page
const pageOneText = [
  {
    text: "Small problems can turn into big issues tomorrow",
    class: "text-4xl font-bold text-gray-900",
  },
  {
    text: "Schedule an appointment today.",
    class:
      "text-2xl font-semibold text-green-600 underline underline-offset-10",
  },
];

// NOTE: Bottom 3 animated texts
const featureItems = [
  {
    title: "Mission Statement",
    description:
      "Create a solution for clients and handy individuals to collaborate together.",
  },
  {
    title: "Simple Pricing Model",
    description:
      "We charge a flat rate of $10 per job completion as the middleman, no matter the amount of hours. No hidden fees. We are dedicated to create the lowest cost of middleman fees for a good experience from both the client and contractors.",
  },
  {
    title: "Background Checks",
    description:
      "Independent contractors sign up through our platform will undergo a criminial background check to increase the safety of customers",
  },
];

// NOTE: Track visibility per feature item
const featureVisible = ref(featureItems.map(() => false));

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const index = Number(entry.target.dataset.index);
          featureVisible.value[index] = true;
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 },
  );
  // WARN: using vanilla JS DOM. Not the recommended Vue.js way of doing it.
  document.querySelectorAll(".feature-item").forEach((el) => {
    observer.observe(el);
  });
});

const filteredJobs = computed(() => {
  const query = value.value.toLowerCase();
  return jobs.filter((job) => job.name.toLowerCase().includes(query));
});

function showScrollState() {
  showScroll.value = !showScroll.value;
}

function selectjob(item) {
  value.value = item.name;
}

// WARN: quick and dirty way to re-route in the search bar
function handleSearch() {
  const match = jobs.find(
    (job) => job.name.toLowerCase() === value.value.toLowerCase(),
  );
  if (match) {
    window.location.hash = "#/Form";
  }
  console.log("HandleSearhc() function called");
}
</script>

<template>
  <div
    class="flex flex-col items-center mt-30 bg-linear-to-b from-white from-0% via-white-500 via-5% to-green-300 to-100%"
  >
    <main class="w-full flex flex-col items-center justify-center">
      <!-- NOTE: PageOneText — all pop up at once -->
      <div
        class="animate__animated animate__fadeInUp flex flex-col items-center gap-4"
      >
        <div class="flex flex-col items-center gap-2">
          <div v-for="(text, i) in pageOneText" :key="i" :class="text.class">
            {{ text.text }}
          </div>
        </div>

        <!-- NOTE: Search Box -->
        <div class="w-full max-w-sm relative">
          <div class="mt-10 flex items-center gap-2">
            <Input
              type="text"
              v-model="value"
              @focus="showScrollState"
              @blur="showScrollState"
              placeholder="What do you need help with?"
              class="border-2 border-stone-600 rounded-lg"
            />
            <Button type="submit" @click="handleSearch">Search</Button>
          </div>
          <div v-if="showScroll" class="absolute mt-1 w-full z-10">
            <ScrollArea class="h-50 w-full rounded-md bg-background shadow-lg">
              <div class="p-6 space-y-3">
                <div
                  v-for="job in filteredJobs"
                  :key="job.name"
                  @mousedown="selectjob(job)"
                  class="cursor-pointer rounded px-2 py-1 hover:bg-muted transition"
                >
                  {{ job.name }}
                </div>
              </div>
            </ScrollArea>
          </div>
        </div>

        <!-- NOTE: Job Type Buttons/Icons -->
        <div
          class="mt-10 flex flex-wrap items-center justify-center scale-[1.8] p-6 rounded-lg"
        >
          <div class="flex flex-col items-center">
            <a href="#/Form">
              <Button
                class="p-1"
                variant="outline"
                size="icon"
                aria-label="Submit"
              >
                <img :src="drillImage" />
              </Button>
            </a>
            <div class="scale-[0.5] mt-1">Home Repair</div>
          </div>
          <div class="flex flex-col items-center">
            <a href="#/Form">
              <Button
                class="p-1"
                variant="outline"
                size="icon"
                aria-label="Submit"
              >
                <img :src="garden" />
              </Button>
            </a>
            <div class="scale-[0.5] mt-1">Gardening</div>
          </div>
        </div>
      </div>
    </main>

    <!-- NOTE: Scroll-triggered feature sections (right to left) -->
    <!-- This lives below the fold — user must scroll to trigger animations -->
    <section
      class="w-full min-h-screen flex flex-col items-center justify-center px-6 py-20"
    >
      <div class="max-w-2xl w-full flex flex-col gap-10">
        <div
          v-for="(item, i) in featureItems"
          :key="i"
          :data-index="i"
          class="feature-item"
          :class="
            featureVisible[i]
              ? 'animate__animated animate__fadeInRight'
              : 'opacity-0'
          "
          :style="{ animationDelay: `${i * 0.15}s` }"
        >
          <h3 class="text-2xl font-bold text-green-700">{{ item.title }}</h3>
          <p class="text-base text-muted-foreground mt-2">
            {{ item.description }}
          </p>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<style scoped></style>
