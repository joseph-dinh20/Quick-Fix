<script setup>
import { ref, onMounted } from 'vue'
import { Card } from '@/components/ui/card'

import {
  Table, TableBody, TableCaption, TableCell,
  TableFooter, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'

import {
  Avatar, AvatarImage,
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from '@/components/ui/dialog'

import starIcon from '@/assets/icons/star.png'
import Provider from '@/components/Provider.vue'

import { getFavorites, toggleFavoriteProvider } from '@/services/api'

const BASE_URL = 'http://localhost:8000'

const absoluteUrl = (path) => {
  if (!path) return ''
  return path.startsWith('http') ? path : `${BASE_URL}${path}`
}

const favoriteProviders = ref([])
const selectedProvider = ref(null)
const dialogOpen = ref(false)

const normalizeFavoriteProvider = (provider) => ({
  ...provider,
  avatar: absoluteUrl(provider.avatar),
  price: provider.price_per_hour ?? provider.price ?? 0,
  aboutMe: provider.about_me ?? provider.aboutMe ?? '',
  averageRating: provider.average_rating ?? provider.averageRating ?? 0,
  jobsCompleted: provider.total_rating ?? 0,
  ratings: provider.ratings ?? [],
  services: provider.services ?? [],
  city: provider.profile?.city ?? provider.city ?? '',
  state: provider.profile?.state ?? provider.state ?? '',
  workPhotos: (provider.work_images || []).map((image) => absoluteUrl(image.image)),
})

const fetchFavorites = async () => {
  try {
    const response = await getFavorites()
    favoriteProviders.value = (response.data || []).map(normalizeFavoriteProvider)
  } catch (error) {
    console.error('Failed to load favorite providers', error)
    favoriteProviders.value = []
  }
}

const removeFavorite = async (provider) => {
  try {
    await toggleFavoriteProvider(provider.id)
    favoriteProviders.value = favoriteProviders.value.filter((p) => p.id !== provider.id)
  } catch (error) {
    console.error('Failed to remove favorite provider', error)
  }
}

const openDialog = (provider) => {
  selectedProvider.value = provider
  dialogOpen.value = true
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
          <!-- <TableHead>Avatar</TableHead> -->
          <TableHead class="text-center"></TableHead>
          <TableHead class="w-50 text-center">Name</TableHead>
          <TableHead class="w-50 text-center">Hired For</TableHead>
          <TableHead class="w-50 text-center">Last Hired</TableHead>
          <TableHead class="w-50 text-center">You Rated</TableHead>
          <TableHead class="text-center"></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="(provider, i) in favoriteProviders"
          :key="provider.id"
          class="transition duration-150 ease-in-out hover:bg-slate-100 hover:shadow-sm cursor-pointer"
          :class="['animate__animated animate__fadeInUp']"
          :style="{ animationDelay: `${i * 0.05}s` }"
          @click="openDialog(provider)"
        >
          <TableCell class="text-center">
            <Avatar class="scale-[1.3] align-top">
              <AvatarImage :src="provider.avatar" />
            </Avatar>
          </TableCell>
          <TableCell class="text-center"> {{ provider.name }} </TableCell>
          <TableCell class="text-center">
            {{ provider.service_type || '-' }}
          </TableCell>
          <TableCell class="text-center">{{ formatDate(provider.last_hired_date) }}</TableCell>
          <TableCell class="text-center">
            <span class="inline-flex items-center justify-center gap-1">
              <template v-if="provider.rating !== null && provider.rating !== undefined">
                <img class="w-4 inline-block align-top" :src="starIcon" />
                {{ provider.rating }}
              </template>
              <template v-else>-</template>
            </span>
          </TableCell>
          <TableCell class="text-center space-x-2">
            <Button @click.stop.prevent="removeFavorite(provider)" class="hover:bg-destructive hover:text-white"
              variant="outline" size="sm">Remove</Button>
          </TableCell>
        </TableRow>
      </TableBody>
      <TableFooter>
        <!-- <TableRow> -->
        <!--   <TableCell colspan="3"> -->
        <!--     Total -->
        <!--   </TableCell> -->
        <!--   <TableCell class="text-right"> -->
        <!--     $2,500.00 -->
        <!--   </TableCell> -->
        <!-- </TableRow> -->
      </TableFooter>
      <TableCaption>A list of your favorited providers.</TableCaption>
    </Table>

  </Card>

  <Dialog :open="dialogOpen" @update:open="dialogOpen = $event">
    <DialogContent class="max-w-6xl p-0 h-[90vh] max-h-[90vh] overflow-auto">
      <div class="p-4 h-full">
        <Provider v-if="selectedProvider" :provider="selectedProvider" />
      </div>
    </DialogContent>
  </Dialog>
</template>
