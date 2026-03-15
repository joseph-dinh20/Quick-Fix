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
import { AspectRatio } from '@/components/ui/aspect-ratio'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

import {
  Dialog,
  DialogContent,
  DialogDescription,
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

import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'

import { ref, computed, onMounted } from 'vue'
import starIcon from '@/assets/icons/star.png'
import aboutMeIcon from '@/assets/icons/aboutMe.png'
import albumIcon from '@/assets/icons/album.png'
import reviewIcon from '@/assets/icons/review.png'

import {
  getServices,
  loadMyProvider,
  updateProviderServices,
} from '@/services/api.js'

const { provider } = defineProps({
  provider: {
    type: Object,
    default: null,
  }
})

const fallbackProvider = ref(null)
const allServices = ref([])
const selectedServices = ref([])
const servicesMessage = ref('')
const savingServices = ref(false)
const loadingServices = ref(true)

const currentProvider = computed(() => provider || fallbackProvider.value || {
  name: '',
  avatar: '',
  averageRating: 0,
  average_rating: 0,
  price: 0,
  price_per_hour: 0,
  aboutMe: '',
  about_me: '',
  workPhotos: [],
  work_images: [],
  ratings: [],
  services: [],
})

const normalizedWorkPhotos = computed(() => {
  if (currentProvider.value?.workPhotos?.length) {
    return currentProvider.value.workPhotos
  }

  if (currentProvider.value?.work_images?.length) {
    return currentProvider.value.work_images.map((img) => {
      if (typeof img === 'string') return img
      if (img?.image) {
        return img.image.startsWith('http')
          ? img.image
          : `http://localhost:8000${img.image}`
      }
      return ''
    }).filter(Boolean)
  }

  return []
})

const displayedPhotos = computed(() => normalizedWorkPhotos.value.slice(0, 4))

const normalizedRatings = computed(() => currentProvider.value?.ratings || [])
const totalRating = computed(() => {
  if (normalizedRatings.value.length) return normalizedRatings.value.length
  return currentProvider.value?.total_rating || 0
})

const ratingsPerPage = 3
const currentPage = ref(1)

const chunkUserRating = computed(() => {
  const ratingList = normalizedRatings.value
  const chunks = []

  for (let i = 0; i < ratingList.length; i += ratingsPerPage) {
    chunks.push(ratingList.slice(i, i + ratingsPerPage))
  }

  return chunks
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function toggleService(serviceId) {
  if (selectedServices.value.includes(serviceId)) {
    selectedServices.value = selectedServices.value.filter(id => id !== serviceId)
  } else {
    selectedServices.value = [...selectedServices.value, serviceId]
  }
}

async function fetchServiceData() {
  try {
    loadingServices.value = true
    servicesMessage.value = ''

    const [servicesRes, myProviderRes] = await Promise.all([
      getServices(),
      loadMyProvider(),
    ])

    allServices.value = servicesRes.data
    fallbackProvider.value = myProviderRes.data

    selectedServices.value = (myProviderRes.data.services || []).map(service => service.id)
  } catch (err) {
    console.error('Error loading services/provider:', err)
    servicesMessage.value = 'Could not load services.'
  } finally {
    loadingServices.value = false
  }
}

async function saveServices() {
  try {
    savingServices.value = true
    servicesMessage.value = ''

    await updateProviderServices(selectedServices.value)
    servicesMessage.value = 'Services updated successfully.'

    const refreshed = await loadMyProvider()
    fallbackProvider.value = refreshed.data
    selectedServices.value = (refreshed.data.services || []).map(service => service.id)
  } catch (err) {
    console.error('Error updating services:', err)
    servicesMessage.value = 'Failed to update services.'
  } finally {
    savingServices.value = false
  }
}

onMounted(() => {
  fetchServiceData()
})
</script>

<template>
  <div class="flex justify-center">
    <Card class="w-full max-w-5xl">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-10 m-2">
          <Avatar class="scale-[2]">
            <AvatarImage
              :src="currentProvider.avatar ? (currentProvider.avatar.startsWith('http') ? currentProvider.avatar : 'http://localhost:8000' + currentProvider.avatar) : ''"
              alt="photo"
            />
            <AvatarFallback>Avatar</AvatarFallback>
          </Avatar>

          <div>
            <CardTitle>{{ currentProvider.name }}</CardTitle>
            <CardDescription>
              <img class="w-5 inline-block align-top" :src="starIcon">
              {{ currentProvider.averageRating || currentProvider.average_rating || 0 }}
              ({{ totalRating }})
              reviews
            </CardDescription>
          </div>
        </div>

        <div class="flex flex-col items-center">
          <CardTitle class="mb-2">
            ${{ currentProvider.price || currentProvider.price_per_hour || 0 }}/hr
          </CardTitle>
          <Button>Select Me</Button>
        </div>
      </CardHeader>

      <CardContent class="flex flex-col gap-2">
        <Separator class="my-4" />

        <CardTitle>
          <img class="w-8 inline-block" :src="aboutMeIcon"> About Me
        </CardTitle>

        <span>
          {{ currentProvider.aboutMe || currentProvider.about_me || 'No bio yet.' }}
        </span>

        <Separator class="my-2" />

        <CardTitle class="mb-2">Services</CardTitle>

        <div v-if="loadingServices" class="text-sm text-gray-500">
          Loading services...
        </div>

        <div v-else class="flex flex-col gap-3">
          <div class="flex flex-wrap gap-3">
            <label
              v-for="service in allServices"
              :key="service.id"
              class="flex items-center gap-2 border rounded-md px-3 py-2 cursor-pointer"
            >
              <input
                type="checkbox"
                :checked="selectedServices.includes(service.id)"
                @change="toggleService(service.id)"
              />
              <span>{{ service.name }}</span>
            </label>
          </div>

          <div class="flex items-center gap-3">
            <Button @click="saveServices" :disabled="savingServices">
              {{ savingServices ? 'Saving...' : 'Save Services' }}
            </Button>
            <span v-if="servicesMessage" class="text-sm">
              {{ servicesMessage }}
            </span>
          </div>
        </div>

        <Separator class="my-2" />

        <CardTitle>
          <img class="w-8 inline-block" :src="albumIcon"> Work Photos
        </CardTitle>

        <div id="workPhotos" class="flex">
          <div v-for="photo in displayedPhotos" :key="photo" class="w-25">
            <Popover>
              <PopoverTrigger class="w-full h-full">
                <AspectRatio :ratio="1 / 1">
                  <img :src="photo" class="object-cover h-full rounded-lg p-0.5" />
                </AspectRatio>
              </PopoverTrigger>

              <PopoverContent class="w-130 border-0">
                <AspectRatio :ratio="3 / 2">
                  <img :src="photo" class="w-full h-full rounded-lg" />
                </AspectRatio>
              </PopoverContent>
            </Popover>
          </div>

          <div v-if="normalizedWorkPhotos.length > 4" class="w-25">
            <Dialog>
              <DialogTrigger as-child>
                <button type="button" class="w-full h-full">
                  <AspectRatio :ratio="1 / 1">
                    <div class="relative h-full w-full">
                      <img :src="normalizedWorkPhotos[4]" class="object-cover h-full rounded-lg p-0.5">
                      <div class="rounded-lg absolute inset-0.5 bg-black/50 flex items-center justify-center">
                        <span class="text-xl font-bold text-white">{{ normalizedWorkPhotos.length - 4 }}+</span>
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
                      <CarouselItem v-for="photo in normalizedWorkPhotos" :key="photo">
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
          <CardTitle>
            <img class="w-8 inline-block" :src="reviewIcon"> Ratings
          </CardTitle>

          <Card
            v-for="rating in (chunkUserRating[currentPage - 1] || [])"
            :key="rating.userName"
            class="my-4 p-4"
          >
            <div class="flex items-center gap-3">
              <Avatar class="mr-1">
                <AvatarImage :src="rating.userAvatar" />
                <AvatarFallback>Img</AvatarFallback>
              </Avatar>

              <div class="flex flex-col">
                <p class="font-semibold">{{ rating.userName }}</p>
                <div class="flex items-center gap-0.5">
                  <img
                    v-for="star in 5"
                    :key="star"
                    :src="starIcon"
                    class="w-4 h-4"
                    :class="{ 'opacity-30': star > rating.userRated }"
                  />
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

        <div v-if="normalizedRatings.length > 0">
          <Pagination
            :items-per-page="ratingsPerPage"
            :total="normalizedRatings.length"
            :default-page="1"
            @update:page="currentPage = $event"
          >
            <PaginationContent v-slot="{ items }">
              <div class="flex mt-5">
                <PaginationPrevious />
                <div v-for="(item, index) in items" :key="index">
                  <PaginationItem
                    v-if="item.type === 'page'"
                    :value="item.value"
                    :is-active="item.value === currentPage"
                  >
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