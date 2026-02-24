<script setup>
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

import { ref, computed } from 'vue'
//NOTE: item-per-page='5' means to show 5 items per page
// so if :total is 10 then there will only be 2 pages.
// <-- previous 1, 2, ... next --->
// :default-page is setting by default when user loads the component in,
// at what page do you want the user to be at.

// Example comments (replace with your real data)
const comments = ref(
  Array.from({ length: 25 }, (_, i) => ({
    id: i + 1,
    author: `User ${i + 1}`,
    body: `This is comment #${i + 1}`,
  }))
)

const perPage = 5
const total = computed(() => comments.value.length)
console.log(total.value)

</script>
<template>
  <Pagination v-slot="{ page }" :items-per-page="perPage" :total="total" :default-page="1">
    <!-- Paginated content -->
    <ul class="space-y-3 mb-4">
      <li v-for="comment in comments.slice((page - 1) * perPage, page * perPage)" :key="comment.id"
        class="rounded border p-3">
        <div class="font-medium">{{ comment.author }}</div>
        <div class="text-sm opacity-80">{{ comment.body }}</div>
      </li>
    </ul>

    <!-- Pagination controls -->
    <PaginationContent v-slot="{ items }">
      <PaginationPrevious />

      <template v-for="(item, index) in items" :key="index">
        <PaginationItem v-if="item.type === 'page'" :value="item.value" :is-active="item.value === page">
          {{ item.value }}
        </PaginationItem>
      </template>

      <PaginationEllipsis :index="4" />
      <PaginationNext />
    </PaginationContent>
  </Pagination>
</template>
