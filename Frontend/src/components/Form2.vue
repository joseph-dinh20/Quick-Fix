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

const plans = [
  {
    id: 'starter',
    title: 'Starter (100K tokens/month)',
    description: 'For everyday use with basic features.',
  },
  {
    id: 'pro',
    title: 'Pro (1M tokens/month)',
    description: 'For advanced AI usage with more features.',
  },
  {
    id: 'enterprise',
    title: 'Enterprise (Unlimited tokens)',
    description: 'For large teams and heavy usage.',
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

const onSubmit = handleSubmit((data) => {
  console.log(data)
})
</script>

<template>
  <Card class="w-full sm:max-w-md">
    <!-- <CardHeader> -->
    <!--   <CardTitle>Subscription Plan</CardTitle> -->
    <!--   <CardDescription> -->
    <!--     See pricing and features for each plan. -->
    <!--   </CardDescription> -->
    <!-- </CardHeader> -->
    <!-- <CardContent"> -->
    <CardContent class="m-5">
      <form id="form-vee-radiogroup" @submit="onSubmit">
        <FieldGroup>
          <VeeField v-slot="{ field, errors }" name="plan">
            <FieldSet :data-invalid="!!errors.length">
              <FieldLegend>Hours</FieldLegend>
              <FieldDescription>
                How big is the task going to be?
              </FieldDescription>
              <RadioGroup :name="field.name" :model-value="field.value" :aria-invalid="!!errors.length"
                @update:model-value="field.onChange">
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
        </FieldGroup>
      </form>
    </CardContent>
    <CardFooter>
      <Field orientation="horizontal">
        <Button type="button" variant="outline" @click="resetForm">
          Reset
        </Button>
        <Button type="submit" form="form-vee-radiogroup">
          Continue
        </Button>
      </Field>
    </CardFooter>
  </Card>
</template>
