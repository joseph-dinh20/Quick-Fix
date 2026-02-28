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

import { Separator } from '@/components/ui/separator'
import { ScrollArea } from "@/components/ui/scroll-area"

import { faker } from '@faker-js/faker';
import { Badge } from '@/components/ui/badge'
import Provider from '@/components/Provider.vue'

const lorem = faker.lorem.paragraph(20)
const provider = ref(
  {
    name: 'Fahd Albinali',
    avatar: profAvatar,
    price: '100',
    workPhotos: [workPhoto1, workPhoto2, workPhoto3, workPhoto1, workPhoto2, workPhoto3],
    aboutMe: lorem,
    totalRating: '150',
    averageRating: '4.9',
    ratings: Array.from({ length: 26 }, (_, i) => ({
      jobType: ['Gardening', 'Plumbing', 'Carpentry', 'Electrical'][i % 4],
      userName: `User ${i + 1}`,
      date: faker.date.anytime(),
      userAvatar: defaultAvatar,
      userRated: Math.floor(Math.random() * 5) + 1,
      userComment: faker.lorem.paragraph(),
    })),
  },
)

const displayedPhotos = computed(() => provider.value.workPhotos.slice(0, 4))
const ratingsPerPage = 5
const currentPage = ref(1)
const chunkUserRating = computed(() => {
  const ratingList = provider.value.ratings
  const chunks = []
  for (let i = 0; i < ratingList.length; i += ratingsPerPage) {
    chunks.push(ratingList.slice(i, i + ratingsPerPage))
  }
  return chunks
})
</script>

<template>
  <div v-for="i in 10" class="m-5">
    <Card class="flex flex-col max-w-150 min-w-50">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-20 m-2 pt-10 pl-10">
          <Avatar class="scale-[4]">
            <AvatarImage :src="provider.avatar" alt="@shadcn" />
            <AvatarFallback>Avatar</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{{ provider.name }}</CardTitle>
            <CardDescription>
              <img class="w-5 inline-block align-top" :src="starIcon">
              {{ provider.averageRating }}
              ({{ provider.totalRating }})
              reviews
            </CardDescription>
            <Dialog>
              <DialogTrigger as-child>
                <Button variant="default" class="mt-5">View Profile</Button>
              </DialogTrigger>
              <DialogContent class="h-full max-h-95/100 max-w-200 p-0 gap-0 m-0">
                <DialogHeader class="sr-only">
                  <DialogTitle>Provider Profile</DialogTitle>
                  <DialogDescription>Full provider profile details</DialogDescription>
                </DialogHeader>
                <ScrollArea class="h-full max-h-full">
                  <div class="p-4">
                    <Provider />
                  </div>
                </ScrollArea>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <CardTitle>
          <Badge variant="outline" class="text-lg">${{ provider.price }}/hr</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent class="flex flex-col gap-2">
        <Separator class="my-4" />
        <CardTitle><img class="w-8 inline-block" :src="aboutMeIcon"> About Me</CardTitle>
        <span class="line-clamp-4"> {{ provider.aboutMe }} </span>
        <Separator class="my-2" />
      </CardContent>
      <CardFooter class="flex flex-col">
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped></style>
