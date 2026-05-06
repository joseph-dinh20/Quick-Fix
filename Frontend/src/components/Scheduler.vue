<!-- NOTE: Scheduler.vue -->
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
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import { ref, watch, computed } from "vue";
import "vue-toast-notification/dist/theme-sugar.css";
import { useToast } from "vue-toast-notification";

import { useOrderStore } from "@/store/orderStore";
import { useUserStore } from "@/store/userStore";

const orderStore = useOrderStore();
const userStore = useUserStore();
const $toast = useToast();

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
const minDate = todayDate.subtract({ days: 365 });
const selectedTime = ref();
const isOpen = ref(false);
const df = new DateFormatter("en-US", { dateStyle: "long" });

const isComplete = computed(() => selectedDate.value && selectedTime.value);

watch(selectedDate, () => {
  isOpen.value = false;
});

function routeToPayment() {
  // Save schedule data to the order store regardless — survives a login detour
  orderStore.setSelectedProvider(provider);
  orderStore.setSchedule(
    selectedDate.value.toString(),
    selectedTime.value.time,
    selectedTime.value.text,
  );

  // Providers can't book services
  if (userStore.isProvider) {
    $toast.error(
      "Providers can't book services. Please use a customer account.",
    );
    return;
  }

  if (!userStore.isLoggedIn) {
    sessionStorage.setItem("redirectAfterLogin", "/Payment");
    $toast.info("Please log in to continue with your booking.");
    window.location.hash = "#/Login";
    return;
  }

  window.location.hash = "#/Payment";
}
</script>

<template>
  <div class="flex flex-col items-center px-4 py-10">
    <Card class="ring-border/50 w-full max-w-md border-0 shadow-lg ring-1">
      <CardHeader class="pb-2">
        <div
          class="mb-2 flex items-center gap-2 text-sm font-medium text-green-600"
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
        <div class="mt-5 flex items-center gap-5">
          <Avatar class="scale-[1.3]">
            <AvatarImage :src="provider.avatar" alt="provider photo" />
            <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
          </Avatar>
          <span class="text-lg font-semibold">{{ provider.name }}</span>
        </div>
      </CardHeader>

      <CardContent class="flex flex-col gap-6 pt-4">
        <!-- Date -->
        <div class="flex flex-col gap-2">
          <label class="flex items-center gap-2 text-sm font-medium">
            <CalendarIcon class="text-muted-foreground size-4" />
            Date
          </label>
          <Popover v-model:open="isOpen">
            <PopoverTrigger as-child>
              <Button
                variant="outline"
                class="w-full cursor-pointer justify-start font-normal"
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
                :minValue="minDate"
                :numberOfMonths="1"
                initial-focus
              />
              <!-- :minValue="nextDay" -->
            </PopoverContent>
          </Popover>
        </div>

        <!-- Time -->
        <div class="flex flex-col gap-2">
          <label class="flex items-center gap-2 text-sm font-medium">
            <Clock class="text-muted-foreground size-4" />
            Time of day
          </label>
          <Select v-model="selectedTime">
            <SelectTrigger
              class="h-11 w-full cursor-pointer"
              :class="!selectedTime && 'text-muted-foreground'"
            >
              <div class="flex items-center gap-2">
                <CheckCircle2
                  v-if="selectedTime"
                  class="size-4 shrink-0 text-green-500"
                />
                <SelectValue placeholder="Select a time window" />
              </div>
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem
                  v-for="item in timeOfDay"
                  :key="item.time"
                  :value="item"
                  class="cursor-pointer"
                >
                  <span class="font-medium">{{ item.time }}</span>
                  <span class="text-muted-foreground ml-1">
                    ({{ item.text }})
                  </span>
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <CardDescription>
          Your contractor will reach out to you to confirm exact details.
        </CardDescription>
        <Button
          @click="routeToPayment"
          class="w-40 cursor-pointer self-center rounded-3xl"
          :disabled="!isComplete"
        >
          Confirm Schedule
        </Button>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped>
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
