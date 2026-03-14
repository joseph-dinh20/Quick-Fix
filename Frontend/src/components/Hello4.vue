<script setup>
import { ref, onMounted } from "vue"
import { updateServiceProvider, loadMyProvider, deleteWorkImage, me } from "@/services/api"

const aboutMe = ref("")
const price = ref("")

const services = ref([])

const existingImages = ref([])
const newImages = ref([])

const availableServices = [
  { id: 1, name: "Plumbing" },
  { id: 2, name: "Electrical" },
  { id: 3, name: "Cleaning" }
]

// --------- Load Provider Profile ---------
async function loadProfile() {
  try {
    const response = await loadMyProvider();
    const data = response.data;
    console.log(data);
    aboutMe.value = data.about_me || "";
    price.value = data.price_per_hour || "";
    services.value = data.services || [];

    existingImages.value = data.work_images;

  } catch (error) {
    console.error("Failed to load profile", error);
  }
}

function toggleService(serviceId) {
  if (services.value.includes(serviceId)) {
    services.value = services.value.filter(s => s !== serviceId);
  } else {
    services.value.push(serviceId);
  }
}

function handleImageUpload(event) {
  const files = event.target.files;

  for (let i = 0; i < files.length; i++) {
    newImages.value.push(files[i]);
  }
}

function removeNewImage(index) {
  newImages.value.splice(index, 1);
}


// --------- Submit Update ---------
async function submitProviderUpdate() {

  const formData = new FormData();

  if (aboutMe.value !== "") {
    formData.append("about_me", aboutMe.value);
  }

  if (price.value !== "") {
    formData.append("price_per_hour", price.value);
  }

services.value.forEach(service => {
  const id = typeof service === "object" ? service.id : service
  formData.append("services", id)
})

  newImages.value.forEach(file => {
    formData.append("work_images", file);
  })

  try {
    await updateServiceProvider(formData);
    alert("Provider profile updated");
  } catch (error) {
    console.error(error);
    alert("Update failed");
  }
}


// ------------------- Delete images ------------------- //
async function removeExistingImage(id, index) {

  try {
    await deleteWorkImage(id);

    existingImages.value.splice(index, 1);

  } catch (error) {
    console.error("Failed to delete image", error);
  }
}

onMounted(loadProfile);
</script>

<template>

<div>

<h2>Update Service Provider</h2>

<div>
<label>About Me</label>
<textarea v-model="aboutMe"></textarea>
</div>

<div>
<label>Price Per Hour</label>
<input v-model="price" type="number" step="0.01" />
</div>

<div>
<label>Services Offered</label>

<div v-for="service in availableServices" :key="service.id">
<input
type="checkbox"
:checked="services.includes(service.id)"
@click="toggleService(service.id)"
>
{{ service.name }}
</div>

</div>

<div>
<label>Existing Work Images</label>

<div v-for="(img, index) in existingImages" :key="img.id">

<img :src="'http://localhost:8000' + img.image" width="120">

<button @click="removeExistingImage(img.id, index)">
Delete
</button>

</div>

</div>

<div>
<label>Upload New Images</label>

<input type="file" multiple @change="handleImageUpload">

<div v-for="(img, index) in newImages" :key="index">

{{ img.name }}

<button @click="removeNewImage(index)">
Remove
</button>

</div>

</div>

<button @click="submitProviderUpdate">
Update Provider
</button>

</div>

</template>