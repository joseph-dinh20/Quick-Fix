<script setup>
import { ref, onMounted } from "vue"
import { getMyJobs, deleteJob } from "../services/api"

// --- UI IMPORTS (Expanded for maximum shadcn usage) ---
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { AspectRatio } from "@/components/ui/aspect-ratio"
import { Label } from "@/components/ui/label"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { 
  Search, 
  Calendar, 
  Pencil, 
  Trash2, 
  ChevronDown, 
  DollarSign, 
  Info,
  ImageIcon 
} from "lucide-vue-next"
// ---------------------------------------------------

const jobs = ref([])
const currentSort = ref("Sort by")
const isDialogOpen = ref(false)
const selectedJob = ref(null)

async function fetchJobs() {
  try {
    const res = await getMyJobs()
    jobs.value = res.data
  } catch (err) {
    console.error(err)
  }
}

async function removeJob(jobId) {
  if (!confirm("Are you sure you want to make this job inactive?")) return
  try {
    await deleteJob(jobId)
    jobs.value = jobs.value.filter(j => j.id !== jobId)
  } catch (err) {
    console.error(err)
  }
}

function updateSort(sortOption) {
  currentSort.value = sortOption
}

function openJobDetails(job) {
  selectedJob.value = job
  isDialogOpen.value = true
}

function editJob(job) {
  console.log("Edit job:", job.title)
}

onMounted(fetchJobs)
</script>

<template>
  <div class="min-h-screen bg-slate-50 p-6 md:p-12 font-sans text-slate-900">
    <div class="max-w-4xl mx-auto">
      
      <h1 class="text-3xl font-extrabold tracking-tight mb-8 text-[#1a202c]">Manage Postings</h1>

      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div class="relative w-full sm:w-[450px] flex items-center bg-white rounded-full border border-slate-200 shadow-sm p-1.5">
          <Search class="w-5 h-5 text-slate-400 ml-3 absolute" />
          <Input
            placeholder="Search postings"
            class="border-0 focus-visible:ring-0 shadow-none pl-10 bg-transparent w-full"
          />
          <Button class="bg-orange-500 hover:bg-orange-600 text-white rounded-full px-6 py-2 shrink-0 h-auto font-bold">
            Search
          </Button>
        </div>

        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="bg-white border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg flex items-center gap-2 shadow-sm px-4 capitalize">
              {{ currentSort }}
              <ChevronDown class="w-4 h-4 text-slate-500 ml-1" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="w-40">
            <DropdownMenuItem @click="updateSort('Newest')">Newest</DropdownMenuItem>
            <DropdownMenuItem @click="updateSort('Oldest')">Oldest</DropdownMenuItem>
            <DropdownMenuItem @click="updateSort('Title (A-Z)')">Title (A-Z)</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div v-if="jobs.length" class="space-y-4">
        <Card 
          v-for="job in jobs" 
          :key="job.id" 
          @click="openJobDetails(job)"
          class="overflow-hidden border-slate-200 shadow-sm rounded-xl hover:shadow-md hover:border-orange-200 transition-all cursor-pointer"
        >
          <CardContent class="p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h3 class="font-bold text-[#1a202c] text-[15px] mb-2.5">{{ job.title }}</h3>
              <div class="flex items-center gap-3 text-sm">
                <Badge 
                  variant="outline" 
                  :class="job.status === 'inactive' 
                    ? 'bg-red-50 text-red-600 border-red-200' 
                    : 'bg-green-50 text-green-600 border-green-200'"
                  class="font-medium px-2.5 py-0.5 rounded-md capitalize"
                >
                  {{ job.status === 'inactive' ? 'Inactive' : 'Active' }}
                </Badge>
                <div class="flex items-center text-slate-500 font-medium">
                  <Calendar class="w-4 h-4 mr-1.5 text-slate-400" />
                  <span>{{ job.deadline || 'No date set' }}</span>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-1">
              <Button variant="ghost" size="icon" class="text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-full" @click.stop="editJob(job)">
                <Pencil class="w-5 h-5" />
              </Button>
              <Button variant="ghost" size="icon" class="text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-full" @click.stop="removeJob(job.id)">
                <Trash2 class="w-5 h-5" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <Dialog v-model:open="isDialogOpen">
        <DialogContent class="sm:max-w-[550px] p-0 overflow-hidden border-none shadow-2xl">
          <div class="bg-white p-6">
            <DialogHeader class="mb-4">
              <div class="flex items-center gap-2 mb-1">
                <Info class="w-4 h-4 text-orange-500" />
                <Label class="text-[10px] uppercase tracking-widest text-slate-400 font-bold">Posting Details</Label>
              </div>
              <DialogTitle class="text-2xl font-extrabold text-slate-900 leading-tight">
                {{ selectedJob?.title }}
              </DialogTitle>
            </DialogHeader>

            <ScrollArea class="h-[350px] pr-4">
              <div class="space-y-4">
                <p class="text-slate-600 leading-relaxed text-[15px]">
                  {{ selectedJob?.description }}
                </p>

                <Separator class="bg-slate-100" />

                <div class="grid grid-cols-2 gap-6">
                  <div class="space-y-1">
                    <Label class="text-slate-400 text-xs font-semibold">Budget Estimate</Label>
                    <div class="flex items-center font-bold text-slate-900">
                      <DollarSign class="w-4 h-4 mr-1 text-green-500" />
                      {{ selectedJob?.budget || 'TBD' }}
                    </div>
                  </div>
                  <div class="space-y-1">
                    <Label class="text-slate-400 text-xs font-semibold">Project Deadline</Label>
                    <div class="flex items-center font-bold text-slate-900">
                      <Calendar class="w-4 h-4 mr-1.5 text-blue-500" />
                      {{ selectedJob?.deadline || 'Flexible' }}
                    </div>
                  </div>
                </div>

                <Separator class="bg-slate-100" />

                <div v-if="selectedJob?.images?.length">
                  <div class="flex items-center gap-2 mb-3">
                    <ImageIcon class="w-4 h-4 text-slate-400" />
                    <Label class="text-slate-900 font-bold">Attached Gallery</Label>
                  </div>
                  <div class="grid grid-cols-3 gap-3">
                    <div v-for="img in selectedJob.images" :key="img.id" class="group relative">
                      <AspectRatio :ratio="1 / 1" class="bg-slate-100 rounded-lg overflow-hidden border border-slate-200">
                        <img
                          :src="'http://localhost:8000' + img.image"
                          class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                        />
                      </AspectRatio>
                    </div>
                  </div>
                </div>
              </div>
            </ScrollArea>
          </div>

          <div class="bg-slate-50 p-4 border-t border-slate-100 flex justify-end">
            <Button @click="isDialogOpen = false" class="bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg px-8">
              Close Preview
            </Button>
          </div>
        </DialogContent>
      </Dialog>

    </div>
  </div>
</template>