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

      <Dialog :open="isDialogOpen" @update:open="isDialogOpen = $event">
      <DialogContent class="max-w-2xl p-0 bg-white border-0 shadow-2xl overflow-hidden rounded-xl">
        <div v-if="selectedJob" class="p-8 max-h-[85vh] overflow-y-auto">

          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl md:text-3xl font-extrabold text-[#1a202c]">{{ selectedJob.title || 'Pest Control Help' }}</h2>
            <Button variant="ghost" size="icon" class="text-slate-700 hover:bg-slate-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            </Button>
          </div>

          <div v-if="selectedJob.images && selectedJob.images.length" class="relative flex items-center mb-10">
            <Button
              variant="ghost"
              size="icon"
              @click="scrollLeft"
              class="absolute -left-4 z-10 bg-white/80 hover:bg-white rounded-full shadow-sm h-8 w-8"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"></path></svg>
            </Button>

            <div ref="carousel" class="flex gap-4 overflow-x-auto snap-x snap-mandatory hide-scrollbar w-full px-4">
              <div
                v-for="img in selectedJob.images"
                :key="img.id"
                class="snap-center shrink-0 w-48 h-48 bg-slate-200 rounded-xl overflow-hidden"
              >
                <img
                  :src="img.image"
                  class="w-full h-full object-cover"
                />
              </div>
            </div>

            <Button
              variant="ghost"
              size="icon"
              @click="scrollRight"
              class="absolute -right-4 z-10 bg-white/80 hover:bg-white rounded-full shadow-sm h-8 w-8"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"></path></svg>
            </Button>
          </div>

          <hr class="border-slate-100 mb-8" />

          <div class="mb-8">
            <h3 class="font-bold text-[#1a202c] text-lg mb-6">Quick Details</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-4">

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                {{ selectedJob.customer?.name || 'Unknown customer' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><circle cx="12" cy="12" r="10"></circle><line x1="2" x2="22" y1="12" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                {{ selectedJob.languages || 'Not specified' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ selectedJob.request_type || 'Request type not provided' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                {{ selectedJob.urgency || 'Urgency not provided' }}
              </div>

              <div class="flex items-center text-slate-600 font-medium">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3">
                  <path d="M8 2v4"></path>
                  <path d="M16 2v4"></path>
                  <rect width="18" height="18" x="3" y="4" rx="2"></rect>
                  <path d="M3 10h18"></path>
                </svg>
                {{ selectedJob.deadline || 'No deadline provided' }}
              </div>

            </div>

            <div class="mt-6 pt-2">
              <span class="text-lg font-bold text-[#1a202c]">
                {{ selectedJob.budget ? `$${selectedJob.budget}` : 'Budget not provided' }}
              </span>
              <span class="text-base text-slate-500 font-medium"> budget</span>
            </div>
          </div>

          <hr class="border-slate-100 mb-8" />

          <div>
            <h3 class="font-bold text-[#1a202c] text-lg mb-4">About the Job</h3>
            <p class="text-slate-600 leading-relaxed whitespace-pre-wrap">{{ selectedJob.description || `Well, the bugs start comin' and they don't stop comin'
Fed to the plants and they just keep munchin'

Didn't make sense not to spray for fun
Your brain gets smart, but the pests just come

So much to do, so much to spray
So, what's wrong with clearing them away?

You'll never know if you don't check (check)
Your garden's gonna thrive if you protect!` }}</p>
          </div>

        </div>
      </DialogContent>
    </Dialog>

    </div>
  </div>
</template>