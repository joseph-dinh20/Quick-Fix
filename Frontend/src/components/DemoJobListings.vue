<!-- THIS PAGE LISTS ALL JOB POSTINGS (viewable for users not signed in) AND ALSO ALLOWS TOGGLING FAVORITING JOBS (if service provider) -->
<template>
  <div class="jobs-container">
    <h2>All Jobs</h2>

    <div v-if="loading">Loading...</div>

    <div v-else>
      <div
        v-for="job in jobs"
        :key="job.id"
        class="job-card"
      >
        <div class="job-info">
          <h3>{{ job.title }}</h3>
          <p>{{ job.description }}</p>
        </div>

        <div class="job-actions">
          <button @click="toggle(job)">
            {{ job.is_favorited ? "Unfavorite" : "Favorite" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAllJobs, toggleFavorite } from "@/services/api";

export default {
  name: "JobsList",

  data() {
    return {
      jobs: [],
      loading: false,
    };
  },

  async mounted() {
    this.fetchJobs();
  },

  methods: {
    async fetchJobs() {
      this.loading = true;
      try {
        const res = await getAllJobs();
        this.jobs = res.data.results || res.data; // handles pagination or not
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async toggle(job) {
      try {
        const res = await toggleFavorite(job.id);
        job.is_favorited = res.data.favorited;
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.jobs-container {
  max-width: 800px;
  margin: auto;
}

.job-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 10px;
}

.job-info {
  max-width: 70%;
}

.job-actions button {
  padding: 6px 12px;
  cursor: pointer;
}
</style>