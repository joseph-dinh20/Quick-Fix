<!-- NOTE: Payment.vue -->
<script setup>
import { ref, reactive, computed } from "vue";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import { CalendarIcon, Clock, AlertCircle } from "lucide-vue-next";

import { useOrderStore } from "@/store/orderStore";
import { useOrderHistoryStore } from "@/store/orderHistoryStore";
import { storeToRefs } from "pinia";
import { useUserStore } from "@/store/userStore";

const serviceFee = 10;

const orderStore = useOrderStore();
const userStore = useUserStore();
const historyStore = useOrderHistoryStore();
const {
  selectedProvider,
  scheduledDate,
  scheduledTime,
  scheduledTimeText,
  address,
  apartment,
  plan,
  description,
} = storeToRefs(orderStore);

const formattedDate = computed(() => {
  if (!scheduledDate.value) return "Not selected";
  return new Date(scheduledDate.value + "T00:00:00").toLocaleDateString(
    "en-US",
    { dateStyle: "long" },
  );
});

const planLabel = computed(() => {
  const labels = {
    small: "Small (1 hour)",
    medium: "Medium (2–3 hours)",
    large: "Large (4+ hours)",
  };
  return labels[plan.value] || plan.value;
});

// ===== Form state =====
const form = reactive({
  cardholder: "",
  cardNumber: "",
  expMonth: "",
  expYear: "",
  cvv: "",
  comments: "",
});

const errors = reactive({
  cardholder: "",
  cardNumber: "",
  expMonth: "",
  expYear: "",
  cvv: "",
});

const submitError = ref("");
const loading = ref(false);

// ===== Luhn algorithm =====
function luhnCheck(num) {
  const digits = num.replace(/\s/g, "").split("").reverse().map(Number);
  const sum = digits.reduce((acc, d, i) => {
    if (i % 2 === 1) {
      const doubled = d * 2;
      return acc + (doubled > 9 ? doubled - 9 : doubled);
    }
    return acc + d;
  }, 0);
  return sum % 10 === 0;
}

// ===== Zod schemas =====
const cardholderSchema = z
  .string()
  .trim()
  .min(2, "Please enter the cardholder's full name")
  .max(60, "Name is too long")
  .regex(/^[a-zA-Z\s'-]+$/, "Name can only contain letters");

const cardNumberSchema = z
  .string()
  .transform((v) => v.replace(/\s/g, ""))
  .pipe(
    z
      .string()
      .regex(/^\d+$/, "Card number must contain only digits")
      .min(13, "Card number is too short")
      .max(19, "Card number is too long")
      .refine(luhnCheck, "Invalid card number"),
  );

const expMonthSchema = z
  .string()
  .min(1, "Required")
  .regex(/^(0[1-9]|1[0-2])$/, "Invalid month");

const expYearSchema = z
  .string()
  .min(1, "Required")
  .regex(/^\d{4}$/, "Invalid year");

const cvvSchema = z.string().regex(/^\d{3,4}$/, "CVV must be 3 or 4 digits");

// ===== Validation — only runs on blur / select change =====
function validateField(field) {
  const schemas = {
    cardholder: cardholderSchema,
    cardNumber: cardNumberSchema,
    expMonth: expMonthSchema,
    expYear: expYearSchema,
    cvv: cvvSchema,
  };
  const result = schemas[field].safeParse(form[field]);
  errors[field] = result.success ? "" : result.error.issues[0].message;

  // cross-field expiry-not-past check
  if (field === "expMonth" || field === "expYear") {
    if (
      /^(0[1-9]|1[0-2])$/.test(form.expMonth) &&
      /^\d{4}$/.test(form.expYear)
    ) {
      const exp = new Date(Number(form.expYear), Number(form.expMonth));
      if (exp <= new Date()) {
        errors.expYear = "Card has expired";
      }
    }
  }
}

// ===== Card number: format AND validate only on blur =====
function handleCardNumberBlur() {
  const cleaned = form.cardNumber.replace(/\D/g, "").slice(0, 19);
  form.cardNumber = cleaned.replace(/(.{4})/g, "$1 ").trim();
  validateField("cardNumber");
}

// ===== Test cards =====
const testCards = {
  4242424242424242: { result: "success" },
  4000000000000002: { result: "decline", message: "Your card was declined." },
  4000000000009995: { result: "decline", message: "Insufficient funds." },
  4000000000000069: { result: "decline", message: "Card has expired." },
  4000000000000127: { result: "decline", message: "Incorrect CVV." },
};

// ===== Submit =====
async function handleSubmit() {
  ["cardholder", "cardNumber", "expMonth", "expYear", "cvv"].forEach(
    validateField,
  );
  const hasErrors = Object.values(errors).some((e) => e);
  if (hasErrors) {
    submitError.value = "Please fix the errors above before submitting.";
    return;
  }

  submitError.value = "";
  loading.value = true;

  await new Promise((r) => setTimeout(r, 900));

  const cleanedNumber = form.cardNumber.replace(/\s/g, "");
  const cardOutcome = testCards[cleanedNumber] || { result: "success" };

  if (cardOutcome.result !== "success") {
    submitError.value = cardOutcome.message;
    loading.value = false;
    return;
  }

  const orderRecord = {
    confirmationId: `QF-${Math.random().toString(36).slice(2, 8).toUpperCase()}`,
    serviceCategory: orderStore.serviceCategory || "Service",
    customerId: userStore.currentUser?.id,
    customerName: userStore.currentUser?.name,
    customerEmail: userStore.currentUser?.email,
    provider: {
      userID: selectedProvider.value?.userID,
      name: selectedProvider.value?.name,
      avatar: selectedProvider.value?.avatar,
      hiredFor: selectedProvider.value?.profession || "Service",
    },
    plan: plan.value,
    planLabel: planLabel.value,
    address: address.value,
    apartment: apartment.value,
    description: description.value,
    scheduledDate: scheduledDate.value,
    scheduledTime: scheduledTime.value,
    scheduledTimeText: scheduledTimeText.value,
    hourlyRate: selectedProvider.value?.price || 0,
    serviceFee,
    last4: cleanedNumber.slice(-4),
    cardholder: form.cardholder,
    comments: form.comments,
  };

  historyStore.addOrder(orderRecord);

  // NEW: Save the address to the logged-in user's profile so it prefills
  // next time they open the Form. saveAddress no-ops if not logged in.
  userStore.saveAddress(address.value, apartment.value);

  loading.value = false;
  window.location.hash = `/PaymentSuccess?id=${orderRecord.confirmationId}`;
}

function handleCancel() {
  window.location.hash = "/";
}
</script>

<template>
  <div class="m-10 flex items-start justify-center gap-5">
    <Card class="w-100 rounded-3xl border-2 p-5">
      <form @submit.prevent="handleSubmit" autocomplete="off">
        <FieldGroup>
          <FieldSet>
            <FieldLegend>Payment Method</FieldLegend>
            <FieldDescription>
              All transactions are secure and encrypted
            </FieldDescription>
            <FieldGroup>
              <Field>
                <FieldLabel for="checkout-card-name">
                  Cardholder Full Name
                </FieldLabel>
                <Input
                  id="checkout-card-name"
                  v-model="form.cardholder"
                  autocomplete="off"
                  :class="errors.cardholder && 'border-destructive'"
                  @blur="validateField('cardholder')"
                />
                <p v-if="errors.cardholder" class="text-destructive text-sm">
                  {{ errors.cardholder }}
                </p>
              </Field>

              <Field>
                <FieldLabel for="checkout-card-number">Card Number</FieldLabel>
                <Input
                  id="checkout-card-number"
                  v-model="form.cardNumber"
                  placeholder="1234 5678 9012 3456"
                  inputmode="numeric"
                  maxlength="23"
                  autocomplete="off"
                  :class="errors.cardNumber && 'border-destructive'"
                  @blur="handleCardNumberBlur"
                />
                <p v-if="errors.cardNumber" class="text-destructive text-sm">
                  {{ errors.cardNumber }}
                </p>
              </Field>

              <div class="grid grid-cols-3 gap-4">
                <Field>
                  <FieldLabel for="checkout-exp-month">Month</FieldLabel>
                  <Select
                    v-model="form.expMonth"
                    @update:model-value="validateField('expMonth')"
                  >
                    <SelectTrigger
                      id="checkout-exp-month"
                      :class="errors.expMonth && 'border-destructive'"
                    >
                      <SelectValue placeholder="MM" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem
                        v-for="m in [
                          '01',
                          '02',
                          '03',
                          '04',
                          '05',
                          '06',
                          '07',
                          '08',
                          '09',
                          '10',
                          '11',
                          '12',
                        ]"
                        :key="m"
                        :value="m"
                      >
                        {{ m }}
                      </SelectItem>
                    </SelectContent>
                  </Select>
                  <p v-if="errors.expMonth" class="text-destructive text-xs">
                    {{ errors.expMonth }}
                  </p>
                </Field>

                <Field>
                  <FieldLabel for="checkout-exp-year">Year</FieldLabel>
                  <Select
                    v-model="form.expYear"
                    @update:model-value="validateField('expYear')"
                  >
                    <SelectTrigger
                      id="checkout-exp-year"
                      :class="errors.expYear && 'border-destructive'"
                    >
                      <SelectValue placeholder="YYYY" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="2026">2026</SelectItem>
                      <SelectItem value="2027">2027</SelectItem>
                      <SelectItem value="2028">2028</SelectItem>
                      <SelectItem value="2029">2029</SelectItem>
                      <SelectItem value="2030">2030</SelectItem>
                    </SelectContent>
                  </Select>
                  <p v-if="errors.expYear" class="text-destructive text-xs">
                    {{ errors.expYear }}
                  </p>
                </Field>

                <Field>
                  <FieldLabel for="checkout-cvv">CVV</FieldLabel>
                  <Input
                    id="checkout-cvv"
                    v-model="form.cvv"
                    placeholder="123"
                    inputmode="numeric"
                    maxlength="4"
                    autocomplete="off"
                    :class="errors.cvv && 'border-destructive'"
                    @blur="validateField('cvv')"
                  />
                  <p v-if="errors.cvv" class="text-destructive text-xs">
                    {{ errors.cvv }}
                  </p>
                </Field>
              </div>
            </FieldGroup>
          </FieldSet>

          <FieldSet>
            <FieldGroup>
              <Field>
                <FieldLabel for="checkout-comments">Comments</FieldLabel>
                <Textarea
                  id="checkout-comments"
                  v-model="form.comments"
                  placeholder="Additional comments, whether you would want to be called or texted"
                  class="resize-none"
                />
              </Field>
            </FieldGroup>
          </FieldSet>

          <div
            v-if="submitError"
            class="border-destructive text-destructive flex items-center gap-2 rounded-md border p-3 text-sm"
          >
            <AlertCircle class="size-4 shrink-0" />
            <span>{{ submitError }}</span>
          </div>

          <Field orientation="horizontal">
            <div>
              <p class="text-muted-foreground mb-5">
                Note: The provider will make communications with you to confirm
                the exact time and details of the job.
              </p>
              <div class="flex gap-2">
                <Button type="submit" :disabled="loading">
                  {{ loading ? "Processing…" : "Submit" }}
                </Button>
                <Button
                  variant="outline"
                  type="button"
                  :disabled="loading"
                  @click="handleCancel"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Field>
        </FieldGroup>
      </form>
    </Card>

    <!-- Order summary card -->
    <Card
      class="border-black-800 flex max-w-90 flex-col rounded-3xl border-2 p-5"
    >
      <div class="flex flex-col items-center gap-4 p-5">
        <Avatar class="scale-[1.3]">
          <AvatarImage :src="selectedProvider.avatar" />
          <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
        </Avatar>
        <CardTitle>{{ selectedProvider.name }}</CardTitle>
      </div>

      <Separator />

      <div class="flex flex-col gap-3 p-5">
        <CardTitle class="text-base">Job Details</CardTitle>
        <div class="flex justify-between text-sm">
          <p class="text-muted-foreground mr-4 shrink-0">Job Size</p>
          <p class="text-right font-medium">{{ planLabel }}</p>
        </div>
        <div class="flex justify-between gap-1 text-sm">
          <p class="text-muted-foreground mr-4">Location</p>
          <p class="min-w-0 text-right font-medium text-balance break-words">
            {{ address }}{{ apartment ? `, ${apartment}` : "" }}
          </p>
        </div>
        <div class="flex flex-col gap-1 text-sm">
          <p class="text-muted-foreground">Task Description</p>
          <p class="text-sm wrap-break-word">{{ description }}</p>
        </div>
      </div>

      <Separator />

      <div class="flex flex-col gap-3 p-5">
        <CardTitle class="text-base">Schedule</CardTitle>
        <div class="flex items-center gap-2 text-sm">
          <CalendarIcon class="text-muted-foreground size-4" />
          <p>{{ formattedDate }}</p>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <Clock class="text-muted-foreground size-4" />
          <p>{{ scheduledTime }} {{ scheduledTimeText }}</p>
        </div>
      </div>

      <Separator />

      <div class="flex flex-col gap-3 p-5">
        <CardTitle class="text-base">Cost Breakdown</CardTitle>
        <div class="flex justify-between text-sm">
          <p>Hourly Rate</p>
          <p class="font-medium">${{ selectedProvider.price.toFixed(2) }}</p>
        </div>
        <div class="flex justify-between text-sm">
          <p>Service Fee</p>
          <p>${{ serviceFee.toFixed(2) }}</p>
        </div>
      </div>
    </Card>
  </div>
</template>
