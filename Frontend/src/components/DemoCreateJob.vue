<script setup>
import { ref } from "vue"
import { createJob } from "../services/api"

const title = ref("")
const description = ref("")
const budget = ref("")
const deadline = ref("")
const requestType = ref("quote")
const services = ref([])   // array of IDs
const images = ref([])

const message = ref("")

function handleImageUpload(e) {
  images.value = Array.from(e.target.files)
}

async function submitJob() {
  try {
    await createJob({
      title: title.value,
      description: description.value,
      budget: budget.value,
      deadline: deadline.value,
      request_type: requestType.value,
      services: services.value,
      images: images.value
    })

    message.value = "Job created successfully"

    // reset form
    title.value = ""
    description.value = ""
    budget.value = ""
    deadline.value = ""
    requestType.value = "quote"
    services.value = []
    images.value = []

  } catch (err) {
    console.error(err)
    message.value = "Error creating job"
  }
}
</script>

<template>
  <div>
    <h1>Create Job</h1>

    <p v-if="message">{{ message }}</p>

    <form @submit.prevent="submitJob">

      <div>
        <label>Title</label><br />
        <input v-model="title" required />
      </div>

      <div>
        <label>Description</label><br />
        <textarea v-model="description" required />
      </div>

      <div>
        <label>Budget</label><br />
        <input type="number" v-model="budget" />
      </div>

      <div>
        <label>Deadline</label><br />
        <input type="datetime-local" v-model="deadline" required />
      </div>

      <div>
        <label>Request Type</label><br />
        <select v-model="requestType">
          <option value="quote">Quote</option>
          <option value="service">Service</option>
          <option value="both">Both</option>
        </select>
      </div>

      <div>
        <label>Services (IDs for now)</label><br />
        <input
          placeholder="e.g. 1,2"
          @change="e => services = e.target.value.split(',').map(Number)"
        />
      </div>

      <div>
        <label>Images</label><br />
        <input type="file" multiple @change="handleImageUpload" />
      </div>

      <button type="submit">Create Job</button>

    </form>
  </div>
</template>