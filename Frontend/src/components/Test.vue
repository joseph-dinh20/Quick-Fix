<script setup>
// import type { DateValue } from '@internationalized/date'
import { getLocalTimeZone, today } from '@internationalized/date'
import { Calendar } from '@/components/ui/calendar'
import { ref } from 'vue'

// const date = ref(today(getLocalTimeZone())) as Ref<DateValue>
const date = ref(today(getLocalTimeZone()))
const defaultPlaceholder = today(getLocalTimeZone())
</script>

<template>
  <Calendar v-model="date" :default-placeholder="defaultPlaceholder" weekday-format="short"
    class="rounded-md border shadow-sm **:data-[slot=calendar-cell-trigger]:size-12!">
    <template #calendar-heading="{ date, month }">
      <div class="flex gap-2 items-center">
        <div>
          Custom heading
        </div>
        <component :is="month" :date="date" />
      </div>
    </template>
  </Calendar>
</template>
