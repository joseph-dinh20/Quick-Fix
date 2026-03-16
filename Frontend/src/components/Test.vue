<script setup>
// import type { DateValue } from '@internationalized/date'
import { DateFormatter, getLocalTimeZone, today } from '@internationalized/date'

import { CalendarIcon } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

import { ref } from 'vue'

const defaultPlaceholder = today(getLocalTimeZone())
const date = ref()
const df = new DateFormatter('en-US', {
  dateStyle: 'long',
})

const selectedDate = () => {
  console.log(date.value)
}
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button>
        Schedule
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-auto p-0" align="start">
      <Calendar v-model="date" :default-placeholder="defaultPlaceholder" layout="month-and-year" initial-focus
        @click="selectedDate" />
      <p>{{ date }}</p>
    </PopoverContent>
  </Popover>
</template>
