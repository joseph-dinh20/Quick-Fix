<script setup>
import { ref, onMounted } from 'vue'
import { Card } from '@/components/ui/card'

import {
  Table, TableBody, TableCaption, TableCell,
  TableFooter, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'

import {
  Avatar, AvatarImage, AvatarFallback
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'

import {
  Dialog,
  DialogContent,
  DialogTrigger,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'

import { ScrollArea } from '@/components/ui/scroll-area'

import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import starIcon from '@/assets/icons/star.png'
import Provider from '@/components/DemoProvider.vue'

import { getFavorites, toggleFavoriteProvider } from '@/services/api'

const BASE_URL = 'http://localhost:8000'

const absoluteUrl = (path) => {
  if (!path) return ''
  return path.startsWith('http') ? path : `${BASE_URL}${path}`
}

const favoriteProviders = ref([])

function normalizeFavoriteProvider(provider) {
  return {
    ...provider,
    avatar: absoluteUrl(provider.avatar),
    price: provider.price_per_hour,
    aboutMe: provider.about_me,
    averageRating: provider.average_rating,
    jobsCompleted: provider.total_rating || 0,
    ratings: provider.ratings || [],
    services: provider.services || [],
    city: provider.city || "",
    state: provider.state || "",
    workPhotos: (provider.work_images || []).map((img) =>
      absoluteUrl(img.image),
    ),
  };
}

const fetchFavorites = async () => {
  try {
    const response = await getFavorites()
    favoriteProviders.value = response.data.map(normalizeFavoriteProvider)
  } catch (error) {
    console.error('Failed to load favorite providers', error)
    favoriteProviders.value = []
  }
}

const removeFavorite = async (provider) => {
  try {
    await toggleFavoriteProvider(provider.id)
    favoriteProviders.value = favoriteProviders.value.filter(
      (p) => p.id !== provider.id
    )
  } catch (error) {
    console.error('Failed to remove favorite provider', error)
  }
}

onMounted(fetchFavorites)

function formatDate(date) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}
</script>

<template>
  <Card class="p-5">
    <Table>
      <TableHeader>
        <TableRow class="**:text-black **:font-semibold">
          <TableHead class="text-center"></TableHead>
          <TableHead class="text-center">Name</TableHead>
          <TableHead class="text-center">Hired For</TableHead>
          <TableHead class="text-center">Last Hired</TableHead>
          <TableHead class="text-center">You Rated</TableHead>
          <TableHead class="text-center"></TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        <Dialog
          v-for="(provider, i) in favoriteProviders"
          :key="provider.id"
        >
          <!-- entire row clickable -->
          <DialogTrigger as-child>
            <TableRow
              class="transition duration-150 ease-in-out hover:bg-slate-100 hover:shadow-sm cursor-pointer"
              :class="['animate__animated animate__fadeInUp']"
              :style="{ animationDelay: `${i * 0.05}s` }"
            >
              <TableCell class="text-center">
                <Avatar class="scale-[1.3]">
                  <AvatarImage :src="provider.avatar" />
                  <AvatarFallback>
                    <img :src="defaultAvatar" />
                  </AvatarFallback>
                </Avatar>
              </TableCell>

              <TableCell class="text-center">
                {{ provider.name }}
              </TableCell>

              <TableCell class="text-center">
                {{ provider.service_type || '-' }}
              </TableCell>

              <TableCell class="text-center">
                {{ formatDate(provider.last_hired_date) }}
              </TableCell>

              <TableCell class="text-center">
                <span class="inline-flex items-center justify-center gap-1">
                  <template v-if="provider.rating">
                    <img class="w-4" :src="starIcon" />
                    {{ provider.rating }}
                  </template>
                  <template v-else>-</template>
                </span>
              </TableCell>

              <!-- Prevent dialog when clicking Remove -->
              <TableCell class="text-center">
                <Button
                  @click.stop.prevent="removeFavorite(provider)"
                  variant="outline"
                  size="sm"
                  class="hover:bg-destructive hover:text-white"
                >
                  Remove
                </Button>
              </TableCell>
            </TableRow>
          </DialogTrigger>

          <!-- Provider popup -->
          <DialogContent class="h-full max-h-[95vh] max-w-3xl p-0">
            <DialogHeader class="sr-only">
              <DialogTitle>Provider Profile</DialogTitle>
              <DialogDescription>
                Full provider profile details
              </DialogDescription>
            </DialogHeader>

            <ScrollArea class="h-full">
              <div class="p-4">
                <Provider :provider="provider" />
              </div>
            </ScrollArea>
          </DialogContent>
        </Dialog>
      </TableBody>

      <TableFooter></TableFooter>

      <TableCaption>
        A list of your favorited providers.
      </TableCaption>
    </Table>
  </Card>
</template>

<style scoped></style>