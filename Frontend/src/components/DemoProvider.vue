<script setup>
import {
  Card, CardContent, CardDescription, CardFooter,
  CardHeader, CardTitle,
} from '@/components/ui/card'

import {
  Avatar, AvatarFallback, AvatarImage,
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { AspectRatio } from '@/components/ui/aspect-ratio'
import { Label } from '@/components/ui/label'

import {
  Popover, PopoverContent, PopoverTrigger,
} from '@/components/ui/popover'

import {
  Dialog, DialogClose, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from '@/components/ui/dialog'

import {
  Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious
} from '@/components/ui/carousel'

import {
  Pagination, PaginationContent, PaginationEllipsis, PaginationItem,
  PaginationNext, PaginationPrevious,
} from '@/components/ui/pagination'

import {
  HoverCard, HoverCardContent, HoverCardTrigger,
} from '@/components/ui/hover-card'

import { ref, computed, watch, onMounted } from 'vue'
// import workPhoto1 from '@/assets/workPhotos/bathroom.jpg'
// import workPhoto2 from '@/assets/workPhotos/garden.jpg'
// import workPhoto3 from '@/assets/workPhotos/kitchen.jpg'
// import profAvatar from '@/assets/avatars/avatar.png'
// import defaultAvatar from '@/assets/avatars/defaultAvatar.png'
import starIcon from '@/assets/icons/star.png'
import aboutMeIcon from '@/assets/icons/aboutMe.png'
import albumIcon from '@/assets/icons/album.png'
import reviewIcon from '@/assets/icons/review.png'

import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { faker } from '@faker-js/faker';
import checkMarkIcon from '@/assets/icons/checkMark.png'
import { fetchReviews } from '@/services/api'

//NOTE: grabs data from ProviderList.vue component
const { provider } = defineProps(['provider'])

const displayedPhotos = computed(() => provider.workPhotos.slice(0, 4))
const totalRating = provider.ratings.length
const ratingsPerPage = 3
const currentPage = ref(1)
const chunkUserRating = computed(() => {
  const ratingList = provider.ratings
  const chunks = []
  for (let i = 0; i < ratingList.length; i += ratingsPerPage) {
    chunks.push(ratingList.slice(i, i + ratingsPerPage))
  }
  return chunks
})

const reviews = ref([])
const reviewsLoading = ref(false)
const reviewsPerPage = 3
const currentReviewPage = ref(1)

const paginatedReviews = computed(() => {
  const start = (currentReviewPage.value - 1) * reviewsPerPage
  const end = start + reviewsPerPage
  return reviews.value.slice(start, end)
})

const totalReviewPages = computed(() => Math.ceil(reviews.value.length / reviewsPerPage))

async function loadProviderReviews() {
  if (!provider?.id) return
  reviewsLoading.value = true
  try {
    const res = await fetchReviews(provider.id)
    reviews.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    reviewsLoading.value = false
  }
}

// format date to human readable format
function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

// bool state var for read more and read less.
const isExpanded = ref(false)

//NOTE: all this to get photo Carousel number update ex. 4th out of 6 photos (4/6)
const api = ref()
const totalCount = ref(0)
const current = ref(0)

const showReadMoreButton = computed(() => {
  return provider.aboutMe.split(' ').length > 80
})

function setApi(val) {
  api.value = val
}

watch(api, (api) => {
  if (!api)
    return
  totalCount.value = api.scrollSnapList().length
  current.value = api.selectedScrollSnap() + 1
  api.on('select', () => {
    current.value = api.selectedScrollSnap() + 1
  })
})

onMounted(loadProviderReviews)

//BUG: Debugging Area
console.log('length of user aboutMe description = ' + provider.aboutMe.split(' ').length)
console.log('showReadMoreButton state = ' + showReadMoreButton.value)
</script>

<template>
  <div class="flex justify-center items-center pt-[10vh]">
    <Card>
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-10 m-2">
          <Avatar class="scale-[2]">
            <AvatarImage :src="provider.avatar" alt="photo" />
            <AvatarFallback>Avatar</AvatarFallback>
          </Avatar>
          <div class="flex flex-col h-10">
            <CardTitle>{{ provider.name }}</CardTitle>
            <CardDescription class="mt-1 text-sm text-slate-500">
              {{ provider.city || 'Location unknown' }}, {{ provider.state || '' }}
            </CardDescription>
            <CardDescription class="mt-1">
              <Badge variant="outline">
                <img class="w-4 inline-block align-top" :src="starIcon">
                {{ provider.averageRating }}
                ({{ reviews.length }})
                reviews
              </Badge>
            </CardDescription>
            <Badge variant="outline">
              <img class="w-4 inline-block" :src="checkMarkIcon">
              Completed {{ provider.jobsCompleted }} Jobs
            </Badge>
          </div>
        </div>
        <div class="flex flex-col items-center">
          <CardTitle> ${{ provider.price }} / hr </CardTitle>
          <Button class="mt-2">Select Me</Button>
        </div>
      </CardHeader>
        <div class="flex flex-wrap gap-2 mt-2 px-4 py-2">
          <div v-for="service in provider.services" :key="service.id">
            <Badge variant="secondary" size="sm">{{ service.name }}</Badge>
          </div>
        </div>
      <CardContent class="flex flex-col gap-2">
        <Separator class="my-4" />
        <CardTitle><img class="w-8 inline-block" :src="aboutMeIcon"> About Me</CardTitle>
        <span :class="{ 'line-clamp-10': !isExpanded }"> {{ provider.aboutMe }} </span>
        <Button v-if="showReadMoreButton" variant="link" @click="isExpanded = !isExpanded"
          class="p-0 text-sm text-blue-500 hover:text-blue-700 font-medium mt-1 self-start">
          {{ isExpanded ? 'Hide ↑' : 'Read More ↓' }}
        </Button>
        <Separator class="my-2" />
        <CardTitle> <img class="w-8 inline-block" :src="albumIcon"> Work Photos</CardTitle>
        <div id="workPhotos" class="flex">
          <div v-for="photo in displayedPhotos" class="w-25">
            <HoverCard :open-delay="50" :close-delay="0">
              <HoverCardTrigger as-child>
                <AspectRatio :ratio="1 / 1">
                  <img :src="photo" class="object-cover h-full rounded-lg p-0.5" />
                </AspectRatio>
              </HoverCardTrigger>
              <HoverCardContent class="w-130 border-0">
                <AspectRatio :ratio="3 / 2">
                  <img :src="photo" class="w-full h-full rounded-lg" />
                </AspectRatio>
              </HoverCardContent>
            </HoverCard>
          </div>

          <!-- NOTE: If provider has more than 4 images, show the Carousel. -->
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
                  <Carousel class="flex flex-col items-center" :opts="{ startIndex: 4, loop: true, duration: 10 }"
                    @init-api="setApi">
                    <CarouselContent>
                      <CarouselItem v-for="(photo, index) in provider.workPhotos" :key="photo.name">
                        <div class="aspect-square">
                          <img :src="photo" class="w-full h-full object-cover rounded-lg" />
                        </div>
                      </CarouselItem>
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                    <Badge class="mt-2 text-sm bg-blue-500 text-white" variant="outline">
                      {{ current }} of {{ totalCount }} photos
                    </Badge>
                  </Carousel>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>
          <div v-else-if="provider.workPhotos.length === 0" class="text-sm text-slate-500 mt-2">
            No images yet.
          </div>
        </div>
        <Separator class="my-2" />
      </CardContent>

      <!-- NOTE: Provider Ratings Section -->
      <CardFooter class="flex flex-col">
        <div v-if="provider.ratings.length > 0" class="items-start self-start w-full h-auto">
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
        <!-- <div v-else-if="reviews.length === 0" class="self-start">
          no user ratings yet.
        </div> -->

        <div class="self-start mt-6 w-full">
          <CardTitle><img class="w-8 inline-block" :src="reviewIcon"> Customer Reviews ({{ reviews.length }})</CardTitle>
          <div v-if="reviewsLoading" class="text-sm text-slate-500 mt-2">Loading reviews...</div>
          <div v-else-if="reviews.length">
            <div v-for="review in paginatedReviews" :key="review.id" class="border rounded-lg p-4 mt-3">
              <div class="flex items-center justify-between gap-3">
                <div>
                  <p class="font-semibold">{{ review.reviewer_name }}</p>
                  <div class="flex items-center gap-1 mt-1">
                    <img
                      v-for="star in 5"
                      :key="star"
                      :src="starIcon"
                      class="w-4 h-4"
                      :class="{ 'opacity-30': star > review.rating }"
                    />
                  </div>
                </div>
                <span class="text-xs uppercase tracking-wide text-slate-500">{{ new Date(review.created_at).toLocaleDateString() }}</span>
              </div>
              <p class="mt-3 text-sm text-slate-700">{{ review.comment }}</p>
              <div v-if="review.images && review.images.length" class="mt-3 flex gap-2 flex-wrap">
                <div v-for="image in review.images" :key="image.id" class="w-16">
                  <HoverCard :open-delay="50" :close-delay="0">
                    <HoverCardTrigger as-child>
                      <AspectRatio :ratio="1 / 1">
                        <img :src="'http://localhost:8000' + image.image" class="object-cover h-full rounded-lg cursor-pointer" alt="Review image" />
                      </AspectRatio>
                    </HoverCardTrigger>
                    <HoverCardContent class="w-80 border-0">
                      <AspectRatio :ratio="3 / 2">
                        <img :src="'http://localhost:8000' + image.image" class="w-full h-full rounded-lg" alt="Review image enlarged" />
                      </AspectRatio>
                    </HoverCardContent>
                  </HoverCard>
                </div>
              </div>
            </div>
            <div v-if="totalReviewPages > 1" class="mt-4">
              <Pagination :total="reviews.length" :items-per-page="reviewsPerPage" :default-page="1" @update:page="currentReviewPage = $event">
                <PaginationContent>
                  <PaginationPrevious />
                  <PaginationItem
                    v-for="page in totalReviewPages"
                    :key="page"
                    :value="page"
                    :is-active="page === currentReviewPage"
                  >
                    {{ page }}
                  </PaginationItem>
                  <PaginationNext />
                </PaginationContent>
              </Pagination>
            </div>
          </div>
          <div v-else class="text-sm text-slate-500 mt-2">No reviews yet.</div>
        </div>
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped></style>