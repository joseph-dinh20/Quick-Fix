<template>
  <div class="min-h-screen bg-slate-0 text-slate-900 p-6 md:p-12 font-sans relative">
    <div class="max-w-5xl mx-auto">
      
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight">Assigned Jobs</h1>
        <Button variant="ghost" size="icon" class="text-slate-700"
        @click="navigate('#/DemoMap?view=jobs')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" x2="9" y1="3" y2="18"></line><line x1="15" x2="15" y1="6" y2="21"></line></svg>
        </Button>
      </div>

    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div class="relative w-full sm:w-[450px] flex items-center bg-white rounded-full border border-slate-200 shadow-sm p-1.5">
          <Search class="w-5 h-5 text-slate-400 ml-3 absolute" />
          <Input
            v-model="searchQuery"
            placeholder="Search postings"
            class="border-0 focus-visible:ring-0 shadow-none pl-10 bg-transparent w-full"
          />
          <Button @click="applySearch" class="text-white rounded-full px-6 py-2 shrink-0 h-auto font-bold">
            Search
          </Button>
        </div>

        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="bg-white border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg flex items-center gap-2 shadow-sm px-4 capitalize">
              {{ currentSort }}
              <ChevronDown class="w-4 h-4 text-slate-500 ml-1" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="w-40">
            <DropdownMenuItem @click="updateSort('Newest')">Newest</DropdownMenuItem>
            <DropdownMenuItem @click="updateSort('Oldest')">Oldest</DropdownMenuItem>
            <DropdownMenuItem @click="updateSort('Title (A-Z)')">Title (A-Z)</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

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

      <!-- Empty state when no accepted jobs -->
      <div v-else-if="filteredJobs.length === 0" class="text-center py-20 text-slate-400">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
          stroke-linejoin="round" class="mx-auto mb-4 opacity-40">
          <rect width="18" height="18" x="3" y="3" rx="2"></rect>
          <path d="m9 12 2 2 4-4"></path>
        </svg>
        <p class="text-lg font-medium">No assigned jobs yet</p>
        <p class="text-sm mt-1">Jobs will appear here once a client accepts your application.</p>
      </div>

      <div v-else class="flex flex-col gap-5">
        <Card
          v-for="job in filteredJobs.slice(0, 20)"
          :key="job.job_id || job.id"
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
              <p class="text-sm text-slate-500">by {{ job.customer?.name || job.customer || customerName(job.user_id) }}</p>
              <p class="text-sm text-slate-500">{{ job.city }}{{ job.state ? ', ' + job.state : '' }}</p>
            </div>
            <div class="mt-3">
              <span class="text-sm font-bold text-slate-900">
                {{ job.budget || job.price ? `$${job.budget || job.price}` : '$0' }}
              </span>
              <span class="text-sm text-slate-500 mr-3"> / hr</span>
              <!-- Show "Accepted" badge to reflect that this job was assigned via acceptance -->
              <Badge
                variant="outline"
                class="font-medium px-2.5 py-0.5 rounded-md bg-green-50 text-green-600 border-green-200"
              >
                Accepted
              </Badge>
            </div>

            <div class="flex flex-wrap gap-2 mt-2">
              <span
                v-if="job.service"
                class="text-xs bg-slate-100 px-2 py-1 rounded-md text-slate-600"
              >
                {{ job.service }}
              </span>
              <span
                v-for="service in (job.services || [])"
                :key="service.id || service"
                class="text-xs bg-slate-100 px-2 py-1 rounded-md text-slate-600"
              >
                {{ service.name || service }}
              </span>
            </div>
          </div>

          <div class="flex flex-col sm:items-end w-full sm:w-auto gap-3 mt-4 sm:mt-0">
            <Button
              @click="markDone(job)"
              class="w-full sm:w-auto text-white font-semibold"
              :disabled="job.status === 'Complete' || job.status === 'complete'"
            >
              {{ job.status === 'Complete' || job.status === 'complete' ? 'Completed' : 'Mark as Complete' }}
            </Button>

            <Button
              variant="link"
              class="h-auto p-0 text-xs font-medium decoration-1 underline-offset-4 text-slate-500 hover:text-slate-800"
              @click="openJobModal(job)"
            >
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
            <h2 class="text-2xl md:text-3xl font-extrabold text-[#1a202c]">{{ selectedJob.title || 'Job Details' }}</h2>
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
                {{ selectedJob.customer?.name || selectedJob.customer || customerName(selectedJob.user_id) }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ selectedJob.city }}{{ selectedJob.state ? ', ' + selectedJob.state : '' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><line x1="12" x2="12" y1="2" y2="22"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                ${{ selectedJob.budget || selectedJob.price || 0 }} / hr
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                {{ selectedJob.service || 'General' }}
              </div>

            </div>
          </div>

          <div v-if="selectedJob.description" class="mb-6">
            <h3 class="font-bold text-[#1a202c] text-lg mb-3">Description</h3>
            <p class="text-slate-600 text-sm leading-relaxed">{{ selectedJob.description }}</p>
          </div>

        </div>
      </DialogContent>
    </Dialog>

  </div>
</template>

<script>
import { fetchAssignedJobs, completeJob } from "@/services/api"
import { storeToRefs } from "pinia";
import { useJobStore } from "@/store/jobStore";
import { useUserStore, ALL_USERS } from "@/store/userStore";
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ChevronDown, Search } from 'lucide-vue-next'


export default {
  name: "JobsList",

  components: {
    Button,
    Card,
    Input,
    Skeleton,
    Dialog,
    DialogContent,
    Badge,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    ChevronDown,
    Search,
  },

  data() {
    return {
      jobStore: useJobStore(),
      userStore: useUserStore(),
      jobs: [],
      loading: false,
      selectedJob: null,
      isDialogOpen: false,
      searchQuery: '',
      displayQuery: '',
      currentSort: 'Sort by',
      backendAvailable: true,
    };
  },
  
  computed: {
    filteredJobs() {
      let result = [...this.jobs]

      if (this.currentSort === 'Newest') {
        result.sort((a, b) => new Date(b.deadline || b.date || 0) - new Date(a.deadline || a.date || 0))
      } else if (this.currentSort === 'Oldest') {
        result.sort((a, b) => new Date(a.deadline || a.date || 0) - new Date(b.deadline || b.date || 0))
      } else if (this.currentSort === 'Title (A-Z)') {
        result.sort((a, b) => (a.title || '').localeCompare(b.title || ''))
      }

      if (!this.displayQuery.trim()) return result
      const q = this.displayQuery.toLowerCase()
      return result.filter(job =>
        (job.title || '').toLowerCase().includes(q) ||
        (job.description || '').toLowerCase().includes(q) ||
        (job.city || '').toLowerCase().includes(q)
      )
    }
  },

  async mounted() {
    this.fetchJobs();
  },

  methods: {
    navigate(path) {
      window.location.hash = path;
    },

    applySearch() {
      this.displayQuery = this.searchQuery
    },

    updateSort(sortOption) {
      this.currentSort = sortOption
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      })
    },

    // Resolve a customer display name from user_id using ALL_USERS
    customerName(userId) {
      const user = ALL_USERS.find(u => u.id === userId);
      return user?.name || 'Unknown Customer';
    },

    fallbackJob(job, index = 0) {
      const customer = ALL_USERS.find(u => u.id === job.user_id);
      return {
        job_id: job.job_id || `fallback_${index + 1}`,
        user_id: job.user_id || "u_fallback",
        provider_id: job.provider_id ?? 0,
        title: job.title || "Untitled Job",
        description: job.description || "No description provided",
        services: job.service ? [job.service] : ["General Repair"],
        service: job.service || "General Repair",
        budget: job.price ?? 0,
        city: job.city || "Long Beach",
        state: job.state || "California",
        lat: Number(job.lat ?? 33.7701),
        lng: Number(job.lng ?? -118.1937),
        languages: job.language || "English",
        urgency: job.urgency || "normal",
        deadline: job.date || new Date().toISOString(),
        request_type: job.request_type || "quote",
        is_favorited: job.is_favorited ?? false,
        // Store the status as "Accepted" since these came from accepted decisions
        status: "Accepted",
        customer: customer?.name || "Unknown Customer",
        images: job.images || [],
      };
    },

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
        console.error("Backend unavailable, using accepted jobs from decisions store", err);

        // ── CORE FIX ──────────────────────────────────────────────────────────
        // Use getAcceptedJobsForProvider instead of filtering by provider_id.
        // This reads the global decisions store so only jobs where the client
        // actually clicked "Accept" on the provider's application show up.
        const currentUserId = this.userStore.currentUser?.id;
        if (currentUserId) {
          const acceptedJobs = this.jobStore.getAcceptedJobsForProvider(currentUserId);
          this.jobs = acceptedJobs.map((job, index) => this.fallbackJob(job, index));
        } else {
          this.jobs = [];
        }

        this.backendAvailable = false;
      } finally {
        this.loading = false;
      }
    },

    async markDone(job) {
      try {
        const res = await completeJob(job.id)
        await this.fetchJobs()
        console.log(res);
      } catch (err) {
        console.error(err);
        // Update locally in both stores
        this.jobStore.saveJob(job.job_id, { status: "Complete" });
        job.status = "Complete";
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