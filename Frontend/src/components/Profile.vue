<script setup lang="ts">
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
import { ref } from 'vue'

const photo = ref('https://thumbs.dreamstime.com/b/man-lawn-mower-cutting-grass-garden-summer-works-care-169327253.jpg')
const avatar = ref('https://media.tenor.com/hHO9MW5-yw8AAAAM/jjk-jujutsu-kaisen.gif')
</script>

<template>
  <div class="justify-items-center">
    <p class="text-3xl">Setup your profile for {Job Title} </p>
    <Card class="min-h-200 min-w-200">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-[30px]">
          <Avatar class="scale-[1.8]">
            <AvatarImage :src="avatar" alt="@shadcn" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>
              Enter Name Here
            </CardTitle>
            <Input id="name" type="text" placeholder="Enter your name here..."></Input>
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
          placeholder="Write short but detailed description on how you can help the customers."></Textarea>
      </CardContent>
      <CardFooter class="flex flex-col items-start gap-[16px]">
        <p>Photos</p>
        <div class="w-full max-w-[8rem] flex flex-col gap-[30px]">
          <AspectRatio :ratio="1 / 1" class="rounded-lg flex gap-[10px]">
            <img class="rounded-lg" :src="photo" alt="Worker Photo" fill>
            <img class="rounded-lg" :src="photo" alt="Worker Photo" fill>
            <img class="rounded-lg" :src="photo" alt="Worker Photo" fill>
          </AspectRatio>
          <p class="text-2xl">Ratings</p>
          <p>Customer (5.0)</p>
          <p>Comment:</p>
        </div>
        <Button>Set Profile</Button>
      </CardFooter>
    </Card>
  </div>
</template>
