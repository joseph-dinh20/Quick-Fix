<script setup lang="ts">
import { Card, CardContent } from '@/components/ui/card'
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '@/components/ui/carousel'

import {
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

import { ref, computed } from 'vue'
import workPhoto1 from '@/assets/workPhotos/bathroom.jpg'
import workPhoto2 from '@/assets/workPhotos/garden.jpg'
import workPhoto3 from '@/assets/workPhotos/kitchen.jpg'
import profAvatar from '@/assets/avatars/avatar.png'
import defaultAvatar from '@/assets/avatars/defaultAvatar.png'
import starIcon from '@/assets/icons/star.png'
import aboutMeIcon from '@/assets/icons/aboutMe.png'
import albumIcon from '@/assets/icons/album.png'
import reviewIcon from '@/assets/icons/review.png'

//NOTE: need to use this at some point for setting up date formatting
import { DateFormatter, getLocalTimeZone, today } from '@internationalized/date'

const todayDate = today(getLocalTimeZone())
const provider = ref(
  {
    name: 'Fahd Albinali',
    avatar: profAvatar,
    price: '100',
    workPhotos: [workPhoto1, workPhoto2, workPhoto3, workPhoto1, workPhoto2, workPhoto3],
    aboutMe: 'I am a Professor, a Engineer, a Co-Founder and CEO.',
    totalRating: '150',
    averageRating: '4.9',
    ratings: [
      {
        jobType: 'Gardening',
        userName: 'Andrew Jones',
        date: todayDate,
        userAvatar: defaultAvatar,
        userRated: '5',
        userComment: 'Hot diggity damn this professor has a great mustache',
      },
      {
        jobType: 'Gardening',
        userName: 'Dave Chappelle',
        date: todayDate,
        userAvatar: defaultAvatar,
        userRated: '5',
        userComment: 'Hot diggity damn this professor has a great mustache',
      }
    ],
  },
)

</script>

<template>
  <Carousel class="min-w-200">
    <CarouselContent>
      <CarouselItem v-for="photo in provider.workPhotos">
        <div class="p-1">
          <!-- <Card> -->
          <!-- <CardContent class="flex aspect-square items-center justify-center p-6"> -->
          <div class="flex aspect-square items-center justify-center p-6">
            <img :src="photo" class="w-full h-full object-over" />
          </div>
          <!-- </CardContent> -->
          <!-- </Card> -->
        </div>
      </CarouselItem>
    </CarouselContent>
    <CarouselPrevious />
    <CarouselNext />
  </Carousel>
</template>
