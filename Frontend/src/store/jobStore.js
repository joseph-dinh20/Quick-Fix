import { defineStore } from "pinia";
import { ref } from "vue";
import jobsData from "@/store/data/jobs.json";
import { useUserStore } from "@/store/userStore";

export const useJobStore = defineStore(
  "job",
  () => {
    const jobList = ref(jobsData);
    const edits = ref({});
    const favorites = ref(new Set());

    function getFavoritesKey() {
      const userStore = useUserStore();
      return `favoritedJobs_${userStore.currentUser?.id || 'guest'}`;
    }

    function loadFavorites() {
      favorites.value = new Set(JSON.parse(localStorage.getItem(getFavoritesKey()) || '[]'));
    }

    function toggleFavorite(jobId) {
      if (favorites.value.has(jobId)) {
        favorites.value.delete(jobId);
      } else {
        favorites.value.add(jobId);
      }
      localStorage.setItem(getFavoritesKey(), JSON.stringify([...favorites.value]));
    }

    function isFavorited(jobId) {
      console.log('Type:', typeof favorites.value, 'Value:', favorites.value);
      return favorites.value.has(jobId);
    }

    function saveJob(jobId, updates) {
      const existing = edits.value[jobId] || {};
      edits.value = {
        ...edits.value,
        [jobId]: { ...existing, ...updates },
      };
    }

    function getMergedJob(jobId) {
      const seed = jobsData.find((j) => j.job_id === jobId);
      if (!seed) return null;
      const edit = edits.value[jobId] || {};
      return { ...seed, ...edit };
    }

    function getMergedJobs() {
      return jobsData.map((j) => getMergedJob(j.job_id));
    }

    function getJobsByUser(userId) {
      return getMergedJobs().filter((job) => job.user_id === userId);
    }

    function getJobsByProvider(providerId) {
      return getMergedJobs().filter((job) => job.provider_id === providerId);
    }

    function getJobsByService(service) {
      return getMergedJobs().filter((job) => job.service === service);
    }

    function getJobsByUrgency(urgency) {
      return getMergedJobs().filter((job) => job.urgency === urgency);
    }

    function getFavoritedJobs() {
      return getMergedJobs().filter((job) => isFavorited(job.job_id));
    }

    return {
      jobList,
      edits,
      favorites,
      saveJob,
      getMergedJob,
      getMergedJobs,
      getJobsByUser,
      getJobsByProvider,
      getJobsByService,
      getJobsByUrgency,
      getFavoritedJobs,
      loadFavorites,
      toggleFavorite,
      isFavorited,
    };
  },
  { persist: 
    {
      pick: ["edits"],
    },
 }
);