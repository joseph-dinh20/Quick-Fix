<template>
  <div v-if="loading">Loading...</div>

  <div v-else-if="provider">
    <!-- Provider Info -->
    <h1>{{ provider.name }}</h1>
    <img
      v-if="provider.avatar"
      :src="'http://localhost:8000' + provider.avatar"
      width="120"
    />
    <p>{{ provider.about_me }}</p>
    <p><strong>Price:</strong> ${{ provider.price_per_hour }}/hr</p>
    <p><strong>Location:</strong> {{ provider.city }}, {{ provider.state }}</p>

    <!-- Average Rating -->
    <h2>⭐ Average Rating: {{ provider.average_rating }}</h2>

    <!-- Reviews Section -->
    <h3>Reviews</h3>
    <div v-if="reviews.length">
      <div
        v-for="review in reviews"
        :key="review.id"
        style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;"
      >
        <p><strong>{{ review.reviewer_name }}</strong></p>
        <p>Rating: {{ review.rating }}/5</p>
        <p>{{ review.comment }}</p>
        <button @click="handleDelete(review.id)">Delete</button>
      </div>
    </div>
    <div v-else>No reviews yet.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { fetchReviews, loadProvider, deleteReview } from "../services/api"

const provider = ref(null)
const reviews = ref([])
const loading = ref(false)
const id = 2

async function fetchProvider() {
  try {
    const res = await loadProvider(id)
    provider.value = res.data  // <--- assign the provider
  } catch (err) {
    console.error(err)
  }
}

async function fetchProviderReviews() {
  try {
    const res = await fetchReviews(id)
    reviews.value = res.data
  } catch (err) {
    console.error(err)
  }
}

async function handleDelete(id) {
  await deleteReview(id)
  reviews.value = reviews.value.filter(r => r.id !== id)
}

onMounted(async () => {
  loading.value = true
  await Promise.all([fetchProvider(), fetchProviderReviews()])
  loading.value = false
})
</script>