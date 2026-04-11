<template>
  <div class="min-h-screen bg-slate-0 text-slate-900 p-6 md:p-12 font-sans relative">
    <div class="max-w-5xl mx-auto">
      
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight">Favorite Jobs</h1>
        <Button variant="ghost" size="icon" class="text-slate-700">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" x2="9" y1="3" y2="18"></line><line x1="15" x2="15" y1="6" y2="21"></line></svg>
        </Button>
      </div>

    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div class="relative w-full sm:w-[450px] flex items-center bg-white rounded-full border border-slate-200 shadow-sm p-1.5">
          <Search class="w-5 h-5 text-slate-400 ml-3 absolute" />
          <Input
            placeholder="Search postings"
            class="border-0 focus-visible:ring-0 shadow-none pl-10 bg-transparent w-full"
          />
          <Button class="text-white rounded-full px-6 py-2 shrink-0 h-auto font-bold">
            Search
          </Button>
        </div>

      </div>

      <div v-if="loading" class="flex flex-col gap-5">
        <Card v-for="n in 3" :key="n" class="flex flex-col sm:flex-row p-4 gap-6 items-center shadow-sm border-slate-200">
          <Skeleton class="w-full sm:w-48 h-32 rounded-lg" />
          <div class="flex-1 w-full space-y-3">
            <Skeleton class="h-6 w-3/4 sm:w-1/3" />
            <Skeleton class="h-4 w-1/2 sm:w-1/4" />
            <Skeleton class="h-4 w-1/3 sm:w-1/4" />
          </div>
          <Skeleton class="h-10 w-full sm:w-24 mt-4 sm:mt-0" />
        </Card>
      </div>

      <div v-else class="flex flex-col gap-5">
        <Card
          v-for="job in jobs.slice(0, 20)"
          :key="job.id"
          class="flex flex-col sm:flex-row items-start sm:items-center p-4 shadow-sm hover:shadow-md transition-shadow border-slate-200 gap-6"
        >
          <div class="w-full sm:w-48 h-32 flex-shrink-0 bg-slate-100 rounded-lg overflow-hidden">
            <img
              v-if="job.images && job.images.length"
              :src="job.images[0].image"
              alt="Job preview"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-slate-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect><circle cx="9" cy="9" r="2"></circle><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path></svg>
            </div>
          </div>

          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-bold text-slate-900 truncate">{{ job.title }}</h3>
            <div class="mt-1 flex flex-col gap-1">
              <p class="text-sm text-slate-500">{{ job.customer?.name || 'Unknown customer' }}</p>
              <p class="text-sm text-slate-500">{{ job.request_type || 'Request type not provided' }}</p>
            </div>
            <div class="mt-3">
              <span class="text-sm font-bold text-slate-900">
                {{ job.budget ? `$${job.budget}` : 'Budget not provided' }}
              </span>
              <span class="text-sm text-slate-500"> budget</span>
            </div>

            <div class="flex flex-wrap gap-2 mt-2">
              <span
                v-for="service in job.services"
                :key="service.id"
                class="text-xs bg-slate-100 px-2 py-1 rounded-md text-slate-600"
              >
                {{ service.name }}
              </span>
            </div>
          </div>

          <div class="flex flex-col sm:items-end w-full sm:w-auto gap-3 mt-4 sm:mt-0">
            <Button @click="markDone(job)" class="w-full sm:w-auto text-white font-semibold">
              Mark as Complete
            </Button>

            <Button
              variant="link"
              class="h-auto p-0 text-xs font-medium decoration-1 underline-offset-4"
              :class="'text-slate-500 hover:text-slate-800'"
              @click="openJobModal(job)"
            >
              <svg v-if="job.is_favorited" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1.5"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>
              View Job
            </Button>
          </div>
        </Card>
      </div>

      <div v-if="!loading && jobs.length > 20" class="flex items-center justify-center gap-2 mt-10">
        <Button variant="outline" disabled class="bg-white border-slate-200">
          Previous
        </Button>
        <Button variant="outline" class="bg-white border-slate-200 hover:bg-slate-100">
          Next
        </Button>
      </div>

    </div>

    <Dialog :open="isDialogOpen" @update:open="isDialogOpen = $event">
      <DialogContent class="max-w-2xl p-0 bg-white border-0 shadow-2xl overflow-hidden rounded-xl">
        <div v-if="selectedJob" class="p-8 max-h-[85vh] overflow-y-auto">

          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl md:text-3xl font-extrabold text-[#1a202c]">{{ selectedJob.title || 'Pest Control Help' }}</h2>
            <Button variant="ghost" size="icon" class="text-slate-700 hover:bg-slate-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            </Button>
          </div>

          <div v-if="selectedJob.images && selectedJob.images.length" class="relative flex items-center mb-10">
            <Button
              variant="ghost"
              size="icon"
              @click="scrollLeft"
              class="absolute -left-4 z-10 bg-white/80 hover:bg-white rounded-full shadow-sm h-8 w-8"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"></path></svg>
            </Button>

            <div ref="carousel" class="flex gap-4 overflow-x-auto snap-x snap-mandatory hide-scrollbar w-full px-4">
              <div
                v-for="img in selectedJob.images"
                :key="img.id"
                class="snap-center shrink-0 w-48 h-48 bg-slate-200 rounded-xl overflow-hidden"
              >
                <img
                  :src="img.image"
                  class="w-full h-full object-cover"
                />
              </div>
            </div>

            <Button
              variant="ghost"
              size="icon"
              @click="scrollRight"
              class="absolute -right-4 z-10 bg-white/80 hover:bg-white rounded-full shadow-sm h-8 w-8"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"></path></svg>
            </Button>
          </div>

          <hr class="border-slate-100 mb-8" />

          <div class="mb-8">
            <h3 class="font-bold text-[#1a202c] text-lg mb-6">Quick Details</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-4">

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                {{ selectedJob.customer?.name || 'Unknown customer' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><circle cx="12" cy="12" r="10"></circle><line x1="2" x2="22" y1="12" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                {{ selectedJob.languages || 'Not specified' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ selectedJob.request_type || 'Request type not provided' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                {{ selectedJob.urgency || 'Urgency not provided' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3">
                  <path d="M8 2v4"></path>
                  <path d="M16 2v4"></path>
                  <rect width="18" height="18" x="3" y="4" rx="2"></rect>
                  <path d="M3 10h18"></path>
                </svg>
                {{ selectedJob.deadline || 'No deadline provided' }}
              </div>

            </div>

            <div class="mt-6 pt-2">
              <span class="text-lg font-bold text-[#1a202c]">
                {{ selectedJob.budget ? `$${selectedJob.budget}` : 'Budget not provided' }}
              </span>
              <span class="text-base text-slate-500 font-medium"> budget</span>
            </div>
          </div>

          <hr class="border-slate-100 mb-8" />

          <div>
            <h3 class="font-bold text-[#1a202c] text-lg mb-4">About the Job</h3>
            <p class="text-slate-600 leading-relaxed whitespace-pre-wrap">{{ selectedJob.description || `No description` }}</p>
          </div>

        </div>
      </DialogContent>
    </Dialog>

  </div>
</template>

<script>
import { fetchAssignedJobs, completeJob } from "@/services/api"
// import { getFavoriteJobs, toggleFavoriteJob } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Dialog, DialogContent } from "@/components/ui/dialog";


export default {
  name: "JobsList",

  components: {
    Button,
    Card,
    Input,
    Skeleton,
    Dialog,
    DialogContent,
  },

  data() {
    return {
      jobs: [],
      loading: false,
      selectedJob: null,
      isDialogOpen: false,
    };
  },

  async mounted() {
    this.fetchJobs();
  },

  methods: {
    async fetchJobs() {
      this.loading = true;
      try {
        const res = await fetchAssignedJobs();
        const jobs = res.data.results || res.data;

        this.jobs = jobs.map((job) => ({
          ...job,
          images: (job.images || []).map((img) => ({
            ...img,
            image: img.image?.startsWith("http")
              ? img.image
              : `http://localhost:8000${img.image}`,
          })),
        }));
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async markDone(job) {
      try {
        const res = await completeJob(job.id)
        await this.loadJobs()
        console.log(res);
      } catch (err) {
        console.error(err);
      }
    },

    openJobModal(job) {
      this.selectedJob = job;
      this.isDialogOpen = true;
    },

    scrollLeft() {
      this.$refs.carousel?.scrollBy({
        left: -250,
        behavior: "smooth",
      });
    },

    scrollRight() {
      this.$refs.carousel?.scrollBy({
        left: 250,
        behavior: "smooth",
      });
    },
  },
};
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>