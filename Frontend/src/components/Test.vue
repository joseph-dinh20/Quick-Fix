<script setup>
import { ref, reactive, computed, useTemplateRef, nextTick } from 'vue'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'

// This is for image upload, image display
const photoList = ref([])
const selectedImage = ref()
const renderComponent = ref(true)

function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  selectedImage.value = file
}

function handleFileSubmit() {
  if (!selectedImage.value) return
  const fileUrl = URL.createObjectURL(selectedImage.value)
  photoList.value.push(fileUrl)
  selectedImage.value = null
}

const forceReRender = async () => {
  renderComponent.value = false
  await nextTick()
  renderComponent.value = true
}

</script>

<template>
  <div class="flex flex-col gap-10">
    <Input v-if="renderComponent" type="file" accept="image/png, image/jpeg" @change="handleFileChange" />

    <Button v-if="selectedImage" @click="handleFileSubmit(), forceReRender()">
      Submit
    </Button>

    <div v-for="item in photoList">
      <img :src="item" class="w-12 h-12 object-cover" />
    </div>

  </div>

</template>
