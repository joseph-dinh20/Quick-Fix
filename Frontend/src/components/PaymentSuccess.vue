<!-- PaymentSuccess.vue -->
<script setup>
import { computed } from "vue";
import { Card, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { CheckCircle2, CalendarIcon, Clock, MapPin } from "lucide-vue-next";
import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import { useOrderHistoryStore } from "@/store/orderHistoryStore";
import { storeToRefs } from "pinia";

const historyStore = useOrderHistoryStore();
const { orders } = storeToRefs(historyStore);

const confirmationId = computed(() => {
  const hash = window.location.hash;
  const match = hash.match(/[?&]id=([^&]+)/);
  return match ? match[1] : null;
});

const order = computed(() => {
  if (!confirmationId.value) return orders.value[0];
  return orders.value.find((o) => o.confirmationId === confirmationId.value);
});

const formattedDate = computed(() => {
  if (!order.value?.scheduledDate) return "—";
  return new Date(order.value.scheduledDate + "T00:00:00").toLocaleDateString(
    "en-US",
    { dateStyle: "long" },
  );
});

function goHome() {
  window.location.hash = "/";
}
function goToOrders() {
  window.location.hash = "/OrderHistory";
}
</script>

<template>
  <div class="m-10 flex justify-center">
    <Card
      v-if="order"
      class="animate__animated animate__fadeInUp w-[28rem] rounded-3xl border-2 p-8"
    >
      <div class="flex flex-col items-center gap-3">
        <CheckCircle2
          class="animate__animated animate__bounceIn size-16 text-green-600"
        />
        <CardTitle class="text-2xl">Payment Confirmed</CardTitle>
        <p class="text-muted-foreground text-center text-sm">
          Your booking is scheduled. We've sent the details to your account.
        </p>
        <p class="text-muted-foreground text-xs">
          Confirmation #
          <span class="text-foreground font-mono font-semibold">
            {{ order.confirmationId }}
          </span>
        </p>
      </div>

      <Separator class="my-6" />

      <div class="flex items-center gap-3">
        <Avatar>
          <AvatarImage :src="order.provider.avatar" />
          <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
        </Avatar>
        <div>
          <p class="font-medium">{{ order.provider.name }}</p>
          <p class="text-muted-foreground text-xs">
            {{ order.provider.hiredFor }}
          </p>
        </div>
      </div>

      <Separator class="my-6" />

      <div class="flex flex-col gap-3 text-sm">
        <div class="flex items-center gap-2">
          <CalendarIcon class="text-muted-foreground size-4" />
          <span>{{ formattedDate }}</span>
        </div>
        <div class="flex items-center gap-2">
          <Clock class="text-muted-foreground size-4" />
          <span>{{ order.scheduledTime }} {{ order.scheduledTimeText }}</span>
        </div>
        <div class="flex items-start gap-2">
          <MapPin class="text-muted-foreground mt-0.5 size-4 shrink-0" />
          <span class="break-words">
            {{ order.address
            }}{{ order.apartment ? `, ${order.apartment}` : "" }}
          </span>
        </div>
      </div>

      <Separator class="my-6" />

      <div class="flex flex-col gap-2 text-sm">
        <div class="flex justify-between">
          <span class="text-muted-foreground">Job size</span>
          <span class="font-medium">{{ order.planLabel }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-muted-foreground">Paying With</span>
          <span class="font-medium">•••• {{ order.last4 }}</span>
        </div>
        <div class="mt-2 flex justify-between text-base font-semibold">
          <span>Per hour charge</span>
          <span>${{ order.hourlyRate.toFixed(2) }}/hr</span>
        </div>
      </div>

      <div class="mt-8 flex gap-2">
        <Button class="flex-1" @click="goToOrders">View Orders</Button>
        <Button variant="outline" class="flex-1" @click="goHome">
          Back to Home
        </Button>
      </div>
    </Card>

    <Card v-else class="p-8 text-center">
      <p class="text-muted-foreground">No order found.</p>
      <Button class="mt-4" @click="goHome">Back to Home</Button>
    </Card>
  </div>
</template>
