<script setup lang="ts">
import { ref } from 'vue'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm, Field as VeeField } from 'vee-validate'
import { z } from 'zod'
import { Textarea } from '@/components/ui/textarea'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  // CardDescription,
  CardFooter,
  CardHeader,
  // CardHeader,
  // CardTitle,
} from '@/components/ui/card'
import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
  FieldTitle,
} from '@/components/ui/field'
import {
  RadioGroup,
  RadioGroupItem,
} from '@/components/ui/radio-group'
import { Input } from './ui/input'

const plans = [
  {
    id: 'small',
    title: 'small (less than 1 Hour)',
    description: 'small tasks that can be done quick.',
  },
  {
    id: 'medium',
    title: 'medium (2~3 Hours)',
    description: 'tasks that requires extra time',
  },
  {
    id: 'large',
    title: 'large (3+ Hours minimum)',
    description: 'for larger projects with more complexity',
  },
] as const

const formSchema = toTypedSchema(
  z.object({
    plan: z.string().min(1, 'You must select an option to continue.'),
  }),
)

const { handleSubmit, resetForm } = useForm({
  validationSchema: formSchema,
  initialValues: {
    plan: '',
  },
})

const step = ref(1)

async function nextStep() {
  try {
    await handleSubmit(
      (values) => {
        console.log('Step 1 valid, values:', values)
        step.value++
      },
      (errors) => {
        console.log('Step 1 invalid, errors:', errors)
      }
    )()
  } catch (err) {
    console.error('Unexpected error in step validation:', err)
  }
}

</script>

<template>
  <div v-if="step === 1">
    <Card class="m-20 min-h-100 min-w-100">
      <CardContent class="m-5">
        <Field>
          <FieldSet>
            <FieldGroup>
              <FieldLegend variant="legend">Where are you Located?</FieldLegend>
              <Input id="street" placeholder="Street Address" required />
              <Input id="unit" placeholder="Unit Number or apt" required />
              <Button type="submit" @click="step++"> Continue </Button>
            </FieldGroup>
          </FieldSet>
        </Field>
      </CardContent>
    </Card>
  </div>
  <div v-if="step === 2" class="w-full sm:max-w-md m-5">
    <Card>
      <CardContent class="m-5">
        <VeeField v-slot="{ field, errors }" name="plan">
          <FieldSet :data-invalid="!!errors.length">
            <FieldLegend>Hours</FieldLegend>
            <FieldDescription>
              How big is the project going to take?
            </FieldDescription>
            <RadioGroup :name="field.name" :model-value="field.value" :aria-invalid="!!errors.length"
              @update:model-value="field.onChange">

              <!-- displaying entire loop of plans -->
              <FieldLabel v-for="plan in plans" :key="plan.id" :for="`form-vee-radiogroup-${plan.id}`">
                <Field orientation="horizontal" :data-invalid="!!errors.length">
                  <FieldContent>
                    <FieldTitle>{{ plan.title }}</FieldTitle>
                    <FieldDescription>
                      {{ plan.description }}
                    </FieldDescription>
                  </FieldContent>
                  <RadioGroupItem :id="`form-vee-radiogroup-${plan.id}`" :value="plan.id"
                    :aria-invalid="!!errors.length" />
                </Field>
              </FieldLabel>
            </RadioGroup>
            <!-- <FieldError v-if="errors.length" :errors="errors" /> -->
            <FieldError v-if="errors.length" class="text-red-500" />
            {{ errors[0] }}
          </FieldSet>
        </VeeField>
      </CardContent>
      <CardFooter>
        <Field orientation="horizontal">
          <Button type="button" variant="outline" @click="resetForm">
            Reset
          </Button>
          <!-- <Button type="submit" @click="nextStep" form="form-vee-radiogroup"> -->
          <Button type="button" @click="nextStep"> Continue </Button>
        </Field>
      </CardFooter>
    </Card>
  </div>
  <div v-if="step === 3" class="m-5 min-h-100 min-w-100 flex flex-col">
    <div className="grid w-full gap-2">
      <Field>
        <FieldLabel class="text-2xl">Describe to us what you need help with</FieldLabel>
        <FieldDescription>Inform the fixers what you need help with as best as you can. </FieldDescription>
        <FieldDescription>A helpful description can reduce the time spent with your fixer.
        </FieldDescription>
        <Textarea id="textarea-message" placeholder="Type your message here." />
        <Button>Submit</Button>
      </Field>
    </div>
  </div>
</template>
