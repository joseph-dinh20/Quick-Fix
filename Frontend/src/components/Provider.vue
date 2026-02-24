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

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'

import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '@/components/ui/carousel'

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

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
    // ratings: [
    //   {
    //     jobType: 'Gardening',
    //     userName: 'Andrew Jones',
    //     date: todayDate,
    //     userAvatar: defaultAvatar,
    //     userRated: '5',
    //     userComment: 'Hot diggity damn this professor has a great mustache',
    //   },
    //   {
    //     jobType: 'Gardening',
    //     userName: 'Dave Chappelle',
    //     date: todayDate,
    //     userAvatar: defaultAvatar,
    //     userRated: '5',
    //     userComment: 'Hot diggity damn this professor has a great mustache',
    //   }
    // ],
    //NOTE: generated temporary list of ratings to display
    ratings: Array.from({ length: 25 }, (_, i) => ({
      jobType: ['Gardening', 'Plumbing', 'Carpentry', 'Electrical'][i % 4],
      userName: `User ${i + 1}`,
      date: todayDate,
      userAvatar: defaultAvatar,
      userRated: Math.floor(Math.random() * 2) + 4, // 4 or 5 stars
      userComment: `This is rating #${i + 1}. Excellent service and very professional.`,
    })),
  },
)

//NOTE: slicing and display only up to 4 images
const displayedPhotos = computed(() => provider.value.workPhotos.slice(0, 4))

</script>

<template>
  <div>
    <Card class="flex flex-col max-w-200 min-w-120">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-10 m-2">
          <Avatar class="scale-[2]">
            <AvatarImage :src="provider.avatar" alt="@shadcn" />
            <AvatarFallback>Avatar</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{{ provider.name }}</CardTitle>
            <CardDescription>
              <img class="w-5 inline-block" :src="starIcon">
              {{ provider.averageRating }}
              ({{ provider.totalRating }})
              reviews
            </CardDescription>
          </div>
        </div>
        <div>
          <CardTitle>
            ${{ provider.price }}/hr
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent class="flex flex-col gap-2">
        <CardTitle><img class="w-8 inline-block" :src="aboutMeIcon"> About Me</CardTitle>
        <span> {{ provider.aboutMe }} Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eligendi
          laborum nisi
          reprehenderit aspernatur, quia explicabo blanditiis iste laudantium tempora ducimus corrupti consequuntur
          quibusdam atque, labore sequi quam sunt dolorem ut!
        </span>
        <CardTitle> <img class="w-8 inline-block" :src="albumIcon"> Work Photos</CardTitle>
        <div id="workPhotos" class="flex">
          <div v-for="photo in displayedPhotos" class="w-25">
            <Popover>
              <PopoverTrigger class="w-full h-full">
                <AspectRatio :ratio="1 / 1">
                  <img :src="photo" class="object-cover h-full rounded-lg p-0.5" />
                </AspectRatio>
                <PopoverContent class="w-150 border-0">
                  <AspectRatio :ratio="3 / 2">
                    <img :src="photo" class="w-full h-full rounded-lg" />
                  </AspectRatio>
                </PopoverContent>
              </PopoverTrigger>
            </Popover>
          </div>
          <div v-if="provider.workPhotos.length > 4" class="w-25">
            <AlertDialog>
              <AlertDialogTrigger as-child>
                <button type="button" class="w-full h-full">
                  <AspectRatio :ratio="1 / 1">
                    <div class="relative h-full w-full">
                      <img :src="provider.workPhotos[4]" class="object-cover h-full rounded-lg p-0.5">
                      <div class="rounded-lg absolute inset-0.5 bg-black/50
                    flex items-center justify-center">
                        <span class="text-xl font-bold text-white">{{ provider.workPhotos.length - 4 }}+</span>
                      </div>
                    </div>
                  </AspectRatio>
                </button>
              </AlertDialogTrigger>
              <AlertDialogContent class="min-w-100 max-w-170 flex justify-center">
                <AlertDialogHeader>
                  <AlertDialogTitle></AlertDialogTitle>
                  <AlertDialogDescription>
                  </AlertDialogDescription>
                  <Carousel>
                    <CarouselContent>
                      <CarouselItem v-for="photo in provider.workPhotos">
                        <div class="flex aspect-square items-center justify-center">
                          <img :src="photo" class="w-full h-full object-over rounded-lg" />
                        </div>
                      </CarouselItem>
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                  </Carousel>
                </AlertDialogHeader>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
      </CardContent>
      <CardFooter class="flex flex-col items-start gap-[10px]">
        <CardTitle><img class="w-8 inline-block" :src="reviewIcon"> Ratings</CardTitle>
        <div v-if="provider.ratings.length > 0">
          <div v-for="rating in provider.ratings" class="flex flex-col gap-1">
            <div class="flex flex-row">
              <Avatar class="scale-[1] mr-1">
                <AvatarImage :src="rating.userAvatar" />
                <AvatarFallback>Img</AvatarFallback>
              </Avatar>
              <div>
                <p>{{ rating.userName }}</p>
                <p>Rated: {{ rating.userRated }} stars</p>
              </div>
            </div>

            <div class="flex flex-col">
              <p>Hired For: {{ rating.jobType }}</p>
              <p>Date: {{ rating.date }}</p>
              <p>Comment: {{ rating.userComment }}</p>
            </div>
          </div>
        </div>
        <Pagination v-slot="{ page }" :items-per-page="1" :total="provider.ratings.length" :default-page="1">
          <PaginationContent v-slot="{ items }">
            <PaginationPrevious />
            <div v-for="(item, index) in items" :key="index">
              <PaginationItem v-if="item.type === 'page'" :value="item.value" :is-active="item.value === page">
                {{ item.value }}
              </PaginationItem>
            </div>
            <PaginationEllipsis :index="4" />
            <PaginationNext />
          </PaginationContent>
        </Pagination>
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped>
/* * { */
/*   margin: 0; */
/*   padding: 0; */
/* } */
</style>
