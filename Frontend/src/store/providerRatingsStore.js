// store/providerRatingsStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import providersData from "@/store/data/providers.json";

export const useProviderRatingsStore = defineStore(
  "providerRatings",
  () => {
    // User-submitted ratings, keyed by provider userID.
    // Shape per entry: array of { jobType, userName, date, userAvatar, userRated, userComment }
    const userRatings = ref({});

    function addRating(providerId, rating) {
      const existing = userRatings.value[providerId] || [];
      userRatings.value = {
        ...userRatings.value,
        [providerId]: [rating, ...existing],
      };
    }

    // Returns the merged rating list for a given provider:
    // user-submitted ratings first (most recent), then the seed ratings from providers.json
    function getRatingsFor(providerId) {
      const seed = providersData.find((p) => p.userID === providerId);
      const seedRatings = seed?.ratings || [];
      const fromUsers = userRatings.value[providerId] || [];
      return [...fromUsers, ...seedRatings];
    }

    // Computed merged average rating.
    function getAverageFor(providerId) {
      const all = getRatingsFor(providerId);
      if (!all.length) return null;
      const sum = all.reduce((acc, r) => acc + (r.userRated || 0), 0);
      return (sum / all.length).toFixed(1);
    }

    return { userRatings, addRating, getRatingsFor, getAverageFor };
  },
  {
    persist: true,
  },
);
