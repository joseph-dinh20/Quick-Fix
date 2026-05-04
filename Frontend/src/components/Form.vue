<!-- NOTE: Form.vue -->
<script setup>
import { toTypedSchema } from "@vee-validate/zod";
import { Check, Circle, Dot } from "lucide-vue-next";
import { ref, onMounted, useTemplateRef } from "vue";
import * as z from "zod";
import { Button } from "@/components/ui/button";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import { Input } from "@/components/ui/input";
import {
  Stepper,
  StepperDescription,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger,
} from "@/components/ui/stepper";

import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Textarea } from "@/components/ui/textarea";

// NOTE: Global state management
import { useOrderStore } from "@/store/orderStore";
import { useUserStore } from "@/store/userStore";

const orderStore = useOrderStore();
const userStore = useUserStore();

// Ref to the vee-validate <Form> so we can call setFieldValue after mount
const formRef = useTemplateRef("formRef");

const formSchema = [
  z.object({
    address: z
      .string({ message: "Address cannot be left empty." })
      .min(1, { message: "Address cannot be left empty." }),
    apartment: z.string().optional(),
  }),
  z.object({
    plan: z.enum(["small", "medium", "large"], {
      message: "you must select an option.",
    }),
  }),
  z.object({
    description: z
      .string({ message: "description cannot be empty." })
      .min(1, { message: "description cannot be empty." }),
  }),
];

const stepIndex = ref(1);
const steps = [
  { step: 1, title: "Service Location", description: "Provide an address" },
  { step: 2, title: "Job Length", description: "How big is the job?" },
  { step: 3, title: "Additional Information", description: "job description" },
];

const plans = [
  {
    id: "small",
    title: "Small (1 hour)",
    description: "it takes about an hour or less to complete the job",
  },
  {
    id: "medium",
    title: "Medium (2~3 hours)",
    description: "the job requires about 2-3 hours to complete",
  },
  {
    id: "large",
    title: "Large (4+ hours or more)",
    description: "for larger projects that require extra time",
  },
];

// On mount, prefill address + apartment from the logged-in user's saved profile.
// If not logged in, leave the form empty.
onMounted(() => {
  if (!formRef.value) return;
  if (!userStore.isLoggedIn) return;

  const savedAddress = userStore.currentUser?.address || "";
  const savedApartment = userStore.currentUser?.apartment || "";

  if (savedAddress) {
    formRef.value.setFieldValue("address", savedAddress);
  }
  if (savedApartment) {
    formRef.value.setFieldValue("apartment", savedApartment);
  }
});

function onSubmit(values) {
  // Save form data to the in-progress order
  orderStore.setFormData(values);

  // Persist most-recent address to the logged-in user's profile.
  // saveAddress is a no-op if the user isn't logged in.
  userStore.saveAddress(values.address, values.apartment);

  window.location.hash = "#/ProviderList";
}
</script>

<template>
  <div class="mx-auto mt-10 max-w-150 px-10 py-10">
    <Form
      ref="formRef"
      v-slot="{ meta, values, validate }"
      as=""
      keep-values
      :validation-schema="toTypedSchema(formSchema[stepIndex - 1])"
    >
      <Stepper
        v-slot="{
          isNextDisabled,
          isPrevDisabled,
          nextStep,
          prevStep,
          modelValue,
        }"
        v-model="stepIndex"
        class="block w-full"
      >
        <form
          @submit="
            (e) => {
              e.preventDefault();
              validate();

              if (stepIndex === steps.length && meta.valid) {
                onSubmit(values);
              }
            }
          "
        >
          <div class="flex-start flex w-full gap-10">
            <StepperItem
              v-for="(step, index) in steps"
              :key="step.step"
              v-slot="{ state }"
              class="relative flex w-full flex-col items-center justify-center"
              :step="step.step"
            >
              <StepperSeparator
                v-if="step.step !== steps[steps.length - 1].step"
                class="bg-muted group-data-[state=completed]:bg-primary absolute top-5 right-[calc(-90%+10px)] left-[calc(50%+20px)] block h-0.5 shrink-0 rounded-full"
              />

              <StepperTrigger as-child>
                <Button
                  :variant="
                    state === 'completed' || state === 'active'
                      ? 'default'
                      : 'outline'
                  "
                  size="icon"
                  class="z-10 shrink-0 rounded-full"
                  :class="[
                    state === 'active' &&
                      'ring-ring ring-offset-background ring-2 ring-offset-2',
                  ]"
                  :disabled="
                    state !== 'completed' &&
                    index >= (modelValue || 0) &&
                    !meta.valid
                  "
                >
                  <Check v-if="state === 'completed'" class="size-5" />
                  <Circle v-if="state === 'active'" />
                  <Dot v-if="state === 'inactive'" />
                </Button>
              </StepperTrigger>

              <div class="mt-5 flex flex-col items-center text-center">
                <StepperTitle
                  :class="[state === 'active' && 'text-primary']"
                  class="text-sm font-semibold transition lg:text-base"
                >
                  {{ step.title }}
                </StepperTitle>
                <StepperDescription
                  :class="[state === 'active' && 'text-primary']"
                  class="text-muted-foreground sr-only text-xs transition md:not-sr-only lg:text-sm"
                >
                  {{ step.description }}
                </StepperDescription>
              </div>
            </StepperItem>
          </div>

          <div class="mt-20 flex flex-col gap-4">
            <template v-if="stepIndex === 1">
              <Card>
                <CardHeader>
                  <CardTitle>Service Location</CardTitle>
                  <CardDescription>
                    Where should the provider show up?
                  </CardDescription>
                </CardHeader>
                <CardContent class="flex flex-col gap-6">
                  <FormField v-slot="{ componentField: field }" name="address">
                    <FormItem>
                      <FormLabel>Address</FormLabel>
                      <FormControl>
                        <Input
                          type="text"
                          v-bind="field"
                          placeholder="323 W Salt Lake, Long Beach, CA, 90100"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>

                  <FormField v-slot="{ componentField }" name="apartment">
                    <FormItem>
                      <FormLabel>Apartment (optional)</FormLabel>
                      <FormControl>
                        <Input
                          type="text"
                          v-bind="componentField"
                          placeholder="Unit 101 | Suite #3 | Apt #10"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>
                </CardContent>
                <CardFooter class="flex items-center justify-between pt-4">
                  <Button
                    :disabled="isPrevDisabled"
                    variant="outline"
                    @click="prevStep()"
                  >
                    Back
                  </Button>
                  <Button
                    class="cursor-pointer"
                    :type="meta.valid ? 'button' : 'submit'"
                    :disabled="isNextDisabled"
                    @click="meta.valid && nextStep()"
                  >
                    Next
                  </Button>
                </CardFooter>
              </Card>
            </template>

            <template v-if="stepIndex === 2">
              <Card>
                <CardHeader>
                  <CardTitle class="font-semibold">Service Length</CardTitle>
                </CardHeader>
                <CardContent>
                  <FormField v-slot="{ componentField }" name="plan">
                    <FormItem>
                      <FormLabel class="text-muted-foreground text-sm">
                        How long does the task take?
                      </FormLabel>
                      <FormControl>
                        <RadioGroup
                          :model-value="componentField.modelValue"
                          @update:model-value="
                            componentField['onUpdate:modelValue']
                          "
                          class="flex flex-col gap-3"
                        >
                          <div
                            v-for="plan in plans"
                            :key="plan.id"
                            @click="
                              componentField['onUpdate:modelValue'](plan.id)
                            "
                            class="hover:bg-muted flex cursor-pointer items-center justify-between space-x-3 rounded-lg border p-3"
                            v-bind:class="{
                              'border-green-500 bg-green-50':
                                componentField.modelValue === plan.id,
                            }"
                          >
                            <div class="flex flex-col">
                              <FormLabel class="text-base font-medium">
                                {{ plan.title }}
                              </FormLabel>
                              <FormLabel class="text-muted-foreground text-sm">
                                {{ plan.description }}
                              </FormLabel>
                            </div>
                            <RadioGroupItem :value="plan.id" />
                          </div>
                        </RadioGroup>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>
                </CardContent>
                <CardFooter class="flex items-center justify-between pt-4">
                  <Button
                    :disabled="isPrevDisabled"
                    variant="outline"
                    @click="prevStep()"
                  >
                    Back
                  </Button>
                  <Button
                    class="cursor-pointer"
                    :type="meta.valid ? 'button' : 'submit'"
                    :disabled="isNextDisabled"
                    @click="meta.valid && nextStep()"
                  >
                    Next
                  </Button>
                </CardFooter>
              </Card>
            </template>

            <template v-if="stepIndex === 3">
              <Card class="min-h-full">
                <CardHeader>
                  <CardTitle class="font-semibold">Task Description</CardTitle>
                  <CardDescription>
                    provide additional information about the job. A good
                  </CardDescription>
                  <CardDescription>
                    description will reduce the time spent between you and the
                    Fixer.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <FormField v-slot="{ componentField }" name="description">
                    <FormItem>
                      <FormLabel></FormLabel>
                      <FormControl>
                        <Textarea
                          class="min-h-50 min-w-full"
                          type="text"
                          v-bind="componentField"
                          placeholder="Start describing here..."
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>
                </CardContent>
                <CardFooter class="flex items-center justify-between pt-4">
                  <Button
                    :disabled="isPrevDisabled"
                    variant="outline"
                    @click="prevStep()"
                  >
                    Back
                  </Button>
                  <Button type="submit" class="cursor-pointer">Submit</Button>
                </CardFooter>
              </Card>
            </template>
          </div>
        </form>
      </Stepper>
    </Form>
  </div>
</template>
