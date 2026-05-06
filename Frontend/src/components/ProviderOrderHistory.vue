<!-- ProviderOrderHistory.vue -->
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { CheckCircle2, AlertCircle, Phone, Mail } from "lucide-vue-next";

import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import { useOrderHistoryStore } from "@/store/orderHistoryStore";
import { useUserStore } from "@/store/userStore";
import { useReportsStore } from "@/store/reportsStore";
import { storeToRefs } from "pinia";

import Report from "@/components/Report.vue";

const historyStore = useOrderHistoryStore();
const userStore = useUserStore();
const reportsStore = useReportsStore();
const { orders } = storeToRefs(historyStore);

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

const myJobs = computed(() => {
  const myProviderId = userStore.currentUser?.providerId;
  if (!myProviderId) return [];
  return orders.value
    .filter((o) => o.provider?.userID === myProviderId)
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
});

// ===== Mark Complete Dialog =====
const completeDialogOpen = ref(false);
const activeOrder = ref(null);

const completeForm = reactive({
  hoursWorked: "",
  providerComment: "",
});

const completeError = ref("");

const hoursOptions = Array.from({ length: 12 }, (_, i) => String(i + 1));

function openCompleteDialog(order) {
  activeOrder.value = order;
  completeForm.hoursWorked = "";
  completeForm.providerComment = "";
  completeError.value = "";
  completeDialogOpen.value = true;
}

function submitComplete() {
  if (!activeOrder.value) return;
  if (!completeForm.hoursWorked) {
    completeError.value = "Please select the hours worked.";
    return;
  }

  historyStore.markComplete(activeOrder.value.id, {
    hoursWorked: Number(completeForm.hoursWorked),
    providerComment: completeForm.providerComment.trim(),
  });

  completeDialogOpen.value = false;
  activeOrder.value = null;
}

// ===== Customer Contact Dialog =====
const customerDialogOpen = ref(false);
const activeCustomerOrder = ref(null);

function phoneFromCustomerId(customerId) {
  if (!customerId) return "(555) 000-0000";
  // Simple deterministic generator from id string
  let hash = 0;
  for (let i = 0; i < customerId.length; i++) {
    hash = (hash * 31 + customerId.charCodeAt(i)) >>> 0;
  }
  const digits = String(hash).padStart(7, "0").slice(0, 7);
  return `(555) ${digits.slice(0, 3)}-${digits.slice(3, 7)}`;
}

function openCustomerDialog(order) {
  activeCustomerOrder.value = order;
  customerDialogOpen.value = true;
}

const activeCustomerPhone = computed(() => {
  if (!activeCustomerOrder.value) return "";
  return phoneFromCustomerId(activeCustomerOrder.value.customerId);
});

const activeCustomerEmail = computed(() => {
  return activeCustomerOrder.value?.customerEmail || "No email on file";
});

// ===== Report Dialog =====
const reportDialogOpen = ref(false);
const reportOrder = ref(null);

function openReportDialog(order) {
  customerDialogOpen.value = false;
  reportOrder.value = order;
  setTimeout(() => {
    reportDialogOpen.value = true;
  }, 150);
}

function reportButtonLabel(order) {
  return reportsStore.hasReported(order.id, "provider-to-customer")
    ? "View Report"
    : "Report Customer";
}
</script>

<template>
  <div class="flex min-w-200 flex-col items-center">
    <Card class="p-5">
      <Table>
        <TableHeader>
          <TableRow class="**:font-semibold **:text-black">
            <TableHead></TableHead>
            <TableHead class="w-50">Customer</TableHead>
            <TableHead class="w-40">Service</TableHead>
            <TableHead class="w-50">Scheduled</TableHead>
            <TableHead class="w-30">Status</TableHead>
            <TableHead class="w-40">Pay</TableHead>
            <TableHead class="w-32">Action</TableHead>
          </TableRow>
        </TableHeader>

        <tbody>
          <TableRow
            v-for="(order, i) in myJobs"
            :key="order.id"
            class="animate__animated animate__fadeInUp"
            :style="{ animationDelay: `${i * 0.05}s` }"
          >
            <TableCell>
              <button
                class="cursor-pointer transition-transform hover:scale-110"
                @click="openCustomerDialog(order)"
                aria-label="View customer info"
              >
                <Avatar class="scale-[1.3] align-top">
                  <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
                </Avatar>
              </button>
            </TableCell>
            <TableCell>
              <button
                class="cursor-pointer text-left hover:underline"
                @click="openCustomerDialog(order)"
              >
                {{ order.customerName || "Customer" }}
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
                      ((order.hourlyRate ?? 0) * order.hoursWorked).toFixed(2)
                    }}
                  </span>
                  <span class="text-muted-foreground text-xs">
                    {{ order.hoursWorked }}h × ${{
                      (order.hourlyRate ?? 0).toFixed(2)
                    }}/hr
                  </span>
                </div>
              </template>
              <template v-else>
                ${{ (order.hourlyRate ?? 0).toFixed(2) }}/hr
              </template>
            </TableCell>

            <TableCell>
              <Button
                v-if="order.hoursWorked"
                variant="outline"
                size="sm"
                disabled
                class="gap-1"
              >
                <CheckCircle2 class="size-4 text-green-600" />
                Done
              </Button>

              <Button
                v-else-if="statusOf(order) === 'completed'"
                variant="outline"
                size="sm"
                class="hover:bg-green-600 hover:text-white"
                @click="openCompleteDialog(order)"
              >
                Mark Complete
              </Button>

              <span v-else class="text-muted-foreground text-xs">
                Upcoming
              </span>
            </TableCell>
          </TableRow>
        </tbody>

        <TableFooter />
        <TableCaption v-if="myJobs.length">Your booked jobs.</TableCaption>
        <TableCaption v-else>
          No bookings yet. Customers will appear here once they hire you.
        </TableCaption>
      </Table>
    </Card>

    <!-- ===== Mark Complete Dialog ===== -->
    <Dialog v-model:open="completeDialogOpen">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Mark job as complete</DialogTitle>
          <DialogDescription>
            Job for {{ activeOrder?.customerName }} on
            {{ formatDate(activeOrder?.scheduledDate) }}
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-2">
          <div class="space-y-2">
            <label class="text-sm font-medium">Hours worked</label>
            <Select v-model="completeForm.hoursWorked">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select hours (1–12)" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="h in hoursOptions" :key="h" :value="h">
                  {{ h }} {{ h === "1" ? "hour" : "hours" }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div class="space-y-2">
            <label class="text-sm font-medium">
              Note for the customer
              <span class="text-muted-foreground font-normal">(optional)</span>
            </label>
            <Textarea
              v-model="completeForm.providerComment"
              placeholder="Anything the customer should know about the work…"
              class="min-h-24 resize-none"
            />
          </div>

          <p
            v-if="completeError"
            class="text-destructive flex items-center gap-2 text-sm"
          >
            <AlertCircle class="size-4" />
            {{ completeError }}
          </p>

          <div
            v-if="completeForm.hoursWorked && activeOrder"
            class="bg-muted/50 mt-1 space-y-1 rounded-md p-3 text-sm"
          >
            <div class="flex justify-between">
              <span class="text-muted-foreground">Hours</span>
              <span>{{ completeForm.hoursWorked }}h</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Rate</span>
              <span>${{ (activeOrder.hourlyRate ?? 0).toFixed(2) }}/hr</span>
            </div>
            <div class="mt-1 flex justify-between border-t pt-1 font-semibold">
              <span>Total</span>
              <span>
                ${{
                  (
                    (activeOrder.hourlyRate ?? 0) *
                    Number(completeForm.hoursWorked)
                  ).toFixed(2)
                }}
              </span>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" @click="completeDialogOpen = false">
            Cancel
          </Button>
          <Button @click="submitComplete">Confirm</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- ===== Customer Contact Dialog ===== -->
    <Dialog v-model:open="customerDialogOpen">
      <DialogContent class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Customer Info</DialogTitle>
          <DialogDescription>
            Contact details for your booking.
          </DialogDescription>
        </DialogHeader>

        <div v-if="activeCustomerOrder" class="space-y-4 py-2">
          <div class="flex items-center gap-4">
            <Avatar class="scale-[1.3]">
              <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
            </Avatar>
            <div class="flex-1">
              <p class="text-lg font-semibold">
                {{ activeCustomerOrder.customerName }}
              </p>
              <p class="text-muted-foreground text-sm">
                Booked on {{ formatDate(activeCustomerOrder.createdAt) }}
              </p>
            </div>
          </div>

          <Separator />

          <div class="space-y-3">
            <button
              type="button"
              class="hover:bg-muted flex w-full items-center gap-3 rounded-md p-2 text-left transition"
              @click="window.location.href = `tel:${activeCustomerPhone}`"
            >
              <Phone class="text-muted-foreground size-4" />
              <div class="flex flex-col">
                <span class="text-muted-foreground text-xs">Phone</span>
                <span class="font-medium">{{ activeCustomerPhone }}</span>
              </div>
            </button>

            <button
              type="button"
              class="hover:bg-muted flex w-full items-center gap-3 rounded-md p-2 text-left transition"
              @click="window.location.href = `mailto:${activeCustomerEmail}`"
              :disabled="!activeCustomerOrder.customerEmail"
            >
              <Mail class="text-muted-foreground size-4" />
              <div class="flex flex-col">
                <span class="text-muted-foreground text-xs">Email</span>
                <span class="font-medium break-all">
                  {{ activeCustomerEmail }}
                </span>
              </div>
            </button>
          </div>
        </div>

        <DialogFooter class="flex-col gap-2 sm:flex-row sm:justify-end">
          <Button
            v-if="activeCustomerOrder"
            variant="outline"
            class="text-amber-700 hover:bg-amber-50 hover:text-amber-800"
            @click="openReportDialog(activeCustomerOrder)"
          >
            {{ reportButtonLabel(activeCustomerOrder) }}
          </Button>
          <Button variant="outline" @click="customerDialogOpen = false">
            Close
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- ===== Report Dialog ===== -->
    <Report
      v-model:open="reportDialogOpen"
      :order="reportOrder"
      direction="provider-to-customer"
    />
  </div>
</template>

<style scoped></style>
