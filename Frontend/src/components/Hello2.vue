<script setup>
import { ref, onMounted } from "vue"

const provider = ref(null)

async function loadProvider() {
  const response = await fetch("http://localhost:8000/api/accounts/providers/1/")
  const data = await response.json()

  provider.value = data
}

onMounted(loadProvider)
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