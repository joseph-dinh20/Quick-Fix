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
import { CheckCircle2, AlertCircle } from "lucide-vue-next";

import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import { useOrderHistoryStore } from "@/store/orderHistoryStore";
import { useUserStore } from "@/store/userStore";
import { storeToRefs } from "pinia";

const historyStore = useOrderHistoryStore();
const userStore = useUserStore();
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

// Only orders for the currently logged-in provider
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
              <Avatar class="scale-[1.3] align-top">
                <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
              </Avatar>
            </TableCell>
            <TableCell>
              {{ order.customerName || "Customer" }}
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

            <!-- Pay column -->
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

            <!-- Action column -->
            <TableCell>
              <!-- Already completed -->
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

              <!-- Completed (past date) but not yet marked -->
              <Button
                v-else-if="statusOf(order) === 'completed'"
                variant="outline"
                size="sm"
                class="hover:bg-green-600 hover:text-white"
                @click="openCompleteDialog(order)"
              >
                Mark Complete
              </Button>

              <!-- Scheduled (upcoming) — nothing to do yet -->
              <span v-else class="text-muted-foreground text-xs">
                Upcoming
              </span>
            </TableCell>
          </TableRow>
        </tbody>

        <TableFooter />
        <TableCaption v-if="myJobs.length"> Your booked jobs. </TableCaption>
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
            class="bg-muted/50 space-y-1 rounded-md p-3 text-sm"
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
  </div>
</template>

<style scoped></style>
