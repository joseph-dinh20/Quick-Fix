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
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

import {
  Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious
} from '@/components/ui/carousel'

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

import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { faker } from '@faker-js/faker';

const provider = ref(
  {
    name: 'Fahd Albinali',
    avatar: profAvatar,
    price: '100',
    workPhotos: [workPhoto1, workPhoto2, workPhoto3, workPhoto1, workPhoto2, workPhoto3],
    aboutMe: 'I am a Professor, a Engineer, a Co-Founder and CEO.',
    averageRating: '4.9',
    ratings: Array.from({ length: 362 }, (_, i) => ({
      jobType: ['Gardening', 'Plumbing', 'Carpentry', 'Electrical'][i % 4],
      userName: faker.person.fullName(),
      date: faker.date.anytime(),
      userAvatar: defaultAvatar,
      userRated: Math.floor(Math.random() * 5) + 1,
      userComment: faker.lorem.paragraph(),
    })),
  },
)

const displayedPhotos = computed(() => provider.value.workPhotos.slice(0, 4))

const totalRating = provider.value.ratings.length
const ratingsPerPage = 3
const currentPage = ref(1)
const chunkUserRating = computed(() => {
  const ratingList = provider.value.ratings
  const chunks = []
  for (let i = 0; i < ratingList.length; i += ratingsPerPage) {
    chunks.push(ratingList.slice(i, i + ratingsPerPage))
  }
  return chunks
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}
</script>

<template>
  <div class="flex justify-center">
    <Card>
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-10 m-2">
          <Avatar class="scale-[2]">
            <AvatarImage :src="provider.avatar" alt="photo" />
            <AvatarFallback>Avatar</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{{ provider.name }}</CardTitle>
            <CardDescription>
              <img class="w-5 inline-block align-top" :src="starIcon">
              {{ provider.averageRating }}
              ({{ totalRating }})
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
        <Separator class="my-4" />
        <CardTitle><img class="w-8 inline-block" :src="aboutMeIcon"> About Me</CardTitle>
        <span> {{ provider.aboutMe }} Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eligendi
          laborum nisi
          reprehenderit aspernatur, quia explicabo blanditiis iste laudantium tempora ducimus corrupti consequuntur
          quibusdam atque, labore sequi quam sunt dolorem ut!🤑🤑🤑
        </span>
        <Separator class="my-2" />
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
            <Dialog>
              <DialogTrigger as-child>
                <button type="button" class="w-full h-full">
                  <AspectRatio :ratio="1 / 1">
                    <div class="relative h-full w-full">
                      <img :src="provider.workPhotos[4]" class="object-cover h-full rounded-lg p-0.5">
                      <div class="rounded-lg absolute inset-0.5 bg-black/50 flex items-center justify-center">
                        <span class="text-xl font-bold text-white">{{ provider.workPhotos.length - 4 }}+</span>
                      </div>
                    </div>
                  </AspectRatio>
                </button>
              </DialogTrigger>
              <DialogContent class="min-w-100 max-w-170 flex justify-center">
                <DialogHeader>
                  <DialogTitle></DialogTitle>
                  <DialogDescription></DialogDescription>
                  <Carousel>
                    <CarouselContent>
                      <CarouselItem v-for="photo in provider.workPhotos">
                        <div class="flex aspect-square items-center justify-center">
                          <img :src="photo" class="w-full h-full object-cover rounded-lg" />
                        </div>
                      </CarouselItem>
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                  </Carousel>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <Separator class="my-2" />
      </CardContent>

      <CardFooter class="flex flex-col">
        <div class="items-start self-start w-full h-auto">
          <CardTitle><img class="w-8 inline-block" :src="reviewIcon"> Ratings</CardTitle>

          <Card v-for="rating in chunkUserRating[currentPage - 1]" :key="rating.userName" class="my-4 p-4">
            <div class="flex items-center gap-3">
              <Avatar class="mr-1">
                <AvatarImage :src="rating.userAvatar" />
                <AvatarFallback>Img</AvatarFallback>
              </Avatar>
              <div class="flex flex-col">
                <p class="font-semibold">{{ rating.userName }}</p>
                <div class="flex items-center gap-0.5">
                  <!-- NOTE: v-for loops functions fine without :key but the docs recommend it -->
                  <!-- in case of change of ordering is needed -->

                  <img v-for="star in 5" :key="star" :src="starIcon" class="w-4 h-4"
                    :class="{ 'opacity-30': star > rating.userRated }" />
                </div>
              </div>
              <div class="flex gap-1 ml-auto">
                <Badge variant="outline">{{ rating.jobType }}</Badge>
                <Badge variant="outline"> Rated on {{ formatDate(rating.date) }}</Badge>
              </div>
            </div>
            <div class="flex flex-col text-sm gap-1">
              <p class="mt-2 line-clamp-4">{{ rating.userComment }}</p>
            </div>
          </Card>
        </div>

        <div v-if="provider.ratings.length > 0">
          <Pagination :items-per-page="ratingsPerPage" :total="provider.ratings.length" :default-page="1"
            @update:page="currentPage = $event">
            <PaginationContent v-slot="{ items }">
              <div class="flex mt-5">
                <PaginationPrevious />
                <div v-for="(item, index) in items" :key="index">
                  <PaginationItem v-if="item.type === 'page'" :value="item.value"
                    :is-active="item.value === currentPage">
                    {{ item.value }}
                  </PaginationItem>
                </div>
                <PaginationEllipsis :index="4" />
                <PaginationNext />
              </div>
            </PaginationContent>
          </Pagination>
        </div>
        <div v-else class="self-start">
          no user ratings yet.
        </div>
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped></style>
