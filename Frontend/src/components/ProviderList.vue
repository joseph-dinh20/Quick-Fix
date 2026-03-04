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
import checkMarkIcon from '@/assets/icons/checkMark.png'
import aboutMeIcon from '@/assets/icons/aboutMe.png'
import albumIcon from '@/assets/icons/album.png'
import reviewIcon from '@/assets/icons/review.png'
import spainFlag from '@/assets/flags/ES.svg'
import vietnamFlag from '@/assets/flags/VN.svg'
import arabicFlag from '@/assets/flags/SA.svg'
import chinaFlag from '@/assets/flags/CN.svg'
import usFlag from '@/assets/flags/US.svg'

import { Separator } from '@/components/ui/separator'
import { ScrollArea } from "@/components/ui/scroll-area"

import { faker } from '@faker-js/faker';
import { Badge } from '@/components/ui/badge'
import Provider from '@/components/Provider.vue'

//NOTE: these data needs to be grabbed from the backend.
//right now averageRating cannot easily be computed on it's own
//since it cannot calculate within something to be initialized
//at the same time.
const generateProvider = () => {
  const jobsCompleted = faker.number.int(150)
  return {
    name: faker.person.fullName(),
    avatar: faker.image.avatar(),
    price: faker.number.int(150),
    workPhotos: [workPhoto1, workPhoto2, workPhoto3, workPhoto1, workPhoto2, workPhoto3],
    aboutMe: faker.lorem.paragraph(20),
    averageRating: '4.9',
    jobsCompleted: jobsCompleted,
    datesBooked: [],
    languages: [spainFlag],
    ratings: Array.from({ length: jobsCompleted }, (_, i) => ({
      jobType: ['Gardening', 'Plumbing', 'Carpentry', 'Electrical'][i % 4],
      userName: faker.person.fullName(),
      date: faker.date.anytime(),
      userAvatar: defaultAvatar,
      userRated: Math.floor(Math.random() * 5) + 1,
      userComment: faker.lorem.paragraph(),
    })),
  }
}

const providers = ref(Array.from({ length: 15 }, generateProvider))

</script>

<template>
  <div v-for="(provider, index) in providers" :key="index" class="m-5">
    <Card class="flex flex-col max-w-150 min-w-120">
      <CardHeader class="justify-between flex-row">
        <!-- <div class="flex flex-row gap-20 m-2 pt-10 pl-10"> -->
        <div class="flex flex-row gap-20 m-2 pl-10">
          <Avatar class="scale-[4] self-center">
            <AvatarImage :src="provider.avatar" alt="@shadcn" />
            <AvatarFallback><img :src="defaultAvatar"></AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{{ provider.name }}</CardTitle>
            <CardDescription class="mt-1">
              <!-- <Badge variant="outline"> -->
              <img class="w-4 inline-block align-top" :src="starIcon">
              {{ provider.averageRating }}
              ({{ provider.ratings.length }})
              reviews
              <!-- </Badge> -->
            </CardDescription>

            <CardDescription class="mt-1 flex flex-col">
              <Badge variant="outline">
                <img class="w-5 inline-block" :src="checkMarkIcon">
                Completed {{ provider.jobsCompleted }} Jobs
              </Badge>
              <Badge variant="outline">
                <img class="w-5 inline-block align-top" :src="checkMarkIcon">
                Fluent in
                <img :src="usFlag" class="w-5">
                <img :src="spainFlag" class="w-5">
                <img :src="chinaFlag" class="w-5">
                <img :src="arabicFlag" class="w-5">
              </Badge>
            </CardDescription>
            <Dialog>
              <DialogTrigger as-child>
                <Button variant="default" class="mt-3">View Profile</Button>
              </DialogTrigger>
              <DialogContent class="h-full max-h-95/100 max-w-150 p-0 gap-0 m-0">
                <DialogHeader class="sr-only">
                  <DialogTitle>Provider Profile</DialogTitle>
                  <DialogDescription>Full provider profile details</DialogDescription>
                </DialogHeader>
                <ScrollArea class="h-full max-h-full">
                  <div class="p-4">
                    <Provider :provider="provider" />
                  </div>
                </ScrollArea>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <CardTitle class="w-15">
          ${{ provider.price }}
          <CardDescription>per hour</CardDescription>
        </CardTitle>
      </CardHeader>
      <CardContent class="flex flex-col gap-2">
        <Separator class="my-2" />
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
