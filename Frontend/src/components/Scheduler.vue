<!-- Scheduler.vue -->
<script setup>
import {
  DateFormatter,
  getLocalTimeZone,
  today,
} from "@internationalized/date";
import { CalendarIcon, Clock, CheckCircle2 } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";
import { ref, watch, computed } from "vue";

const { provider } = defineProps(["provider"]);

const todayDate = today(getLocalTimeZone());
const nextDay = todayDate.add({ days: 1 });
const selectedDate = ref();
const timeOfDay = [
  { time: "Morning", text: "6:00 AM – 10:00 AM" },
  { time: "Midday", text: "10:00 AM – 2:00 PM" },
  { time: "Afternoon", text: "2:00 PM – 6:00 PM" },
  { time: "Evening", text: "6:00 PM – 9:00 PM" },
];
const selectedTime = ref();
const isOpen = ref(false);
const df = new DateFormatter("en-US", {
  dateStyle: "long",
});

const isComplete = computed(() => selectedDate.value && selectedTime.value);

watch(selectedDate, () => {
  isOpen.value = false;
});

function routeToPayment() {
  window.location.hash = "#/Payment";
}
</script>

<template>
  <div class="flex flex-col items-center py-10 px-4">
    <Card class="w-full max-w-md shadow-lg border-0 ring-1 ring-border/50">
      <CardHeader class="pb-2">
        <div
          class="flex items-center gap-2 text-green-600 text-sm font-medium mb-2"
        >
          <CalendarIcon class="size-4" />
          Scheduling
        </div>
        <CardTitle class="text-xl font-semibold tracking-tight">
          Select date & time
        </CardTitle>
        <CardDescription>
          Choose when you'd like the contractor to arrive.
        </CardDescription>
      </CardHeader>

      <CardContent class="flex flex-col gap-6 pt-4">
        <!-- Date -->
        <div class="flex flex-col gap-2">
          <label class="text-sm font-medium flex items-center gap-2">
            <CalendarIcon class="size-4 text-muted-foreground" />
            Date
          </label>
          <Popover v-model:open="isOpen">
            <PopoverTrigger as-child>
              <Button
                variant="outline"
                class="cursor-pointer w-full justify-start font-normal"
                :class="!selectedDate && 'text-muted-foreground'"
              >
                <CheckCircle2
                  v-if="selectedDate"
                  class="size-4 text-green-500"
                />
                {{
                  selectedDate
                    ? df.format(selectedDate.toDate(getLocalTimeZone()))
                    : "Select a date"
                }}
              </Button>
            </PopoverTrigger>
            <PopoverContent class="w-auto p-0" align="start">
              <Calendar
                class="cursor-pointer"
                v-model="selectedDate"
                :default-placeholder="todayDate"
                layout="month-and-year"
                :minValue="nextDay"
                :numberOfMonths="1"
                initial-focus
              />
            </PopoverContent>
          </Popover>
        </div>

        <!-- Time -->
        <div class="flex flex-col gap-2">
          <label class="text-sm font-medium flex items-center gap-2">
            <Clock class="size-4 text-muted-foreground" />
            Time of day
          </label>
          <Select v-model="selectedTime">
            <SelectTrigger
              class="cursor-pointer w-full h-11"
              :class="!selectedTime && 'text-muted-foreground'"
            >
              <div class="flex items-center gap-2">
                <CheckCircle2
                  v-if="selectedTime"
                  class="size-4 text-green-500 shrink-0"
                />
                <SelectValue placeholder="Select a time window" />
              </div>
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem
                  v-for="item in timeOfDay"
                  :key="item.time"
                  :value="item.time"
                  class="cursor-pointer"
                >
                  <span class="font-medium">{{ item.time }}</span>
                  <span class="text-muted-foreground ml-1">
                    ({{ item.text }})</span
                  >
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <!-- Confirm -->
        <CardDescription>
          Your contractor will reach out to you to confirm exact details.
        </CardDescription>
        <Button
          @click="routeToPayment"
          class="cursor-pointer rounded-3xl w-40 self-center"
          :disabled="!isComplete"
        >
          Confirm Schedule
        </Button>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped>
/* NOTE: This is needed to disable the default behavior of ui/Calendar component feature */
:deep([data-today]:not([data-selected])) {
  background: transparent;
}

:deep([data-calendar-cell]:not([data-disabled])) {
  cursor: pointer;
}

:deep([data-disabled]) {
  cursor: not-allowed;
}
</style>
