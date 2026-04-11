<template>
  <div>
    <h2>Assigned Jobs</h2>

    <div v-if="loading">Loading...</div>

    <div v-else>
      <div v-if="jobs.length === 0">
        No assigned jobs
      </div>

      <div
        v-for="job in jobs"
        :key="job.id"
        style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;"
      >
        <div><strong>{{ job.title }}</strong></div>
        <div>Status: {{ job.status }}</div>

        <button
          v-if="job.status === 'in_progress'"
          @click="handleComplete(job.id)"
        >
          Mark as Complete
        </button>

        <div v-else>
          Completed
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchAssignedJobs, completeJob } from "../services/api"

export default {
  data() {
    return {
      jobs: [],
      loading: false
    }
  },

  async mounted() {
    await this.loadJobs()
  },

  methods: {
    async loadJobs() {
      this.loading = true
      try {
        const res = await fetchAssignedJobs()
        this.jobs = res.data
      } finally {
        this.loading = false
      }
    },

    async handleComplete(id) {
      await completeJob(id)
      await this.loadJobs()
    }
  }
}
</script>