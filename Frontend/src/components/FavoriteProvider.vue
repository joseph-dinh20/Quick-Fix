<script setup>
import { ref } from 'vue'
import {
  Card, CardContent,
  CardDescription, CardFooter, CardHeader,
  CardTitle,
} from '@/components/ui/card'

import {
  Table, TableBody, TableCaption, TableCell,
  TableFooter, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'

import {
  Avatar, AvatarFallback, AvatarImage,
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

import avatar1 from '@/assets/avatars/avatar.jpg'
import avatar2 from '@/assets/avatars/avatar.png'
import starIcon from '@/assets/icons/star.png'
import deleteIcon from '@/assets/icons/delete.png'

import { favoriteListStore } from '@/store/userList'
import { storeToRefs } from 'pinia'

//NOTE: Data Display Example
const store = favoriteListStore()
const { favoriteProviders } = storeToRefs(store)
const currentUser = ref('')

console.log(favoriteProviders)
function removeFavorite(provider) {
  console.log('provider unfavorited -> ' + provider.name)
  favoriteProviders.value = favoriteProviders.value.filter((p) => p !== provider)
}

// format date to human readable format
function formatDate(date) {
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
          <TableHead></TableHead>
          <TableHead class="w-50">Name</TableHead>
          <TableHead class="w-50">Hired For</TableHead>
          <TableHead class="w-50">Last Hired</TableHead>
          <TableHead class="w-50">You Rated</TableHead>
          <TableHead></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="(provider, i) in favoriteProviders"
          :key="provider.userID"
          :class="['animate__animated animate__fadeInUp']"
          :style="{ animationDelay: `${i * 0.05}s`}"
        >
          <TableCell>
            <Avatar class="scale-[1.3] align-top">
              <AvatarImage :src="provider.avatar" />
            </Avatar>
          </TableCell>
          <TableCell> {{ provider.name }} </TableCell>
          <TableCell>
            <Badge variant="outline" class="scale-[1.1] bg-green-600 text-white">{{ provider.hiredFor }}</Badge>
          </TableCell>
          <TableCell>{{ formatDate(provider.dateRecentlyHired) }}</TableCell>
          <TableCell>
            <Badge variant="ghost" class="scale-[1.1]">
              <img class="w-4 inline-block align-top" :src="starIcon">
              {{ provider.userRated }}.0
            </Badge>
          </TableCell>
          <TableCell><Button @click="removeFavorite(provider)" class="hover:bg-destructive hover:text-white"
              variant="outline" size="sm">Remove</Button></TableCell>
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
</template>
