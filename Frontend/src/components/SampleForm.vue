<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm, Field as VeeField } from 'vee-validate'
import { z } from 'zod'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
} from '@/components/ui/field'

import { Input } from '@/components/ui/input'

import {
  RadioGroup,
  RadioGroupItem,
} from '@/components/ui/radio-group'

import { Textarea } from '@/components/ui/textarea'

const formSchema = toTypedSchema(
  z.object({
    streetAddress: z
      .string()
      .min(1, 'Street Address cannot be empty'),
    // .max(10, 'Street Address must be at most 10 characters.')
    // .regex(
    //   /^\w+$/,
    //   'Street Address can only contain letters, numbers, and underscores.',
    // ),
    apartment: z
      .string().optional().or(z.literal('')),
    // .string().min(1, 'apartment cannot be empty'),

    taskHours: z
      .number({ error: "Please select an option for hours" }),

    messageForFixer: z
      .string()
      .min(1, "Message cannot be empty!"),
  }),
)

const { handleSubmit, resetForm } = useForm({
  validationSchema: formSchema,
  initialValues: {
    streetAddress: '',
    apartment: '',
    taskHours: undefined,
    messageForFixer: '',
  },
})

// SENDS JSON TO BACKEND EVENTUALLY
const onSubmit = handleSubmit((data) => {
  alert(JSON.stringify(data))
})

</script>

<template>
  <Card class="w-full sm:max-w-md">
    <CardHeader>
      <!-- <CardTitle>Service Information</CardTitle> -->
      <!-- <CardDescription> -->
      <!--   Enter the address you want to be serviced at. -->
      <!-- </CardDescription> -->
    </CardHeader>
    <CardContent>
      <form id="form" @submit="onSubmit">

        <FieldGroup>
          <!-- streetAddress -->
          <VeeField v-slot="{ field, errors }" name="streetAddress">
            <Field :data-invalid="!!errors.length">
              <FieldLabel for="streetAddress" class="underline">
                Street Address
              </FieldLabel>
              <FieldDescription for="streetAddress">
                Enter the address to be serviced at.
              </FieldDescription>
              <Input id="streetAddress" v-bind="field" :aria-invalid="!!errors.length"
                placeholder="ex. 325 S Lake, Pasadena" autocomplete="streetAddress" />
              <FieldError v-if="errors.length" :errors="errors.map((error) => ({ message: error }))" />
            </Field>
          </VeeField>

          <!-- apartment -->
          <VeeField v-slot="{ field, errors }" name="apartment">
            <Field :data-invalid="!!errors.length">
              <FieldLabel for="apartment" class="underline">
                Apartment (optional)
              </FieldLabel>
              <FieldDescription for="streetAddress">
                Enter your apartment number if there is any.
              </FieldDescription>
              <Input id="apartment" v-bind="field" :aria-invalid="!!errors.length"
                placeholder="ex. apt #105, or suite #3" autocomplete="current-apartment" />
              <FieldError v-if="errors.length" :errors="errors.map((error) => ({ message: error }))" />
            </Field>
          </VeeField>

          <!-- hours option -->

          <VeeField v-slot="{ field, errors }" name="taskHours">
            <Field :data-invalid="!!errors.length">
              <FieldLabel for="form-taskHours" class="underline">
                Work Duration
              </FieldLabel>
              <FieldDescription for=form-taskHours>
                How big is the job?
              </FieldDescription>
              <RadioGroup :model-value="field.value" @update:model-value="field.onChange">
                <div class="flex items-center space-x-2">
                  <RadioGroupItem id="r1" :value="1" />
                  <FieldLabel for="r1">Small (<1 hr)</FieldLabel>
                </div>
                <div class="flex items-center space-x-2">
                  <RadioGroupItem id="r2" :value="2" />
                  <FieldLabel for="r2">Medium (2~3 hrs)</FieldLabel>
                </div>
                <div class="flex items-center space-x-2">
                  <RadioGroupItem id="r3" :value="3" />
                  <FieldLabel for="r3">Large (>3 hrs)</FieldLabel>
                </div>
              </RadioGroup>
              <FieldError v-if="errors.length" :errors="errors.map((error) => ({ message: error }))" />
            </Field>
          </VeeField>
        </FieldGroup>

        <VeeField v-slot="{ field, errors }" name="messageForFixer">
          <Field :data-invalid="!!errors.length">
            <FieldLabel for="messageForFixer" class="underline mt-5">
              Job Description
            </FieldLabel>
            <FieldDescription>Let the fixers what you need help with as best as you can. A helpful description can
              reduce the time spent with your fixer.
            </FieldDescription>

            <Textarea id="message" v-bind="field" :aria-invalid="!!errors.length"
              placeholder="Type your message here." />
            <FieldError v-if="errors.length" :errors="errors.map((error) => ({ message: error }))" />
          </Field>
        </VeeField>
      </form>
    </CardContent>
    <CardFooter>
      <Field orientation="horizontal">
        <Button type="button" variant="outline" @click="resetForm">
          Reset
        </Button>
        <Button type="submit" form="form">
          Save
        </Button>
      </Field>
    </CardFooter>
  </Card>
</template>
