<script setup>
import { ref } from "vue"
import { createJob } from "../services/api"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"

const title = ref("")
const city = ref("") // Added missing ref
const zip = ref("")  // Added missing ref
const description = ref("")
const budget = ref("")
const deadline = ref("")
const requestType = ref("quote")
const services = ref([])   // array of IDs
const images = ref([])

const message = ref("")
const fileInput = ref(null) // Template ref for the file input

function handleImageUpload(e) {
  images.value = Array.from(e.target.files)
}

async function submitJob() {
  try {
    await createJob({
      title: title.value,
      description: description.value,
      budget: budget.value,
      deadline: deadline.value,
      request_type: requestType.value,
      services: services.value,
      images: images.value
    })

    message.value = "Job created successfully"

    // reset form
    title.value = ""
    city.value = ""
    zip.value = ""
    description.value = ""
    budget.value = ""
    deadline.value = ""
    requestType.value = "quote"
    services.value = []
    images.value = []

  } catch (err) {
    console.error(err)
    message.value = "Error creating job"
  }
}
</script>

<template>
  <div class="max-w-5xl mx-auto p-8">
    <h1 class="text-3xl font-bold mb-8">Post a Job</h1>

    <div v-if="message" class="mb-4 p-4 bg-blue-50 text-blue-700 rounded-md">
      {{ message }}
    </div>

    <form @submit.prevent="submitJob">
      <div class="bg-white border rounded-xl shadow-sm p-10">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div class="md:col-span-2 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="title" class="font-semibold">
                  Job Title<span class="text-orange-500">*</span>
                </Label>
                <Input 
                  id="title"
                  v-model="title" 
                  placeholder="Job Title" 
                  class="bg-slate-50 focus-visible:ring-orange-500" 
                  required 
                />
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="city" class="font-semibold">City</Label>
                  <Input id="city" v-model="city" placeholder="City" class="bg-slate-50" />
                </div>
                <div class="space-y-2">
                  <Label for="zip" class="font-semibold">ZIP Code</Label>
                  <Input id="zip" v-model="zip" placeholder="ZIP Code" class="bg-slate-50" />
                </div>
              </div>
            </div>

            <div class="space-y-2">
              <Label for="description" class="font-semibold">Description</Label>
              <Textarea 
                id="description"
                v-model="description" 
                placeholder="Describe the job..." 
                class="bg-slate-50 min-h-[150px] focus-visible:ring-orange-500" 
                required 
              />
            </div>
          </div>

          <div class="flex flex-col justify-end">
            <div 
              class="border-2 border-dashed border-slate-200 rounded-xl p-8 flex flex-col items-center justify-center text-slate-400 hover:bg-slate-50 cursor-pointer transition-colors min-h-[150px]"
              @click="fileInput?.click()"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              <span class="text-sm">Upload images</span>
              <input 
                type="file" 
                ref="fileInput" 
                multiple 
                class="hidden" 
                @change="handleImageUpload" 
              />
            </div>
          </div>
        </div>

        <div class="mt-8 border-t pt-8">
          <h3 class="text-lg font-bold mb-4">More Options</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="space-y-4">
              <div class="space-y-2">
                <Label for="date" class="font-semibold">Date</Label>
                <Input id="date" type="date" v-model="deadline" class="bg-white block w-full" />
              </div>
              <div class="space-y-2">
                <Label class="font-semibold">Language</Label>
                <Select default-value="english">
                  <SelectTrigger class="w-full bg-white">
                    <SelectValue placeholder="Select Language" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="english">English</SelectItem>
                      <SelectItem value="spanish">Spanish</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div class="space-y-4">
              <div class="space-y-2">
                <Label for="time" class="font-semibold">Time</Label>
                <Input id="time" type="time" class="bg-white block w-full" />
              </div>
              <div class="space-y-2">
                <Label for="payment" class="font-semibold">Payment</Label>
                <div class="flex items-center border rounded-md overflow-hidden bg-white focus-within:ring-2 focus-within:ring-orange-500 focus-within:ring-offset-2">
                  <span class="px-3 text-slate-500 text-sm">$</span>
                  <input id="payment" v-model="budget" type="number" class="w-full py-2 bg-transparent outline-none text-sm" />
                  <span class="px-3 text-slate-500 text-sm">/hr</span>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <Label class="font-semibold block">Job Type</Label>
              <div class="space-y-3">
                <div class="flex items-center space-x-3">
                  <Checkbox id="type-quote" default-checked class="data-[state=checked]:bg-orange-500 data-[state=checked]:border-orange-500" />
                  <Label for="type-quote" class="text-sm font-normal cursor-pointer">Get a quote</Label>
                </div>
                <div class="flex items-center space-x-3">
                  <Checkbox id="type-fixed" default-checked class="data-[state=checked]:bg-orange-500 data-[state=checked]:border-orange-500" />
                  <Label for="type-fixed" class="text-sm font-normal cursor-pointer">Get fixed</Label>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <Label class="font-semibold block">Urgency</Label>
              <RadioGroup v-model="requestType" class="space-y-1">
                <div class="flex items-center space-x-3">
                  <RadioGroupItem id="urgency-flexible" value="quote" class="text-orange-500 border-slate-300 focus:ring-orange-500" />
                  <Label for="urgency-flexible" class="text-sm font-normal cursor-pointer">Flexible</Label>
                </div>
                <div class="flex items-center space-x-3">
                  <RadioGroupItem id="urgency-soon" value="soon" class="text-orange-500 border-slate-300 focus:ring-orange-500" />
                  <Label for="urgency-soon" class="text-sm font-normal cursor-pointer">Soon</Label>
                </div>
                <div class="flex items-center space-x-3">
                  <RadioGroupItem id="urgency-asap" value="asap" class="text-orange-500 border-slate-300 focus:ring-orange-500" />
                  <Label for="urgency-asap" class="text-sm font-normal cursor-pointer">ASAP</Label>
                </div>
              </RadioGroup>
            </div>
          </div>
        </div>

        <div class="mt-12 flex justify-center">
          <Button 
            type="submit" 
            class="bg-orange-500 hover:bg-orange-600 text-white font-bold h-14 px-16 rounded-xl text-xl transition-all shadow-md active:scale-95"
          >
            Post
          </Button>
        </div>
      </div>
    </form>
  </div>
</template>