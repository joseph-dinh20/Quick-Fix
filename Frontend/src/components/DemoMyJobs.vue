<script setup>
import { ref, onMounted } from "vue"
import { getMyJobs } from "../services/api"

const jobs = ref([])

async function fetchJobs() {
  try {
    const res = await getMyJobs()
    jobs.value = res.data
  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchJobs)
</script>

<template>
  <div>
    <h1>My Jobs</h1>

    <div v-if="jobs.length">
      <div v-for="job in jobs" :key="job.id" style="margin-bottom: 20px;">
        <h2>{{ job.title }}</h2>
        <p>{{ job.description }}</p>
        <p>Budget: {{ job.budget }}</p>
        <p>Deadline: {{ job.deadline }}</p>

        <p>Services:</p>
        <ul>
          <li v-for="s in job.services" :key="s.id">
            {{ s.name }}
          </li>
        </ul>

        <div>
          <img
            v-for="img in job.images"
            :key="img.id"
            :src="'http://localhost:8000' + img.image"
            width="150"
          />
        </div>
      </div>
    </div>

    <div v-else>
      No jobs yet.
    </div>
  </div>
</template>