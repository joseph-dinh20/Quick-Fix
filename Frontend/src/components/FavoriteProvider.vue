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

import { Button } from '@/components/ui/button'

//NOTE: Data Display Example
const currentUser = ref('')
const providerArray = ref([
  {
    userID: 100,
    name: 'John Cena',
    dateRecentHired: '2022-02-22',
    hiredFor: 'Plumming',
    userRated: '5 stars'
  },
  {
    userID: 101,
    name: 'Michael Jackson',
    dateRecentHired: '2019-12-23',
    hiredFor: 'Lawn Work',
    userRated: '4 stars',
  },
  {
    userID: 102,
    name: 'Marcus Parkinson',
    dateRecentHired: '2019-12-23',
    hiredFor: 'House Cleaning',
    userRated: '5 stars',
  },
  {
    userID: 103,
    name: 'Swiggity Swoggity',
    dateRecentHired: '2019-12-23',
    hiredFor: 'Grass Cutting',
    userRated: '3 stars',
  },
])

function removeFavorite(provider) {
  console.log('provider unfavorited -> ' + provider.name)
  providerArray.value = providerArray.value.filter((p) => p !== provider)
}

</script>

<template>
  <Table>
    <TableCaption>A list of your favorited providers.</TableCaption>
    <TableHeader>
      <TableRow class="**:w-50">
        <TableHead> Provider Names </TableHead>
        <TableHead>Hired For</TableHead>
        <TableHead>Last Hired</TableHead>
        <TableHead>Your Review </TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="provider in providerArray" :key="provider.userID">
        <TableCell class="font-medium">
          {{ provider.name }}
        </TableCell>
        <TableCell>{{ provider.hiredFor }}</TableCell>
        <TableCell>{{ provider.dateRecentHired }}</TableCell>
        <TableCell>{{ provider.userRated }}</TableCell>
        <!-- <TableCell class="text-right"> -->
        <!-- X -->
        <!-- {{ provider.userRated }} -->
        <!-- </TableCell> -->
        <TableCell><Button @click="removeFavorite(provider)" class="hover:bg-destructive hover:text-white"
            variant="outline" size="icon-sm">X</Button></TableCell>
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
  </Table>
</template>
