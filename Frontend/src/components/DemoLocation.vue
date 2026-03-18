<script setup>
import { ref, onMounted } from "vue"
import { updateProfile, me } from "@/services/api"

const city = ref("")
const state = ref("")

const lat = ref("")
const lng = ref("")

const currentCity = ref("")
const currentState = ref("")

const message = ref("")

// Load current profile
async function loadProfile() {
  try {
    const res = await me()
    const data = res.data

    currentCity.value = data.city || "Not set"
    currentState.value = data.state || "Not set"
    lat.value = data.latitude || "Not set"
    lng.value = data.longitude || "Not set"
  } catch (err) {
    console.error("Failed to load profile", err)
  }
}

async function submitLocation() {
  try {
    await updateProfile({
      city: city.value || currentCity.value,
      state: state.value || currentState.value
    })

    message.value = "Location updated successfully"

    // refresh displayed values
    await loadProfile()

    // clear inputs
    city.value = ""
    state.value = ""

  } catch (error) {
    console.error(error)
    message.value = error.response?.data
      ? JSON.stringify(error.response.data)
      : "Update failed"
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<template>
<div>
  <h2>Location Settings</h2>

  <!-- Current values -->
  <div>
    <p><strong>Current City:</strong> {{ currentCity }}</p>
    <p><strong>Current State:</strong> {{ currentState }}</p>
    <p><strong>Current Coords:</strong>Lat {{ lat }}, Lng {{ lng }}</p>
  </div>

  <hr />

  <!-- Update form -->
  <div>
    <label>City</label>
    <input v-model="city" placeholder="Enter city" />
  </div>

  <div>
    <label>State</label>
    <input v-model="state" placeholder="Enter state" />
  </div>

  <button @click="submitLocation">
    Save Location
  </button>

  <p>{{ message }}</p>
</div>
</template>