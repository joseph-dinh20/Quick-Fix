<script setup>
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { AspectRatio } from '@/components/ui/aspect-ratio'
import { Label } from '@/components/ui/label'

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

import { ref } from 'vue'

//NOTE: Single Value Variables
const avatar = ref('')
const name = "Satoru Goji"
const rates = ref('')

//NOTE: This is for image upload, image display
const photoList = ref([])
const selectedImage = ref()

function handleFileChange(event) {
  const file = event.target.files[0] //use this for backend at some point
  if (!file) return
  selectedImage.value = file
  console.log("file = " + file)
  handleFileSubmit()
}

function handleFileSubmit() {
  if (!selectedImage.value) return
  //WARN: URL.createObjectURL creates a fake URL that points to a file/blob
  //so that it can be displayed on the browser with <img src="someBlobs...">
  //since HTML elements expect URLs and not file objects.
  const fileUrl = URL.createObjectURL(selectedImage.value)
  photoList.value.push(fileUrl)
  console.log("fileUrl = " + fileUrl)
  selectedImage.value = null
  forceReRender()
}

//NOTE: Temporary copy pasta for avatar upload and display
function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  selectedImage.value = file
  console.log(file)
  handleAvatarSubmit()
}

function handleAvatarSubmit() {
  if (!selectedImage.value) return
  const fileUrl = URL.createObjectURL(selectedImage.value)
  avatar.value = fileUrl
  console.log(avatar.value)
  selectedImage.value = null
}

//NOTE: Force Re-Render Section
// every time forceReRender is called, this updates
// the component value (componentKey) by 1.
// Making vue to aware an update the component is needed because a value has @change
const componentKey = ref(0)
const forceReRender = () => { componentKey.value++ }

</script>

<template>
  <div class="justify-items-center">
    <p class="text-3xl">Profile Setup</p>
    <Card class="min-h-200 min-w-200">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-[30px]">
          <Label for="avatar" class="cursor-pointer">
            <Input id="avatar" type="file" accept="image/png, image/jpeg" @change="handleAvatarUpload" class="hidden" />
            <Avatar class="scale-[2]">
              <AvatarImage :src="avatar" alt="@shadcn" />
              <AvatarFallback>Avatar</AvatarFallback>
            </Avatar>
          </Label>
          <div class="self-center">
            <CardTitle>{{ name }}</CardTitle>
            <!-- <CardDescription>Star Ratings: 5.0 (999 total ratings)</CardDescription> -->
          </div>
        </div>
        <div>
          <CardTitle>
            Rates
            <Input placeholder="$00.00/hr">
            </Input>
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <p>Profile Description</p>
        <Textarea id="description" class="min-h-50 min-w-full text-pretty"
          placeholder="Write short but detailed description on how you can help the customers.">
        </Textarea>

        <Label for="workPhotos" class="mt-5 mb-1">Work Photos</Label>
        <!-- <div id="workPhotos"> -->
        <div v-if="photoList.length < 5">
          <p> photolength is {{ photoList.length }}</p>
          <div class="flex">
            <div v-for="item in photoList" class="w-35">
              <Popover>
                <PopoverTrigger class="w-full h-full">
                  <AspectRatio :ratio="1 / 1">
                    <Input type="image" :key="componentKey" :src="item"
                      class="inline-block border-0 object-cover w-full h-full rounded-lg" />
                  </AspectRatio>
                  <PopoverContent class="w-150 border-0">
                    <AspectRatio :ratio="3 / 2">
                      <img :src="item" class="w-full h-full rounded-lg" />
                    </AspectRatio>
                  </PopoverContent>
                </PopoverTrigger>
              </Popover>
            </div>
          </div>
        </div>
        <div v-else>
          display something else here
        </div>
        <!-- </div> -->

        <Label for="picture" class="mt-5">Photo Upload</Label>
        <Input id="picture" :key="componentKey" type="file" accept="image/png, image/jpeg" @change="handleFileChange"
          class="w-50 cursor-pointer" />
      </CardContent>
      <CardFooter>

        <Button>Save Profile</Button>
      </CardFooter>
    </Card>
  </div>
</template>
