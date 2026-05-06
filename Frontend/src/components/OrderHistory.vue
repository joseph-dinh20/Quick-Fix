<!-- OrderHistory.vue -->
<script setup>
import { computed, ref, reactive } from "vue";
import { Card } from "@/components/ui/card";
import {
  Table,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Star, AlertCircle, Phone, Mail } from "lucide-vue-next";

import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import starIcon from "@/assets/icons/star.png";
import { useOrderHistoryStore } from "@/store/orderHistoryStore";
import { useProviderRatingsStore } from "@/store/providerRatingsStore";
import { useProviderProfileStore } from "@/store/providerProfileStore";
import { useUserStore } from "@/store/userStore";
import { useReportsStore } from "@/store/reportsStore";
import { storeToRefs } from "pinia";

import Provider from "@/components/Provider.vue";
import Report from "@/components/Report.vue";

const historyStore = useOrderHistoryStore();
const ratingsStore = useProviderRatingsStore();
const providerProfileStore = useProviderProfileStore();
const userStore = useUserStore();
const reportsStore = useReportsStore();
const { orders } = storeToRefs(historyStore);

const removingId = ref(null);

function formatDate(date) {
  if (!date) return "—";
  const d = date.includes("T") ? new Date(date) : new Date(date + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function statusOf(order) {
  if (!order.scheduledDate) return "scheduled";
  const apptDate = new Date(order.scheduledDate + "T00:00:00");
  return apptDate >= new Date(new Date().toDateString())
    ? "scheduled"
    : "completed";
}

function hoursUntil(order) {
  if (!order.scheduledDate) return Infinity;
  const appt = new Date(order.scheduledDate + "T00:00:00").getTime();
  return (appt - Date.now()) / (1000 * 60 * 60);
}

function isCancelLocked(order) {
  // return hoursUntil(order) < 48; //cannot cancel within 48 hours of booking time left
  return hoursUntil(order) < -10000; //enabled for testing and cancel at any time
}

const sortedOrders = computed(() =>
  [...orders.value].sort(
    (a, b) => new Date(b.createdAt) - new Date(a.createdAt),
  ),
);

// ===== Cancel flow =====
function cancelOrder(order) {
  removingId.value = order.id;
  setTimeout(() => {
    historyStore.removeOrder(order.id);
    removingId.value = null;
  }, 500);
}

// ===== Rating flow =====
const rateDialogOpen = ref(false);
const viewRatingDialogOpen = ref(false);
const activeOrder = ref(null);

const rateForm = reactive({
  userRated: 0,
  userComment: "",
});

const rateError = ref("");

function openRateDialog(order) {
  activeOrder.value = order;
  rateForm.userRated = 0;
  rateForm.userComment = "";
  rateError.value = "";
  rateDialogOpen.value = true;
}

function openViewRatingDialog(order) {
  activeOrder.value = order;
  viewRatingDialogOpen.value = true;
}

function submitRating() {
  if (!activeOrder.value) return;
  if (rateForm.userRated < 1 || rateForm.userRated > 5) {
    rateError.value = "Please select a star rating.";
    return;
  }
  if (!rateForm.userComment.trim()) {
    rateError.value = "Please leave a short comment.";
    return;
  }

  const order = activeOrder.value;
  const rating = {
    jobType: order.provider?.hiredFor || "Service",
    userName: userStore.currentUser?.name || "Anonymous",
    date: new Date().toISOString(),
    userAvatar: "/assets/avatars/defaultAvatar.png",
    userRated: rateForm.userRated,
    userComment: rateForm.userComment.trim(),
  };

  const providerId = order.provider?.userID;
  if (providerId) {
    ratingsStore.addRating(providerId, rating);
  }

  historyStore.markAsRated(order.id, {
    userRated: rateForm.userRated,
    userComment: rateForm.userComment.trim(),
  });

  rateDialogOpen.value = false;
  activeOrder.value = null;
}

// ===== Provider info dialog =====
const providerDialogOpen = ref(false);
const fullProfileOpen = ref(false);
const activeProvider = ref(null);
const activeProviderOrder = ref(null);

function phoneFromProviderId(providerId) {
  if (!providerId) return "(555) 000-0000";
  const id = String(providerId).padStart(7, "0");
  const digits = (id + "0000000").slice(0, 7);
  return `(555) ${digits.slice(0, 3)}-${digits.slice(3, 7)}`;
}

function emailFromName(name) {
  if (!name) return "provider@quickfix.com";
  return name.replace(/[^a-zA-Z]/g, "").toLowerCase() + "@quickfix.com";
}

function openProviderDialog(order) {
  const providerId = order.provider?.userID;
  if (!providerId) return;

  const merged = providerProfileStore.getMergedProvider(providerId);
  activeProvider.value = merged || order.provider;
  activeProviderOrder.value = order;
  providerDialogOpen.value = true;
}

function openFullProfile() {
  providerDialogOpen.value = false;
  setTimeout(() => {
    fullProfileOpen.value = true;
  }, 150);
}

const activeProviderPhone = computed(() => {
  if (!activeProvider.value) return "";
  return phoneFromProviderId(activeProvider.value.userID);
});

const activeProviderEmail = computed(() => {
  if (!activeProvider.value) return "";
  return emailFromName(activeProvider.value.name);
});

// Live-merged rating for the contact dialog
const activeProviderAverage = computed(() => {
  if (!activeProvider.value) return "—";
  return ratingsStore.getAverageFor(activeProvider.value.userID) || "—";
});

const activeProviderReviewCount = computed(() => {
  if (!activeProvider.value) return 0;
  return ratingsStore.getRatingsFor(activeProvider.value.userID).length;
});

// ===== Report flow =====
const reportDialogOpen = ref(false);
const reportOrder = ref(null);

function openReportDialog(order) {
  // Close the contact dialog first so they don't stack
  providerDialogOpen.value = false;
  reportOrder.value = order;
  setTimeout(() => {
    reportDialogOpen.value = true;
  }, 150);
}

function reportButtonLabel(order) {
  return reportsStore.hasReported(order.id, "customer-to-provider")
    ? "View Report"
    : "Report Provider";
}
</script>

<template>
  <div class="flex min-w-200 flex-col items-center">
    <Card class="p-5">
      <Table>
        <TableHeader>
          <TableRow class="**:font-semibold **:text-black">
            <TableHead></TableHead>
            <TableHead class="w-50">Provider</TableHead>
            <TableHead class="w-50">Service</TableHead>
            <TableHead class="w-50">Scheduled</TableHead>
            <TableHead class="w-30">Status</TableHead>
            <TableHead class="w-30">Hourly Rate</TableHead>
            <TableHead class="w-32">Action</TableHead>
          </TableRow>
        </TableHeader>

        <TransitionGroup name="order" tag="tbody">
          <TableRow
            v-for="(order, i) in sortedOrders"
            :key="order.id"
            :class="[
              'animate__animated',
              removingId === order.id
                ? 'animate__fadeOutUp animate__fast'
                : 'animate__fadeInUp',
            ]"
            :style="{ animationDelay: `${i * 0.05}s` }"
          >
            <TableCell>
              <button
                class="cursor-pointer transition-transform hover:scale-110"
                @click="openProviderDialog(order)"
                aria-label="View provider info"
              >
                <Avatar class="scale-[1.3] align-top">
                  <AvatarImage :src="order.provider?.avatar" />
                  <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
                </Avatar>
              </button>
            </TableCell>

            <TableCell>
              <button
                class="cursor-pointer text-left hover:underline"
                @click="openProviderDialog(order)"
              >
                {{ order.provider?.name }}
              </button>
            </TableCell>

            <TableCell>
              <Badge
                variant="outline"
                class="scale-[1.1] bg-green-600 text-white"
              >
                {{ order.serviceCategory || "Service" }}
              </Badge>
            </TableCell>

            <TableCell>
              <div class="flex flex-col">
                <span>{{ formatDate(order.scheduledDate) }}</span>
                <span class="text-muted-foreground text-xs">
                  {{ order.scheduledTime }} {{ order.scheduledTimeText }}
                </span>
              </div>
            </TableCell>

            <TableCell>
              <Badge
                variant="outline"
                :class="
                  statusOf(order) === 'scheduled'
                    ? 'scale-[1.1] bg-blue-600 text-white'
                    : 'scale-[1.1] bg-gray-500 text-white'
                "
              >
                {{ statusOf(order) }}
              </Badge>
            </TableCell>

            <TableCell class="font-medium">
              <template v-if="order.hoursWorked">
                <div class="flex flex-col">
                  <span>
                    ${{
                      (
                        (order.hourlyRate ?? 0) * order.hoursWorked +
                        (order.serviceFee ?? 0)
                      ).toFixed(2)
                    }}
                  </span>
                  <span class="text-muted-foreground text-xs">
                    Total paid ({{ order.hoursWorked }}h)
                  </span>
                </div>
              </template>
              <template v-else>
                ${{ (order.hourlyRate ?? 0).toFixed(2) }}/hr
              </template>
            </TableCell>

            <TableCell>
              <template v-if="statusOf(order) === 'scheduled'">
                <HoverCard v-if="isCancelLocked(order)" :open-delay="100">
                  <HoverCardTrigger as-child>
                    <span class="inline-block">
                      <Button
                        variant="outline"
                        size="sm"
                        disabled
                        class="cursor-not-allowed opacity-50"
                      >
                        Cancel
                      </Button>
                    </span>
                  </HoverCardTrigger>
                  <HoverCardContent class="w-72">
                    <div class="flex gap-2">
                      <AlertCircle class="size-5 shrink-0 text-amber-600" />
                      <div class="space-y-1">
                        <p class="text-sm font-semibold">Cancellation locked</p>
                        <p class="text-muted-foreground text-xs">
                          You can no longer cancel this booking — the
                          appointment is within 48 hours. This protects
                          providers from last-minute cancellations.
                        </p>
                      </div>
                    </div>
                  </HoverCardContent>
                </HoverCard>

                <AlertDialog v-else>
                  <AlertDialogTrigger as-child>
                    <Button
                      variant="outline"
                      size="sm"
                      class="hover:bg-destructive hover:text-white"
                    >
                      Cancel
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Cancel this booking?</AlertDialogTitle>
                      <AlertDialogDescription>
                        You're about to cancel your appointment with
                        <span class="text-foreground font-medium">
                          {{ order.provider?.name }}
                        </span>
                        on
                        <span class="text-foreground font-medium">
                          {{ formatDate(order.scheduledDate) }}
                        </span>
                        ({{ order.scheduledTime }}). This action cannot be
                        undone.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Keep booking</AlertDialogCancel>
                      <AlertDialogAction
                        class="bg-destructive hover:bg-destructive/90 text-white"
                        @click="cancelOrder(order)"
                      >
                        Yes, cancel
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </template>

              <template v-else>
                <Button
                  v-if="!order.userRated"
                  variant="outline"
                  size="sm"
                  class="hover:bg-yellow-500 hover:text-white"
                  @click="openRateDialog(order)"
                >
                  <Star class="size-4" />
                  Rate
                </Button>
                <Button
                  v-else
                  variant="outline"
                  size="sm"
                  class="gap-1"
                  @click="openViewRatingDialog(order)"
                >
                  <Star class="size-4 fill-yellow-500 text-yellow-500" />
                  {{ order.userRated }}
                </Button>
              </template>
            </TableCell>
          </TableRow>
        </TransitionGroup>

        <TableFooter />
        <TableCaption v-if="sortedOrders.length">
          Your booking history.
        </TableCaption>
        <TableCaption v-else>
          You haven't booked any services yet.
        </TableCaption>
      </Table>
    </Card>

    <!-- ===== Provider Contact Dialog ===== -->
    <Dialog v-model:open="providerDialogOpen">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Provider Info</DialogTitle>
          <DialogDescription>
            Contact details and quick stats for your booked provider.
          </DialogDescription>
        </DialogHeader>

        <div v-if="activeProvider" class="space-y-4 py-2">
          <div class="flex items-center gap-4">
            <Avatar class="scale-[1.3]">
              <AvatarImage :src="activeProvider.avatar" />
              <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
            </Avatar>
            <div class="flex-1">
              <p class="text-lg font-semibold">{{ activeProvider.name }}</p>
              <p class="text-muted-foreground text-sm">
                ${{ (activeProvider.price ?? 0).toFixed(2) }}/hr
              </p>
            </div>
            <Badge variant="outline">
              <img class="inline-block w-4 align-top" :src="starIcon" />
              {{ activeProviderAverage }}
              ({{ activeProviderReviewCount }})
            </Badge>
          </div>

          <Separator />

          <div class="space-y-3">
            <button
              type="button"
              class="hover:bg-muted flex w-full items-center gap-3 rounded-md p-2 text-left transition"
              @click="window.location.href = `tel:${activeProviderPhone}`"
            >
              <Phone class="text-muted-foreground size-4" />
              <div class="flex flex-col">
                <span class="text-muted-foreground text-xs">Phone</span>
                <span class="font-medium">{{ activeProviderPhone }}</span>
              </div>
            </button>

            <button
              type="button"
              class="hover:bg-muted flex w-full items-center gap-3 rounded-md p-2 text-left transition"
              @click="window.location.href = `mailto:${activeProviderEmail}`"
            >
              <Mail class="text-muted-foreground size-4" />
              <div class="flex flex-col">
                <span class="text-muted-foreground text-xs">Email</span>
                <span class="font-medium break-all">
                  {{ activeProviderEmail }}
                </span>
              </div>
            </button>
          </div>
        </div>

        <DialogFooter class="flex-col gap-2 sm:flex-row sm:justify-end">
          <Button
            v-if="activeProviderOrder"
            variant="outline"
            class="text-amber-700 hover:bg-amber-50 hover:text-amber-800"
            @click="openReportDialog(activeProviderOrder)"
          >
            {{ reportButtonLabel(activeProviderOrder) }}
          </Button>
          <Button variant="outline" @click="providerDialogOpen = false">
            Close
          </Button>
          <Button @click="openFullProfile">View Full Profile</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- ===== Full Provider Profile Dialog ===== -->
    <Dialog v-model:open="fullProfileOpen">
      <DialogContent class="m-0 h-full max-h-95/100 max-w-150 gap-0 p-0">
        <DialogHeader class="sr-only">
          <DialogTitle>Provider Profile</DialogTitle>
          <DialogDescription>Full profile details</DialogDescription>
        </DialogHeader>
        <ScrollArea class="h-full max-h-full">
          <div class="p-4">
            <Provider v-if="activeProvider" :provider="activeProvider" />
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>

    <!-- ===== Rate Provider Dialog ===== -->
    <Dialog v-model:open="rateDialogOpen">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Rate your experience</DialogTitle>
          <DialogDescription>
            How was your service with {{ activeOrder?.provider?.name }}? Ratings
            are final and can't be changed once submitted.
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-2">
          <div class="flex items-center justify-center gap-1">
            <button
              v-for="n in 5"
              :key="n"
              type="button"
              class="transition-transform hover:scale-110"
              @click="rateForm.userRated = n"
            >
              <Star
                class="size-9"
                :class="
                  n <= rateForm.userRated
                    ? 'fill-yellow-500 text-yellow-500'
                    : 'text-muted-foreground'
                "
              />
            </button>
          </div>

          <div class="space-y-2">
            <label class="text-sm font-medium">Leave a comment</label>
            <Textarea
              v-model="rateForm.userComment"
              placeholder="Tell others how it went…"
              class="min-h-24 resize-none"
            />
          </div>

          <p
            v-if="rateError"
            class="text-destructive flex items-center gap-2 text-sm"
          >
            <AlertCircle class="size-4" />
            {{ rateError }}
          </p>
        </div>

        <DialogFooter>
          <Button variant="outline" @click="rateDialogOpen = false">
            Cancel
          </Button>
          <Button @click="submitRating">Submit rating</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- ===== View Rating Dialog (already-rated orders) ===== -->
    <Dialog v-model:open="viewRatingDialogOpen">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Your rating</DialogTitle>
          <DialogDescription>
            For {{ activeOrder?.provider?.name }} —
            {{ formatDate(activeOrder?.scheduledDate) }}
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-2">
          <div class="flex items-center justify-center gap-1">
            <Star
              v-for="n in 5"
              :key="n"
              class="size-7"
              :class="
                n <= (activeOrder?.userRated || 0)
                  ? 'fill-yellow-500 text-yellow-500'
                  : 'text-muted-foreground'
              "
            />
          </div>

          <div class="bg-muted/50 rounded-md p-3 text-sm">
            {{ activeOrder?.userComment || "(no comment)" }}
          </div>
        </div>

        <DialogFooter>
          <Button @click="viewRatingDialogOpen = false">Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- ===== Report Dialog ===== -->
    <Report
      v-model:open="reportDialogOpen"
      :order="reportOrder"
      direction="customer-to-provider"
    />
  </div>
</template>

<style scoped>
.order-move {
  transition: transform 0.4s ease;
}
</style>
