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
    const applications = ref({});

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

    function getAppliedJobIds(userId) {
      return Object.entries(applications.value)
        .filter(([jobId, entries]) =>
          entries.some(
            (entry) => (typeof entry === "string" ? entry : entry.userId) === userId
          )
        )
        .map(([jobId]) => jobId);
    }

    function saveJob(jobId, updates) {
      const existing = edits.value[jobId] || {};
      edits.value = {
        ...edits.value,
        [jobId]: { ...existing, ...updates },
      };
    }

    function getApplicationsKey() {
      const userStore = useUserStore();
      return `applications_${userStore.currentUser?.id || "guest"}`;
    }

    function loadApplications() {
      applications.value = JSON.parse(
        localStorage.getItem(getApplicationsKey()) || "{}"
      );
    }

    function initApplications() {
      loadApplications();
    }

    function saveApplications() {
      localStorage.setItem(
        getApplicationsKey(),
        JSON.stringify(applications.value)
      );
    }

    function applyToJob(jobId, userId, formData = {}) {
      if (!applications.value[jobId]) {
        applications.value[jobId] = [];
      }

      const existing = applications.value[jobId].find(
        (entry) => (typeof entry === "string" ? entry : entry.userId) === userId
      );
      if (existing) return false;

      applications.value[jobId].push({
        userId,
        proposedRate: formData.proposedRate ?? "",
        rateType: formData.rateType ?? "hourly",
        availableDate: formData.availableDate ?? "",
        availableTime: formData.availableTime ?? "",
        coverNote: formData.coverNote ?? "",
        appliedAt: new Date().toISOString(),
      });

      saveApplications();
      return true;
    }

    function hasApplied(jobId, userId) {
      return (
        applications.value[jobId]?.some(
          (entry) => (typeof entry === "string" ? entry : entry.userId) === userId
        ) || false
      );
    }

    function getApplicationData(jobId, userId) {
      const entry = applications.value[jobId]?.find(
        (e) => (typeof e === "string" ? e : e.userId) === userId
      );
      return typeof entry === "object" ? entry : null;
    }

    function unapplyFromJob(jobId, userId) {
      if (!applications.value[jobId]) return;

      applications.value[jobId] = applications.value[jobId].filter(
        (entry) => (typeof entry === "string" ? entry : entry.userId) !== userId
      );

      if (applications.value[jobId].length === 0) {
        delete applications.value[jobId];
      }

      saveApplications();
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
      applications,
      applyToJob,
      hasApplied,
      getAppliedJobIds,
      loadApplications,
      initApplications,
      unapplyFromJob,
      getApplicationData,
    };
  },
  { persist: 
    {
      pick: ["edits", "applications"],
    },
 }
);