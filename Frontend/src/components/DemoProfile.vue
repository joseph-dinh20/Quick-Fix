<script setup>
import {
  Card, CardContent, CardFooter, CardHeader, CardTitle
} from '@/components/ui/card'

import {
  Avatar, AvatarFallback, AvatarImage
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { AspectRatio } from '@/components/ui/aspect-ratio'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'

import { ref, onMounted, computed } from 'vue'
import {
  loadMyProvider,
  updateProfile,
  updateServiceProvider,
  getServices,
  deleteWorkImage
} from '@/services/api'

// --------- Reactive State ---------
const name = ref("")
const rates = ref("")
const description = ref("")

// avatar
const avatarPreview = ref("")
const avatarFile = ref(null)

// work images
const photoList = ref([])
const photoFiles = ref([])
const maxImagesPerRow = ref(4)

// provider services
const allServices = ref([])
const selectedServices = ref([])
const servicesMessage = ref('')
const loadingServices = ref(true)
const savingProfile = ref(false)

const existingImages = ref([])
const newImages = ref([])

// --------- Load Provider Profile ---------
async function loadProfile() {
  try {
    const response = await loadMyProvider()
    const data = response.data

    name.value = data.name || ""
    avatarPreview.value = 'http://localhost:8000' + data.avatar || ""
    rates.value = data.price_per_hour || ""
    description.value = data.about_me || ""
    existingImages.value = data.work_images || []
    selectedServices.value = (data.services || []).map(service => service.id)
  } catch (error) {
    console.error("Failed to load profile", error)
  }
}

async function fetchServiceData() {
  try {
    loadingServices.value = true
    servicesMessage.value = ''
    const response = await getServices()
    allServices.value = response.data
  } catch (error) {
    console.error('Failed to load services', error)
    servicesMessage.value = 'Could not load available services.'
  } finally {
    loadingServices.value = false
  }
}

function toggleService(serviceId) {
  if (selectedServices.value.includes(serviceId)) {
    selectedServices.value = selectedServices.value.filter(id => id !== serviceId)
  } else {
    selectedServices.value = [...selectedServices.value, serviceId]
  }
}

// --------- Avatar Upload Preview ---------
function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  avatarFile.value = file
  avatarPreview.value = URL.createObjectURL(file)
}

// --------- Work Images Management  ---------
function handleImageUpload(event) {
  const files = Array.from(event.target.files)

  files.forEach(file => {
    if (!newImages.value.some(f => f.file.name === file.name)) {
      newImages.value.push({
        file,
        preview: URL.createObjectURL(file)
      })
    }
  })

  event.target.value = ""
}


function removeNewImage(index) {
  URL.revokeObjectURL(newImages.value[index].preview)
  newImages.value.splice(index, 1)
}


async function removeExistingImage(id, index) {
  try {
    await deleteWorkImage(id)
    existingImages.value.splice(index, 1)
  } catch (error) {
    console.error("Failed to delete image", error)
  }
}

// --------- Save Profile to Backend ---------
async function saveProfile() {
  const form = new FormData()
  form.append("name", name.value)
  if (avatarFile.value) form.append("avatar", avatarFile.value)

  const providerForm = new FormData()
  providerForm.append("about_me", description.value)
  providerForm.append("price_per_hour", rates.value)
  selectedServices.value.forEach(id => providerForm.append("services", id))

  // <-- append images here instead of `form`
  newImages.value.forEach(img => {
    providerForm.append("work_images", img.file)
  })

  try {
    savingProfile.value = true
    servicesMessage.value = ''

    await updateProfile(form)
    await updateServiceProvider(providerForm) // now includes images

    servicesMessage.value = 'Profile saved successfully.'

    // clean up previews
    newImages.value.forEach(img => URL.revokeObjectURL(img.preview))
    newImages.value = []

    // reload profile to show new images
    await loadProfile()

  } catch (error) {
    console.error("Failed to save profile", error)
    servicesMessage.value = 'Failed to save profile and services.'
  } finally {
    savingProfile.value = false
  }
}

// Combine existing and new images for display
const combinedImages = computed(() => {
  const existing = existingImages.value.map((img) => ({
    src: 'http://localhost:8000' + img.image,
    type: 'existing',
    id: img.id,
    key: 'existing-' + img.id
  }))

  const newly = newImages.value.map((img, index) => ({
    src: img.preview,
    type: 'new',
    index,
    key: 'new-' + index
  }))

  return [...existing, ...newly]
})

// Remove image (handles both existing and new)
function removeImage(img) {
  if (img.type === 'existing') {
    removeExistingImage(img.id, existingImages.value.findIndex(e => e.id === img.id))
  } else if (img.type === 'new') {
    removeNewImage(img.index)
  }
}

// --------- Load on mount ---------
onMounted(() => {
  loadProfile()
  fetchServiceData()
})
</script>

<template>
<div class="justify-items-center flex flex-col items-center m-10">
  <CardTitle class="text-2xl flex justify-center py-5">Profile Setup</CardTitle>

  <Card class="min-h-200 min-w-200 max-w-3xl w-full space-y-6">
    <CardHeader class="justify-between flex-row">
      <div class="flex flex-row gap-[30px]">
        <Label for="avatar" class="cursor-pointer">
          <Input
            id="avatar"
            type="file"
            accept="image/png, image/jpeg"
            @change="handleAvatarUpload"
            class="hidden"
          />
          <Avatar class="scale-[2]">
            <AvatarImage :src="avatarPreview" />
            <AvatarFallback>Avatar</AvatarFallback>
          </Avatar>
        </Label>

        <div class="self-center">
          <CardTitle class="flex-col gap-10 py-3">
            Full Name
            <Input v-model="name" placeholder="Your name"/>
          </CardTitle>
        </div>
      </div>

      <div>
        <CardTitle class="flex-col gap-10 py-3">
          Price per Hour
          <Input v-model="rates" placeholder="$00.00/hr"/>
        </CardTitle>
      </div>
    </CardHeader>

    <CardContent>
      <p>Profile Description</p>
      <Textarea
        v-model="description"
        class="min-h-50 min-w-full"
        placeholder="Write a description about your services."
      />

      <Label class="mt-5 py-3">Work Photos</Label>
        <div
          class="grid gap-4"
          :class="{
            'grid-cols-2': maxImagesPerRow === 2,
            'grid-cols-3': maxImagesPerRow === 3,
            'grid-cols-4': maxImagesPerRow === 4
          }"
        >
          <div
            v-for="img in combinedImages"
            :key="img.key"
            class="relative w-full group"
          >
            <AspectRatio :ratio="1">
              <img :src="img.src" class="object-cover w-full h-full rounded-lg p-0.5" />
            </AspectRatio>
            <Button
              size="icon"
              variant="destructive"
              class="absolute top-1 right-1 opacity-0 group-hover:opacity-100"
              @click="removeImage(img)"
            >
              ✕
            </Button>
          </div>

          <!-- Upload Box -->
          <AspectRatio :ratio="1">
            <label
              class="flex items-center justify-center border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50 w-full h-full"
            >
              <span class="text-sm text-gray-500">+ Upload</span>
              <input type="file" multiple class="hidden" @change="handleImageUpload" />
            </label>
          </AspectRatio>
        </div>
      <!-- <Input
        type="file"
        accept="image/png, image/jpeg"
        @change="handleFileChange"
        class="w-50 cursor-pointer"
      />

      <Label class="mt-5">Services</Label> -->
      <div v-if="loadingServices" class="text-sm text-gray-500">Loading services...</div>
      <div v-else class="flex flex-col gap-3 py-2">
        <div class="flex flex-wrap gap-2">
          <Badge
            v-for="service in allServices.filter(service => selectedServices.includes(service.id))"
            :key="service.id"
            variant="secondary"
          >
            {{ service.name }}
          </Badge>

          <span
            v-if="allServices.filter(service => selectedServices.includes(service.id)).length === 0"
            class="text-sm text-gray-500"
          >
            No services selected yet.
          </span>
        </div>

        <details class="border rounded-md p-3 w-full max-w-full overflow-hidden">
          <summary class="cursor-pointer font-medium">Edit Services</summary>
          <div class="flex flex-wrap gap-3 mt-4">
            <label
              v-for="service in allServices"
              :key="service.id"
              class="flex items-center gap-2 border rounded-md px-3 py-2 cursor-pointer"
            >
              <input
                type="checkbox"
                :checked="selectedServices.includes(service.id)"
                @change="toggleService(service.id)"
              />
              <span>{{ service.name }}</span>
            </label>
          </div>
        </details>
      </div>
    </CardContent>

    <CardFooter>
      <div class="flex flex-col gap-2 w-full">
        <Button @click="saveProfile" :disabled="savingProfile">
          {{ savingProfile ? 'Saving...' : 'Save Profile' }}
        </Button>
        <span v-if="servicesMessage" class="text-sm text-gray-500">
          {{ servicesMessage }}
        </span>
      </div>
    </CardFooter>
  </Card>
</div>
</template>