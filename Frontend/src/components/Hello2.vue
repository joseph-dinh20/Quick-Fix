<script setup>
import { ref, onMounted } from "vue"
import { loadProvider } from "../services/api";

const provider = ref(null)

async function fetchProvider() {
  const response = await loadProvider(1);
  provider.value = response.data;
}

onMounted(fetchProvider)
</script>

<template>
  <div>
    <h1>Provider Test Page</h1>

    <div v-if="provider">

      <h2>{{ provider.name }}</h2>

      <img
        v-if="provider.avatar"
        :src="'http://localhost:8000' + provider.avatar"
        width="150"
      />

      <p>Email: {{ provider.email }}</p>
      <p>Location: {{ provider.city }}, {{ provider.state }}, Lat {{ provider.latitude }}, Lng {{ provider.longitude }}</p>
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

    </div>

    <div v-else>
      Loading...
    </div>
  </div>
</template>