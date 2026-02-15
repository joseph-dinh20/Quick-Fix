<script setup lang="js">
import { toTypedSchema } from '@vee-validate/zod'
import { Check, Circle, Dot } from 'lucide-vue-next'
import { ref } from 'vue'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { h } from 'vue'
import { toast } from 'vue-sonner'

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form'

import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Stepper,
  StepperDescription,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger
} from '@/components/ui/stepper'

import {
  RadioGroup,
  RadioGroupItem,
} from '@/components/ui/radio-group'

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { Textarea } from '@/components/ui/textarea'

// a list of schemas formSchema[0,1,2...]
const formSchema = [
  z.object({
    address: z.string({ message: "Address cannot be left empty." }).min(1, { message: "Address cannot be left empty." }),
    apartment: z.string().optional(),
  }),
  z.object({
    // plan: z.string({ message: 'You must select a subscription plan to continue.' }).min(1, { message: 'You must select a subscription plan to continue.' }),
    plan: z.enum(['small', 'medium', 'large'], {
      message: "you must select an option."
    })
  }),
  z.object({
    description: z.string({ message: "description cannot be empty." }).min(1, { message: "description cannot be empty." })
  }),
]

// step index to know which step we're at along
// with array of steps object steps[0,1,2..]
const stepIndex = ref(1)
const steps = [
  {
    step: 1,
    title: 'Service Location',
    description: 'Provide an address',
  },
  {
    step: 2,
    title: 'Job Length',
    description: 'How big is the job?',
  },
  {
    step: 3,
    title: 'Additional Information',
    description: 'job description',
  },
]

const plans = [
  {
    id: 'small',
    title: 'Small (1 hour)',
    description: 'it takes about an hour or less to complete the job',
  },
  {
    id: 'medium',
    title: 'Medium (2~3 hours)',
    description: 'the job requires about 2-3 hours to complete',
  },
  {
    id: 'large',
    title: 'Large (4+ hours or more)',
    description: 'for larger projects that require extra time',
  },
]

// simple function to get the values in string form for display
function onSubmit(values) {
  toast('You submitted the following values:', {
    description: h('pre', { class: 'bg-code text-code-foreground mt-2 w-[320px] overflow-x-auto rounded-md p-4' }, h('code', JSON.stringify(values, null, 2))),
    position: 'bottom-right',
    class: 'flex flex-col gap-2',
    style: {
      '--border-radius': 'calc(var(--radius)  + 4px)',
    },
  })
}
</script>

<template>
  <div>
    <Form v-slot="{ meta, values, validate }" as="" keep-values :initial-values="{
      apartment: ''
    }" :validation-schema="toTypedSchema(formSchema[stepIndex - 1])">
      <Stepper v-slot="{ isNextDisabled, isPrevDisabled, nextStep, prevStep, modelValue }" v-model="stepIndex"
        class="block w-full">
        <form @submit="(e) => {
          e.preventDefault()
          validate()

          if (stepIndex === steps.length && meta.valid) {
            onSubmit(values)
          }
        }">
          <div class="flex w-full flex-start gap-10">
            <StepperItem v-for="(step, index) in steps" :key="step.step" v-slot="{ state }"
              class="relative flex w-full flex-col items-center justify-center" :step="step.step">
              <StepperSeparator v-if="step.step !== steps[steps.length - 1].step"
                class="absolute left-[calc(50%+20px)] right-[calc(-90%+10px)] top-5 block h-0.5 shrink-0 rounded-full bg-muted group-data-[state=completed]:bg-primary" />

              <StepperTrigger as-child>
                <Button :variant="state === 'completed' || state === 'active' ? 'default' : 'outline'" size="icon"
                  class="z-10 rounded-full shrink-0"
                  :class="[state === 'active' && 'ring-2 ring-ring ring-offset-2 ring-offset-background']"
                  :disabled="state !== 'completed' && (index >= (modelValue || 0) && !meta.valid)">
                  <Check v-if="state === 'completed'" class="size-5" />
                  <Circle v-if="state === 'active'" />
                  <Dot v-if="state === 'inactive'" />
                </Button>
              </StepperTrigger>

              <div class="mt-5 flex flex-col items-center text-center">
                <StepperTitle :class="[state === 'active' && 'text-primary']"
                  class="text-sm font-semibold transition lg:text-base">
                  {{ step.title }}
                </StepperTitle>
                <StepperDescription :class="[state === 'active' && 'text-primary']"
                  class="sr-only text-xs text-muted-foreground transition md:not-sr-only lg:text-sm">
                  {{ step.description }}
                </StepperDescription>
              </div>
            </StepperItem>
          </div>

          <div class="flex flex-col gap-4 mt-20">
            <template v-if="stepIndex === 1">
              <Card>
                <CardHeader>
                  <CardTitle>Service Location</CardTitle>
                  <CardDescription>where should we meet you?</CardDescription>
                </CardHeader>
                <CardContent class="flex flex-col gap-6">
                  <FormField v-slot="{ componentField }" name="address">
                    <FormItem>
                      <FormLabel>Address</FormLabel>
                      <FormControl>
                        <Input type="text" v-bind="componentField"
                          placeholder="323 W Salt Lake, Long Beach, CA, 90100" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>

                  <FormField v-slot="{ componentField }" name="apartment">
                    <FormItem>
                      <FormLabel>Apartment (optional)</FormLabel>
                      <FormControl>
                        <Input type="text" v-bind="componentField" placeholder="Unit 101 | Suite #3 | Apt #10" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>
                </CardContent>
              </Card>
            </template>

            <template v-if="stepIndex === 2">
              <Card>
                <CardHeader>
                  <CardTitlte class="font-semibold">Service Length</CardTitlte>
                </CardHeader>
                <CardContent>
                  <FormField v-slot="{ componentField }" name="plan">
                    <FormItem>
                      <FormLabel class="text-sm text-muted-foreground"> How long does the task take?</FormLabel>
                      <FormControl>
                        <RadioGroup :model-value="componentField.modelValue"
                          @update:model-value="componentField['onUpdate:modelValue']" class="flex flex-col gap-3">
                          <div v-for="plan in plans" :key="plan.id"
                            @click="componentField['onUpdate:modelValue'](plan.id)"
                            class="justify-between cursor-pointer hover:bg-muted flex items-center space-x-3 border rounded-lg p-3"
                            v-bind:class="{
                              'border-green-500 bg-green-50': componentField.modelValue === plan.id,
                            }">
                            <div class="flex flex-col">
                              <FormLabel class="text-base font-medium"> {{ plan.title }} </FormLabel>
                              <formlabel class="text-sm text-muted-foreground">
                                {{ plan.description }}
                              </formlabel>
                            </div>
                            <RadioGroupItem :value="plan.id" />
                          </div>
                        </RadioGroup>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>
                </CardContent>
              </Card>
            </template>

            <template v-if="stepIndex === 3">

              <Card class="min-h-full min-w-150">
                <CardHeader>
                  <CardTitlte class="font-semibold">Task Description</CardTitlte>
                  <CardDescription>
                    provide additional information about the job. A good
                  </CardDescription>
                  <CardDescription>
                    description will reduce the time spent between you and the Fixer.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <FormField v-slot="{ componentField }" name="description">
                    <FormItem>
                      <FormLabel></FormLabel>
                      <FormControl>
                        <Textarea class="min-h-50 min-w-full" type="text" v-bind="componentField"
                          placeholder="Start describing here..." />

                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  </FormField>
                </CardContent>
              </Card>
            </template>
          </div>

          <div class="flex items-center justify-between mt-4">
            <Button :disabled="isPrevDisabled" variant="outline" size="sm" @click="prevStep()">
              Back
            </Button>
            <div class="flex items-center gap-3">
              <Button v-if="stepIndex !== 3" :type="meta.valid ? 'button' : 'submit'" :disabled="isNextDisabled"
                size="sm" @click="meta.valid && nextStep()">
                Next
              </Button>
              <Button v-if="stepIndex === 3" size="sm" type="submit">
                Submit
              </Button>
            </div>
          </div>
        </form>
      </Stepper>
    </Form>
  </div>
</template>
