<script setup>
import { ref, onMounted } from "vue"
import { loadProviders, toggleFavoriteProvider } from "../services/api" // <-- new API

const providers = ref([])

async function fetchProviders() {
  try {
    const response = await loadProviders()
    providers.value = response.data
  } catch (error) {
    console.error("Failed to load providers", error)
  }
}

onMounted(fetchProviders)
</script>

<template>
  <div>
    <h1>Providers</h1>

    <div v-if="providers.length">

      <div
        v-for="provider in providers"
        :key="provider.id"
        style="border: 1px solid #ccc; margin-bottom: 20px; padding: 10px;"
      >

        <h2>{{ provider.name }}</h2>

        <img
          v-if="provider.avatar"
          :src="'http://localhost:8000' + provider.avatar"
          width="150"
        />

        <p>Email: {{ provider.email }}</p>
        <p>
          Location:
          {{ provider.city }}, {{ provider.state }},
          Lat {{ provider.latitude }}, Lng {{ provider.longitude }}
        </p>
        <p>Price per hour: {{ provider.price_per_hour }}</p>
        <p>About: {{ provider.about_me }}</p>

        <h3>Services</h3>
        <ul>
          <li v-for="service in provider.services" :key="service.id">
            {{ service.name }}
          </li>
        </ul>

        <h3>Work Images</h3>
        <div v-for="img in provider.work_images" :key="img.id">
          <img
            :src="'http://localhost:8000' + img.image"
            width="200"
          />
        </div>

        <div class="provider-actions">
          <button @click="toggleFavoriteProvider(provider.id)">
            Toggle favoriting provider
          </button>
        </div>

      </div>

    </div>

    <div v-else>
      Loading...
    </div>
  </div>
</template>