<script setup>
import { ref, onMounted } from "vue"
import { loadProvider } from "../services/api"

const provider = ref(null)
const error = ref("")
const loading = ref(true)

async function fetchProvider() {
  try {
    loading.value = true
    error.value = ""

    const response = await loadProvider(4)
    console.log("Provider response:", response.data)
    provider.value = response.data
  } catch (err) {
    console.error("Error loading provider:", err)
    error.value = "Failed to load provider."
  } finally {
    loading.value = false
  }
}

onMounted(fetchProvider)
</script>

<template>
  <div style="padding: 20px">
    <h1>Provider Test Page</h1>

    <p v-if="loading">Loading...</p>
    <p v-else-if="error">{{ error }}</p>

    <div v-else-if="provider">
      <h2>{{ provider.name || "No name" }}</h2>

      <img
        v-if="provider.avatar"
        :src="'http://localhost:8000' + provider.avatar"
        width="150"
      />

      <p>Email: {{ provider.email || "No email in serializer" }}</p>
      <p>Price per hour: {{ provider.price_per_hour || "No rate" }}</p>
      <p>About: {{ provider.about_me || "No bio" }}</p>
      <p>Average rating: {{ provider.average_rating || "No rating" }}</p>
      <p>Total rating: {{ provider.total_rating || "No total" }}</p>

      <h3>Services</h3>
      <ul v-if="provider.services && provider.services.length">
        <li v-for="service in provider.services" :key="service.id">
          {{ service.name }}
        </li>
      </ul>
      <p v-else>No services found.</p>

      <h3>Work Images</h3>
      <div v-if="provider.work_images && provider.work_images.length">
        <img
            v-for="image in provider.work_images"
            :key="image.id"
            :src="'http://localhost:8000' + image.image"
            width="150"
            style="margin-right: 10px"
        />
      </div>
      <p v-else>No work images found.</p>

      <h3>Raw Provider Data</h3>
      <pre>{{ provider }}</pre>
    </div>
  </div>
</template>