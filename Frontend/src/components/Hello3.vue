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
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

import { ref, onMounted } from 'vue'
import { loadProvider, updateProfile } from '@/services/api'

// --------- Reactive State ---------
const userId = 1 // replace with dynamic user ID from store/route
const name = ref("")
const rates = ref("")
const description = ref("")

// avatar
const avatarPreview = ref("")
const avatarFile = ref(null)

// work images
const photoList = ref([])
const photoFiles = ref([])

// --------- Load Provider Profile ---------
async function loadProfile() {
  try {
    const response = await loadProvider(userId)
    const data = response.data

    name.value = data.name || ""
    avatarPreview.value = data.avatar || ""
    rates.value = data.price_per_hour || ""
    description.value = data.about_me || ""

    photoList.value = response.work_images;

  } catch (error) {
    console.error("Failed to load profile", error)
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
  form.append("price_per_hour", rates.value)
  form.append("about_me", description.value)

  if (avatarFile.value) form.append("avatar", avatarFile.value)
  photoFiles.value.forEach(file => form.append("work_images", file))

  try {
    await updateProfile(form)
    alert("Profile saved!")
  } catch (error) {
    console.error("Failed to save profile", error)
  }
}

// --------- Load on mount ---------
onMounted(() => {
  loadProfile()
})
</script>

<template>
<div class="justify-items-center">
  <p class="text-3xl mb-4">Profile Setup</p>

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
          <CardTitle>
            <Input v-model="name" placeholder="Your name"/>
          </CardTitle>
        </div>
      </div>

      <div>
        <CardTitle>
          Rates
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
    </CardContent>

    <CardFooter>
      <Button @click="saveProfile">Save Profile</Button>
    </CardFooter>
  </Card>
</div>
</template>