<!-- THIS PAGE LISTS ALL JOB POSTINGS (viewable for users not signed in) AND ALSO ALLOWS TOGGLING FAVORITING JOBS (if service provider) -->
<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 p-6 md:p-12 font-sans">
    <div class="max-w-5xl mx-auto">
      
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight">Find work</h1>
        <Button variant="ghost" size="icon" class="text-slate-700">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" x2="9" y1="3" y2="18"></line><line x1="15" x2="15" y1="6" y2="21"></line></svg>
        </Button>
      </div>

      <Card class="flex flex-col md:flex-row items-center rounded-full p-2 mb-8 shadow-sm border-slate-200 gap-2 md:gap-0">
        <div class="flex items-center flex-1 px-4 w-full">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 mr-3"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>
          <Input 
            variant="ghost" 
            placeholder="What do you need done?" 
            class="border-0 focus-visible:ring-0 shadow-none h-10 px-0 w-full" 
          />
        </div>
        <div class="hidden md:block w-[1px] h-8 bg-slate-200"></div>
        <div class="flex items-center flex-1 px-4 w-full border-t md:border-none border-slate-100 pt-2 md:pt-0 mt-2 md:mt-0">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400 mr-3"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          <Input 
            variant="ghost" 
            placeholder="City, State, Zip Code" 
            class="border-0 focus-visible:ring-0 shadow-none h-10 px-0 w-full" 
          />
        </div>
        <Button class="w-full md:w-auto bg-orange-500 hover:bg-orange-600 text-white rounded-full px-8 py-2.5">
          Search
        </Button>
      </Card>

      <div class="flex flex-wrap gap-3 mb-10">
        <Button 
          v-for="filter in ['Pay', 'Language', 'Urgency', 'Type', 'Credentials']" 
          :key="filter" 
          variant="outline" 
          class="bg-white border-slate-200 text-slate-700 hover:bg-slate-50 flex items-center"
        >
          {{ filter }}
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2 text-slate-500"><path d="m6 9 6 6 6-6"></path></svg>
        </Button>
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
              v-if="job.image_url" 
              :src="job.image_url" 
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
              <p class="text-sm text-slate-500">{{ job.id  || 'Joseph E.' }}</p>
              <p class="text-sm text-slate-500">{{ job.location || 'Long Beach, CA' }}</p>
            </div>
            <div class="mt-3">
              <span class="text-sm font-bold text-slate-900">{{ job.budget || '$40' }}</span>
              <span class="text-sm text-slate-500"> an hour</span>
            </div>
          </div>

          <div class="flex flex-col sm:items-end w-full sm:w-auto gap-3 mt-4 sm:mt-0">
            <Button class="w-full sm:w-auto bg-orange-500 hover:bg-orange-600 text-white font-semibold">
              View Job
            </Button>
            
            <Button 
              variant="link" 
              @click="toggle(job)" 
              class="h-auto p-0 text-xs font-medium decoration-1 underline-offset-4"
              :class="job.is_favorited ? 'text-orange-500' : 'text-slate-500 hover:text-slate-800'"
            >
              <svg v-if="job.is_favorited" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1.5"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>
              {{ job.is_favorited ? "Favorited" : "Save to Favorites" }}
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
  </div>
</template>

<script>
import { getAllJobs, toggleFavoriteJob } from "@/services/api";

export default {
  name: "JobsList",

  data() {
    return {
      jobs: [],
      loading: false,
    };
  },

  async mounted() {
    this.fetchJobs();
  },

  methods: {
    async fetchJobs() {
      this.loading = true;
      try {
        const res = await getAllJobs();
        this.jobs = res.data.results || res.data; // handles pagination or not
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async toggle(job) {
      try {
        const res = await toggleFavoriteJob(job.id);
        job.is_favorited = res.data.favorited;
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.jobs-container {
  max-width: 800px;
  margin: auto;
}

.job-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 10px;
}

.job-info {
  max-width: 70%;
}

.job-actions button {
  padding: 6px 12px;
  cursor: pointer;
}
</style>