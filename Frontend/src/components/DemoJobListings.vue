<template>

  <div class="min-h-screen bg-slate-0 text-slate-900 p-6 md:p-12 font-sans relative">
    <div class="max-w-5xl mx-auto">
      
      <div class="flex items-center gap-4 mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight">Find work</h1>
        <Button variant="ghost" size="icon" class="text-slate-700"
          @click="navigate('#/DemoMap?view=jobs')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" x2="9" y1="3" y2="18"></line><line x1="15" x2="15" y1="6" y2="21"></line></svg>
        </Button>
      </div>

      <Card class="flex flex-col md:flex-row items-center rounded-full p-2 mb-3 shadow-sm border-slate-200 gap-2 md:gap-0">
        <ServiceSearchSelect class="flex-1 px-4 w-50" v-model="pendingService" placeholder="Enter your task..." />
        <div class="hidden md:block w-[1px] h-8 bg-slate-200"></div>
        <div class="flex items-center flex-1 px-4 w-full border-t md:border-none border-slate-100 pt-2 md:pt-0 mt-2 md:mt-0">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 mr-3"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          <Input
            v-model="pendingLocation" placeholder="City, State, Zip Code"
          />
        </div>
        <Button @click="searchJobsHandler" class="w-full md:w-auto text-white rounded-full px-8 py-2.5">
          Search
        </Button>
      </Card>

      <div class="flex flex-wrap gap-3 mb-10">
        <Select v-model="pendingDistance">
          <SelectTrigger class="border p-2 rounded w-30">
            <SelectValue placeholder="Distance" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="5">5 Miles</SelectItem>
            <SelectItem value="10">10 Miles</SelectItem>
            <SelectItem value="15">15 Miles</SelectItem>
            <SelectItem value="20">20 Miles</SelectItem>
            <SelectItem value="25">25 Miles</SelectItem>
            <SelectItem value="30">30 Miles</SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="pendingBudget">
          <SelectTrigger class="border p-2 rounded w-30">
            <SelectValue placeholder="Budget" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="0">$0</SelectItem>
            <SelectItem value="25">$25</SelectItem>
            <SelectItem value="50">$50</SelectItem>
            <SelectItem value="75">$75</SelectItem>
            <SelectItem value="100">$100</SelectItem>
            <SelectItem value="150">$150</SelectItem>
            <SelectItem value="200">$200+</SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="pendingJobType">
          <SelectTrigger class="border p-2 rounded w-30">
            <SelectValue placeholder="All Types" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value=".">All Type</SelectItem>
            <SelectItem value="quote">Quote</SelectItem>
            <SelectItem value="service">Service</SelectItem>
            <SelectItem value="both">Both</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div v-if="loading" class="flex flex-col gap-5">
        <Card v-for="n in 4" :key="n" class="flex flex-col sm:flex-row p-4 gap-6 items-center shadow-sm border-slate-200">
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
        <div v-if="!jobs.length && !jobList.length" class="text-sm text-muted-foreground text-center mt-4">
          No results found.
        </div>
        
        <Card
          v-for="job in filteredJobs.slice(0, 20)"
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
              <p class="text-sm text-slate-500">
                by {{ job.customer?.name || job.user_name || 'Unknown customer' }}
              </p>
              <p class="text-sm text-slate-500 capitalize">{{ job.request_type || 'Location not found' }}</p>
              <p class="text-sm text-slate-500">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline mr-1 mb-0.5"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ job.city }}, {{ job.state || 'California' }}
              </p>
            </div>
            
            <div class="mt-3">
              <span class="text-sm font-bold text-slate-900">
                {{ job.budget ? `$${job.budget}` : '$0' }}
              </span>
              <span class="text-sm text-slate-500"> / hr</span>
            </div>

            <div class="flex flex-wrap gap-2 mt-2">
              <span
                v-for="service in job.services"
                :key="service.id || service"
                class="text-xs bg-slate-100 px-2 py-1 rounded-md text-slate-600"
              >
                {{ service.name || service }}
              </span>
            </div>
          </div>

          <div class="flex flex-col sm:items-end w-full sm:w-auto gap-3 mt-4 sm:mt-0">
            <!-- View Job modal button (unchanged) -->
            <Button @click="openJobModal(job)" class="w-full sm:w-auto text-white font-semibold">
              View Job
            </Button>

            <Button
              variant="link"
              @click="toggle(job)"
              class="h-auto p-0 text-xs font-medium decoration-1 underline-offset-4"
              :class="job.is_favorited ? 'text-primary' : 'text-slate-500 hover:text-slate-800'"
            >
              <svg v-if="job.is_favorited" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1.5"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>
              {{ job.is_favorited ? "Favorite" : "Save to Favorites" }}
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
                <img :src="img.image" class="w-full h-full object-cover" />
              </div>
              <div class="snap-center shrink-0 w-48 h-48 bg-green-300 rounded-xl overflow-hidden"></div>
              <div class="snap-center shrink-0 w-48 h-48 rounded-xl overflow-hidden"></div>
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
                {{ selectedJob.customer?.name || selectedJob.user_name || 'Unknown customer' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><circle cx="12" cy="12" r="10"></circle><line x1="2" x2="22" y1="12" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                {{ selectedJob.languages || 'English' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ selectedJob.city + ', ' + (selectedJob.state || 'California') }}
              </div>

              <div class="flex items-center text-slate-600 font-medium capitalize">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                {{ selectedJob.urgency || 'Urgency not provided' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M8 2v4"></path><path d="M16 2v4"></path><rect width="18" height="18" x="3" y="4" rx="2"></rect><path d="M3 10h18"></path></svg>
                {{ formatDate(selectedJob.deadline) }}
              </div>

              <div class="flex items-center text-slate-600 font-medium capitalize">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                {{ selectedJob.request_type || 'Location not found' }}
              </div>

            </div>

            <div class="mt-6 pt-2">
              <span class="text-lg font-bold text-[#1a202c]">
                {{ selectedJob.budget ? `$${selectedJob.budget}` : '$0' }}
              </span>
              <span class="text-base text-slate-500 font-medium mr-5"> / hr</span>

              <span
                v-for="service in selectedJob.services"
                :key="service.id || service"
                class="text-xs bg-slate-100 px-2 py-1 rounded-md text-slate-600 ml-2"
              >
                {{ service.name || service }}
              </span>
            </div>
          </div>

          <hr class="border-slate-100 mb-8" />

          <div>
            <h3 class="font-bold text-[#1a202c] text-lg mb-4">About the Job</h3>
            <p class="text-slate-600 leading-relaxed whitespace-pre-wrap">{{ selectedJob.description || `No description` }}</p>
          </div>
          <hr class="border-slate-100 mb-8" />

          <!-- Application Form -->
          <div>
            <h3 class="font-bold text-[#1a202c] text-lg mb-5">Your Application</h3>

            <div v-if="selectedJob.applied" class="rounded-xl bg-green-50 border border-green-200 p-4 text-green-700 text-sm font-medium">
              ✓ You've already applied to this job.
            </div>

            <div v-else class="flex flex-col gap-4">
              <!-- Rate -->
              <div class="flex gap-3">
                <div class="flex-1">
                  <label class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1 block">Proposed Rate</label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-medium">$</span>
                    <Input
                      v-model="applicationForm.proposedRate"
                      type="number"
                      min="0"
                      placeholder="0"
                      class="pl-7"
                    />
                  </div>
                </div>
                <div class="w-36">
                  <label class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1 block">Rate Type</label>
                  <Select v-model="applicationForm.rateType">
                    <SelectTrigger>
                      <SelectValue placeholder="Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="hourly">Per Hour</SelectItem>
                      <SelectItem value="flat">Flat Rate</SelectItem>
                      <SelectItem value="daily">Per Day</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <!-- Availability -->
              <div class="flex gap-3">
                <div class="flex-1">
                  <label class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1 block">Available Date</label>
                  <Input v-model="applicationForm.availableDate" type="date" />
                </div>
                <div class="flex-1">
                  <label class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1 block">Available Time</label>
                  <Input v-model="applicationForm.availableTime" type="time" />
                </div>
              </div>

              <!-- Cover Note -->
              <div>
                <label class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1 block">Cover Note</label>
                <textarea
                  v-model="applicationForm.coverNote"
                  rows="3"
                  placeholder="Briefly introduce yourself and why you're a good fit..."
                  class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring resize-none"
                />
              </div>

              <Button
                class="w-full text-white font-semibold"
                :disabled="!applicationForm.proposedRate"
                @click="applyToJob(selectedJob)"
              >
                Submit Application
              </Button>
            </div>
          </div>

        </div>
      </DialogContent>
    </Dialog>

  </div>


</template>

<script setup>
import { searchJobs, toggleFavoriteJob } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import ServiceSearchSelect from "@/components/ServiceSearchSelect.vue"
import { ref, onMounted, computed } from "vue"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { storeToRefs } from "pinia";


import { useJobStore } from "@/store/jobStore";
import { useUserStore, ALL_USERS } from "@/store/userStore";
import { useApplicationStore } from "@/store/applicationStore";

const jobStore  = useJobStore();
const userStore = useUserStore();

const { jobList } = storeToRefs(jobStore);

const services      = ref([]);
const jobs          = ref([]);
const loading       = ref(false);
const selectedJob   = ref(null);
const isDialogOpen  = ref(false);

const applicationForm = ref({
  proposedRate: "",
  rateType: "hourly",
  availableDate: "",
  availableTime: "",
  coverNote: "",
});

const pendingDistance = ref('');
const pendingBudget   = ref('');
const pendingJobType  = ref('');
const pendingService  = ref('');
const pendingLocation = ref('');

const searchLocation   = ref("");
const selectedDistance = ref("");
const selectedBudget   = ref("");
const selectedJobType  = ref("");
const selectedService  = ref(null);

const backendAvailable = ref(true);

onMounted(() => {
  fetchServices();
  fetchJobs();
});

const navigate = (path) => {
  window.location.hash = path;
};

function formatDate(date) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

function getUserName(job) {
  const savedProfile = userStore.profiles[job.user_id];
  if (savedProfile?.name) return savedProfile.name;

  const user = ALL_USERS.find(u => u.id === job.user_id);
  if (user) return user.name;

  if (job.provider_id) {
    const provider = ALL_USERS.find(u => u.providerId === job.provider_id);
    if (provider) return provider.name;
  }

  return "Unknown User";
}

const filteredJobs = computed(() => {
  if (backendAvailable.value) return jobs.value;

  return jobs.value.filter(job => {
    if (selectedService.value) {
      const q = selectedService.value.toLowerCase();
      if (!job.service?.toLowerCase().includes(q) && !job.title?.toLowerCase().includes(q)) return false;
    }
    if (searchLocation.value) {
      const q = searchLocation.value.toLowerCase();
      if (!job.city?.toLowerCase().includes(q) && !job.state?.toLowerCase().includes(q)) return false;
    }
    if (selectedBudget.value && (job.budget ?? 0) < Number(selectedBudget.value)) return false;
    if (selectedJobType.value && job.request_type !== selectedJobType.value) return false;
    if (selectedDistance.value) {
      const dist = getDistanceMiles(33.7701, -118.1937, job.lat, job.lng);
      if (dist > Number(selectedDistance.value)) return false;
    }
    return true;
  });
});

function getDistanceMiles(lat1, lng1, lat2, lng2) {
  const R = 3958.8;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2) ** 2 +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLng/2) ** 2;
  return R * 2 * Math.asin(Math.sqrt(a));
}

async function fetchServices() {
  try {
    const res = await fetch("http://localhost:8000/api/services/");
    services.value = await res.json();
  } catch {
    // backend unavailable — silently ignore
  }
}

async function fetchJobs() {
  loading.value = true;

  try {
    const res = await searchJobs({
      services: selectedService.value || undefined,
      budget: selectedBudget.value || undefined,
      request_type: selectedJobType.value || undefined,
      max_distance: selectedDistance.value || undefined,
      location: searchLocation.value || undefined
    });
    
    // simulate API delay (optional but makes it feel real)
    await new Promise((r) => setTimeout(r, 300));

    const data = jobStore.getMergedJobs();

    console.log("demo jobs loaded:", data.length);

    jobs.value = data.map((job, index) => ({
      ...fallbackJob(
        job,
        index,
        { lat: 33.7701, lng: -118.1937 },
        getUserName
      ),
      images: job.images || [],
    }));

    backendAvailable.value = false;
  } catch (err) {
    console.error(err);
    jobs.value = [];
  } finally {
    loading.value = false;
  }
}

async function toggle(job) {
  try {
    const res = await toggleFavoriteJob(job.id);
    job.is_favorited = res.data.favorited;
  } catch {
    jobStore.toggleFavorite(job.job_id);
    job.is_favorited = jobStore.isFavorited(job.job_id);
  }
}

function openJobModal(job) {
  selectedJob.value = {
    ...job,
    applied: jobStore.hasApplied(job.job_id, userStore.currentUser?.id),
  };
  applicationForm.value = { proposedRate: "", rateType: "hourly", availableDate: "", availableTime: "", coverNote: "" };
  isDialogOpen.value = true;
}

async function applyToJob(job) {
  if (!userStore.isProvider) {
    alert("Only service providers can apply.");
    return;
  }

  const success = jobStore.applyToJob(job.job_id, userStore.currentUser.id, applicationForm.value);

  if (!success) {
    alert("You already applied.");
    return;
  }

  selectedJob.value = { ...selectedJob.value, applied: true };
}

function scrollLeft() {
  document.querySelector('.carousel')?.scrollBy({ left: -250, behavior: "smooth" });
}

function scrollRight() {
  document.querySelector('.carousel')?.scrollBy({ left: 250, behavior: "smooth" });
}

function searchJobsHandler() {
  searchLocation.value  = pendingLocation.value;
  selectedService.value = pendingService.value;
  selectedDistance.value = pendingDistance.value;
  selectedBudget.value  = pendingBudget.value;
  selectedJobType.value = pendingJobType.value === '.' ? '' : pendingJobType.value;
  fetchJobs();
}

function fallbackJob(job, index = 0, coords = { lat: 33.7701, lng: -118.1937 }, getUserName) {
  return {
    job_id:       job.job_id || `fallback_${index + 1}`,
    user_id:      job.user_id || "u_fallback",
    user_name:    getUserName(job),
    provider_id:  job.provider_id ?? 0,
    title:        job.title       || "Untitled Job",
    description:  job.description || "No description provided",
    services:     [job.service]   || ["General Repair"],
    budget:       job.price       ?? 0,
    city:         job.city        || "Long Beach",
    state:        job.state       || "California",
    lat:          Number(job.lat  ?? coords.lat),
    lng:          Number(job.lng  ?? coords.lng),
    language:     job.language    || "English",
    urgency:      job.urgency     || "normal",
    deadline:     job.date        || new Date().toISOString(),
    request_type: job.request_type || "quote",
    is_favorited: jobStore.isFavorited(job.job_id) ?? false,
  };
}
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>