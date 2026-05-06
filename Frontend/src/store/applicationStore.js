// store/applicationStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useApplicationStore = defineStore("applications", () => {
  const applications = ref([]); 
  // [{ jobId, providerId }]

  function apply(jobId, providerId) {
    const alreadyApplied = applications.value.find(
      (a) => a.jobId === jobId && a.providerId === providerId
    );

    if (alreadyApplied) return false;

    applications.value.push({ jobId, providerId });
    return true;
  }

  function hasApplied(jobId, providerId) {
    return applications.value.some(
      (a) => a.jobId === jobId && a.providerId === providerId
    );
  }

  return {
    applications,
    apply,
    hasApplied,
  };
}, {
  persist: true,
});