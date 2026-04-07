<script setup>
import { ref, onMounted } from "vue"
import { getMyJobs, deleteJob } from "../services/api"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Search, Calendar, Pencil, Trash2, ChevronDown } from "lucide-vue-next"

const jobs = ref([])

async function fetchJobs() {
  try {
    const res = await getMyJobs()
    jobs.value = res.data
  } catch (err) {
    console.error(err)
  }
}

// Delete a job
async function removeJob(jobId) {
  if (!confirm("Are you sure you want to delete this job?")) return
  try {
    await deleteJob(jobId)
    // Remove the job from local state
    jobs.value = jobs.value.filter(j => j.id !== jobId)
  } catch (err) {
    console.error(err)
  }
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
          <Button class="bg-orange-500 hover:bg-orange-600 text-white rounded-full px-6 py-2 shrink-0 h-auto">
            Search
          </Button>
        </div>

        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="bg-white border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg flex items-center gap-2 shadow-sm px-4">
              Sort by
              <ChevronDown class="w-4 h-4 text-slate-500 ml-1" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="w-40">
            <DropdownMenuItem>Newest</DropdownMenuItem>
            <DropdownMenuItem>Oldest</DropdownMenuItem>
            <DropdownMenuItem>Title (A-Z)</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div v-if="jobs.length" class="space-y-4">
        <Card 
          v-for="job in jobs" 
          :key="job.id" 
          class="p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white border-slate-200 shadow-sm rounded-xl hover:shadow-md transition-all"
        >
          
          <div>
            <h3 class="font-bold text-[#1a202c] text-[15px] mb-2.5">{{ job.title }}</h3>
            <div class="flex items-center gap-3 text-sm">
              
              <Badge 
                variant="outline" 
                :class="job.status === 'inactive' 
                  ? 'bg-red-50 text-red-600 border-red-200' 
                  : 'bg-green-50 text-green-600 border-green-200'"
                class="font-medium px-2.5 py-0.5 rounded-md"
              >
                {{ job.status === 'inactive' ? 'Inactive' : 'Active' }}
              </Badge>

              <div class="flex items-center text-slate-500 font-medium">
                <Calendar class="w-4 h-4 mr-1.5 text-slate-400" />
                <span>{{ job.deadline || 'No date set' }}</span>
              </div>

            </div>
          </div>

          <div class="flex items-center gap-1 mt-2 sm:mt-0">
            <Button variant="ghost" size="icon" class="text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-full">
              <Pencil class="w-5 h-5" />
            </Button>
            
            <Button variant="ghost" size="icon" class="text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-full" @click="removeJob(job.id)">
              <Trash2 class="w-5 h-5" />
            </Button>
          </div>

        </Card>
      </div>

      <div v-else class="flex flex-col items-center justify-center py-20 text-center bg-white border border-slate-200 border-dashed rounded-xl mt-4">
        <div class="bg-slate-50 p-4 rounded-full mb-4">
          <Search class="w-8 h-8 text-slate-400" />
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-1">No postings found</h3>
        <p class="text-slate-500">You haven't created any job postings yet.</p>
      </div>

    </div>
  </div>
</template>