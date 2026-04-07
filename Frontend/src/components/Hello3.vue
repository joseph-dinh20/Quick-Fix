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

import { ref, onMounted } from 'vue'
import {
  loadMyProvider,
  updateProfile,
  updateServiceProvider,
  getServices,
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

// provider services
const allServices = ref([])
const selectedServices = ref([])
const servicesMessage = ref('')
const loadingServices = ref(true)
const savingProfile = ref(false)

// --------- Load Provider Profile ---------
async function loadProfile() {
  try {
    const response = await loadMyProvider()
    const data = response.data

    name.value = data.name || ""
    avatarPreview.value = 'http://localhost:8000' + data.avatar || ""
    rates.value = data.price_per_hour || ""
    description.value = data.about_me || ""
    photoList.value = data.work_images || []
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

// --------- Work Images Upload Preview ---------
function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  photoFiles.value.push(file)
  photoList.value.push(URL.createObjectURL(file))
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
  photoFiles.value.forEach(file => providerForm.append("work_images", file))

  try {
    savingProfile.value = true
    servicesMessage.value = ''

    await updateProfile(form)
    await updateServiceProvider(providerForm)

    await loadProfile()
    servicesMessage.value = 'Profile saved successfully.'
  } catch (error) {
    console.error("Failed to save profile", error)
    servicesMessage.value = 'Failed to save profile and services.'
  } finally {
    savingProfile.value = false
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
  <CardTitle class="text-2xl flex justify-center">Profile Setup</CardTitle>

  <Card class="min-h-200 min-w-200">
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
          <CardTitle class="flex-col gap-10">
            Full Name
            <Input v-model="name" placeholder="Your name"/>
          </CardTitle>
        </div>
      </div>

      <div>
        <CardTitle class="flex-col gap-10">
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

      <Label class="mt-5 mb-1">Work Photos</Label>
      <div class="flex gap-2">
        <div v-for="img in photoList" :key="img.id">
        <img
          :src="'http://localhost:8000' + img.image"
          width="200"
        />
      </div>
      </div>

      <Label class="mt-5">Upload Work Photos</Label>
      <Input
        type="file"
        accept="image/png, image/jpeg"
        @change="handleFileChange"
        class="w-50 cursor-pointer"
      />

      <Label class="mt-5">Services</Label>
      <div v-if="loadingServices" class="text-sm text-gray-500">Loading services...</div>
      <div v-else class="flex flex-col gap-3">
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

        <details class="border rounded-md p-3">
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