<!-- Profile.vue — thin dispatch wrapper -->
<script setup>
import { useUserStore } from "@/store/userStore";
import { storeToRefs } from "pinia";
import CustomerProfile from "@/components/CustomerProfile.vue";
import ProviderProfile from "@/components/ProviderProfile.vue";

const userStore = useUserStore();
const { isLoggedIn, isCustomer, isProvider } = storeToRefs(userStore);
</script>

<template>
  <div>
    <CustomerProfile v-if="isLoggedIn && isCustomer" />
    <ProviderProfile v-else-if="isLoggedIn && isProvider" />
    <div v-else class="text-muted-foreground m-10 text-center">
      Please log in to view your profile.
    </div>
  </div>
</template>
