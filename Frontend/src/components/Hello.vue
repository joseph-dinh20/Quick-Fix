<template>
  <div class="min-h-screen flex flex-col items-center justify-center gap-6 p-6">
    <h1 class="text-4xl font-bold text-green-800">Welcome!</h1>
    
    <!-- Display message from backend -->
    <h2 class="text-xl text-blue-600 text-center">
      INTERCEPTED: {{ backendMessage }}
    </h2>

    <!-- Optional: Retry button if fetch fails -->
    <button
      v-if="backendMessage.includes('Could not')"
      @click="fetchMessage"
      class="px-4 py-2 bg-green-500 text-white rounded"
    >
      Retry
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Hello } from '@/services/api'  // Import the Django API function

// Reactive variable to store backend message
const backendMessage = ref('Loading...')

// Function to fetch message from Django
async function fetchMessage() {
  try {
    const res = await Hello()
    backendMessage.value = res.data.message
  } catch (err) {
    console.error('Failed to fetch backend message:', err)
    backendMessage.value = 'Could not fetch message'
  }
}

// Fetch message once when component mounts
onMounted(fetchMessage)
</script>

<style scoped>
/* Optional styling */
</style>
