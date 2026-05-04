// store/providerProfileStore.js
import { defineStore } from "pinia";
import { ref } from "vue";
import providersData from "@/store/data/providers.json";

export const useProviderProfileStore = defineStore(
  "providerProfile",
  () => {
    // User-edited provider data, keyed by providerId.
    // Shape: { [providerId]: { name, avatar, price, aboutMe, workPhotos } }
    const edits = ref({});

    function saveProfile(providerId, updates) {
      const existing = edits.value[providerId] || {};
      edits.value = {
        ...edits.value,
        [providerId]: { ...existing, ...updates },
      };
    }

    // Returns merged provider data (seed + edits applied on top).
    function getMergedProvider(providerId) {
      const seed = providersData.find((p) => p.userID === providerId);
      if (!seed) return null;
      const edit = edits.value[providerId] || {};
      return {
        ...seed,
        ...(edit.name !== undefined ? { name: edit.name } : {}),
        ...(edit.avatar ? { avatar: edit.avatar } : {}),
        ...(edit.price !== undefined ? { price: edit.price } : {}),
        ...(edit.aboutMe !== undefined ? { aboutMe: edit.aboutMe } : {}),
        ...(edit.workPhotos !== undefined
          ? { workPhotos: edit.workPhotos }
          : {}),
      };
    }

    // Returns the full provider list with all edits applied.
    function getMergedProviders() {
      return providersData.map((p) => getMergedProvider(p.userID));
    }

    return { edits, saveProfile, getMergedProvider, getMergedProviders };
  },
  {
    persist: true,
  },
);
