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

import { ref, nextTick } from 'vue'
// temp image placeholders
const photo = ref('https://thumbs.dreamstime.com/b/man-lawn-mower-cutting-grass-garden-summer-works-care-169327253.jpg')
const avatar = ref('https://media.tenor.com/hHO9MW5-yw8AAAAM/jjk-jujutsu-kaisen.gif')

// will need to grab info from the backend at some point
const name = "Satoru Goji"

// This is for image upload, image display
const photoList = ref([])
const selectedImage = ref()
const renderComponent = ref(true)

function handleFileChange(event) {
  const file = event.target.files[0] //use this for backend at some point
  if (!file) return
  selectedImage.value = file
  handleFileSubmit()
}

function handleFileSubmit() {
  if (!selectedImage.value) return
  const fileUrl = URL.createObjectURL(selectedImage.value)
  photoList.value.push(fileUrl)
  selectedImage.value = null
  forceReRender()
}

// const forceReRender = async () => {
//   renderComponent.value = false
//   await nextTick()
//   renderComponent.value = true
// }
// END OF image upload, image diplay

// another way to force an component to re-render
// every time forceReRender is called, this updates
// the component value by 1. Making vue "know" to
// update the component

const componentKey = ref(0)
const forceReRender = () => { componentKey.value += 1 }

</script>

<template>
  <div class="justify-items-center">
    <p class="text-3xl">Profile Setup for {Skill} </p>
    <Card class="min-h-200 min-w-200">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-[30px]">
          <Avatar class="scale-[1.8]">
            <AvatarImage :src="avatar" alt="@shadcn" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>Name</CardTitle>
            <Input id="name" readonly type="text" :placeholder="name"></Input>
            <CardDescription>Star Ratings: 5.0 (999 total ratings)</CardDescription>
          </div>
        </div>
        <div>
          <CardTitle>Rates<Input placeholder="$00.00/hr"></Input></CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <p>Profile Description</p>
        <Textarea id="description" class="min-h-50 min-w-full text-pretty"
          placeholder="Write short but detailed description on how you can help the customers.">
        </Textarea>


        <Label for="workPhotos" class="mt-5 mb-1">Work Photos</Label>
        <div class="flex gap-1">
          <div v-for="item in photoList" class="w-full max-w-[10rem]">
            <Popover>
              <PopoverTrigger class="w-full h-full">
                <AspectRatio :ratio="1 / 1">
                  <Input type="image" :key="componentKey" :src="item"
                    class="border-0 object-cover w-full h-full rounded-lg" />
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

        <Label for="picture" class="mt-5">Photo Upload</Label>
        <Input id="picture" :key="componentKey" type="file" accept="image/png, image/jpeg" @change="handleFileChange"
          class="w-50" />
      </CardContent>
      <CardFooter class="flex flex-col items-start gap-[16px]">
        <div class="w-full max-w-[8rem] flex flex-col gap-[30px]">
          <p class="text-2xl">Ratings</p>
          <p>Customer 1 (5.0)</p>
          <p>Comment:</p>
          <p>Customer 2 (5.0)</p>
          <p>Comment:</p>
          <p>Customer 3 (5.0)</p>
          <p>Comment:</p>
        </div>
        <Button>Set Profile</Button>
      </CardFooter>
    </Card>
  </div>
</template>
