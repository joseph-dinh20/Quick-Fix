// store/jobStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import jobsData from "@/store/data/jobs.json";



export const useJobStore = defineStore(
  "job",
  () => {
    const jobList = ref(jobsData);

    // User-created or edited jobs, keyed by job_id.
    // Shape: { [jobId]: { ...jobData } }
    const edits = ref({});

    // Add or update a job
    function saveJob(jobId, updates) {
      const existing = edits.value[jobId] || {};
      edits.value = {
        ...edits.value,
        [jobId]: { ...existing, ...updates },
      };
    }

    // Get a merged job (seed + edits applied on top)
    function getMergedJob(jobId) {
      const seed = jobsData.find((j) => j.job_id === jobId);
      if (!seed) return null;
      const edit = edits.value[jobId] || {};
      return {
        ...seed,
        ...edit,
      };
    }

    // Get all merged jobs
    function getMergedJobs() {
      return jobsData.map((j) => getMergedJob(j.job_id));
    }

    // Get jobs by user_id
    function getJobsByUser(userId) {
      return getMergedJobs().filter((job) => job.user_id === userId);
    }

    // Get jobs by provider_id
    function getJobsByProvider(providerId) {
      return getMergedJobs().filter((job) => job.provider_id === providerId);
    }

    // Get jobs by service type
    function getJobsByService(service) {
      return getMergedJobs().filter((job) => job.service === service);
    }

    // Get jobs by urgency
    function getJobsByUrgency(urgency) {
      return getMergedJobs().filter((job) => job.urgency === urgency);
    }

    return {
      jobList,
      edits,
      saveJob,
      getMergedJob,
      getMergedJobs,
      getJobsByUser,
      getJobsByProvider,
      getJobsByService,
      getJobsByUrgency,
    };
  },
  {
    persist: true,
  },
);