<!-- Report.vue -->
<script setup>
import { ref, reactive, computed, watch } from "vue";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { AlertCircle, ShieldAlert } from "lucide-vue-next";

import { useReportsStore } from "@/store/reportsStore";
import { useUserStore } from "@/store/userStore";
import { useToast } from "vue-toast-notification";

const props = defineProps({
  open: { type: Boolean, default: false },
  order: { type: Object, default: null },
  // "customer-to-provider" or "provider-to-customer"
  direction: { type: String, required: true },
});

const emit = defineEmits(["update:open"]);

const reportsStore = useReportsStore();
const userStore = useUserStore();
const $toast = useToast();

const reasonOptionsByDirection = {
  "customer-to-provider": [
    "No-show",
    "Poor work quality",
    "Inappropriate behavior",
    "Damaged property",
    "Scam",
    "Other",
  ],
  "provider-to-customer": [
    "No-show",
    "Inappropriate behavior",
    "Unsafe location",
    "Refused payment",
    "Other",
  ],
};

const reasonOptions = computed(
  () => reasonOptionsByDirection[props.direction] || [],
);

const form = reactive({
  reason: "",
  description: "",
});

const error = ref("");

// Existing report (if any) — shown read-only
const existingReport = computed(() => {
  if (!props.order) return null;
  return reportsStore.getReport(props.order.id, props.direction);
});

const isReadOnly = computed(() => !!existingReport.value);

// Reset / hydrate the form whenever the dialog opens
watch(
  () => props.open,
  (open) => {
    if (!open) return;
    error.value = "";
    if (existingReport.value) {
      form.reason = existingReport.value.reason;
      form.description = existingReport.value.description;
    } else {
      form.reason = "";
      form.description = "";
    }
  },
);

function formatDate(date) {
  if (!date) return "—";
  const d = date.includes("T") ? new Date(date) : new Date(date + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

const reportedTitle = computed(() => {
  if (props.direction === "customer-to-provider") return "Report Provider";
  return "Report Customer";
});

const reportedNameInOrder = computed(() => {
  if (!props.order) return "";
  if (props.direction === "customer-to-provider") {
    return props.order.provider?.name || "";
  }
  return props.order.customerName || "";
});

function handleSubmit() {
  if (isReadOnly.value) return;
  if (!form.reason) {
    error.value = "Please select a reason.";
    return;
  }
  if (form.description.trim().length < 20) {
    error.value = "Description must be at least 20 characters.";
    return;
  }

  const order = props.order;
  const reporter = userStore.currentUser;

  let reportedId, reportedName;
  if (props.direction === "customer-to-provider") {
    reportedId = order.provider?.userID;
    reportedName = order.provider?.name;
  } else {
    reportedId = order.customerId;
    reportedName = order.customerName;
  }

  const success = reportsStore.addReport(order.id, props.direction, {
    reason: form.reason,
    description: form.description.trim(),
    reporterId: reporter?.id,
    reporterName: reporter?.name,
    reportedId,
    reportedName,
  });

  if (!success) {
    error.value = "A report for this booking has already been submitted.";
    return;
  }

  $toast.success("Report submitted. Thank you for letting us know.");
  emit("update:open", false);
}

function handleClose() {
  emit("update:open", false);
}
</script>

<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2">
          <ShieldAlert class="size-5 text-amber-600" />
          {{ reportedTitle }}
        </DialogTitle>
        <DialogDescription v-if="!isReadOnly">
          Reports are confidential. Submit one report per booking.
        </DialogDescription>
        <DialogDescription v-else>
          You already submitted a report for this booking. Reports cannot be
          modified.
        </DialogDescription>
      </DialogHeader>

      <div v-if="order" class="space-y-4 py-2">
        <!-- Order context -->
        <div class="bg-muted/50 space-y-2 rounded-md p-3 text-sm">
          <div class="flex justify-between">
            <span class="text-muted-foreground">Reported user</span>
            <span class="font-medium">{{ reportedNameInOrder }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-muted-foreground">Service</span>
            <Badge variant="outline" class="bg-green-600 text-white">
              {{ order.serviceCategory || "Service" }}
            </Badge>
          </div>
          <div class="flex justify-between">
            <span class="text-muted-foreground">Scheduled</span>
            <span>{{ formatDate(order.scheduledDate) }}</span>
          </div>
        </div>

        <!-- Reason -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Reason</label>
          <Select v-model="form.reason" :disabled="isReadOnly">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a reason" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="r in reasonOptions" :key="r" :value="r">
                {{ r }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Description -->
        <div class="space-y-2">
          <label class="text-sm font-medium">
            Description
            <span class="text-muted-foreground text-xs">
              (at least 20 characters)
            </span>
          </label>
          <Textarea
            v-model="form.description"
            :disabled="isReadOnly"
            placeholder="Tell us what happened so we can investigate…"
            class="min-h-32 resize-none"
          />
        </div>

        <p
          v-if="error"
          class="text-destructive flex items-center gap-2 text-sm"
        >
          <AlertCircle class="size-4" />
          {{ error }}
        </p>

        <Separator v-if="isReadOnly" />

        <p v-if="isReadOnly" class="text-muted-foreground text-xs">
          Submitted on {{ formatDate(existingReport?.createdAt) }}
        </p>
      </div>

      <DialogFooter>
        <Button variant="outline" @click="handleClose">Close</Button>
        <Button v-if="!isReadOnly" @click="handleSubmit">
          Submit report
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
