<template>
  <div class="min-h-screen bg-slate-0 text-slate-900 p-6 md:p-12 font-sans relative">
    <div class="max-w-5xl mx-auto">

      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight">My Applications</h1>

        <Button
          variant="ghost"
          size="icon"
          class="text-slate-700"
          @click="navigate('#/DemoMap?view=jobs')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon>
            <line x1="9" x2="9" y1="3" y2="18"></line>
            <line x1="15" x2="15" y1="6" y2="21"></line>
          </svg>
        </Button>
      </div>

      <!-- Empty state -->
      <div v-if="filteredJobs.length === 0" class="text-center text-slate-500 mt-10">
        You haven't applied to any jobs yet.
      </div>

      <!-- Job list -->
      <div v-else class="flex flex-col gap-5">

        <Card
          v-for="job in filteredJobs"
          :key="job.job_id"
          class="flex flex-col sm:flex-row items-start sm:items-center p-4 shadow-sm border-slate-200 gap-6"
        >

          <!-- image placeholder -->
          <div class="w-full sm:w-48 h-32 bg-slate-100 rounded-lg overflow-hidden flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"
              viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="text-slate-300">
              <rect width="18" height="18" x="3" y="3" rx="2"></rect>
              <circle cx="9" cy="9" r="2"></circle>
              <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
            </svg>
          </div>

          <!-- content -->
          <div class="flex-1">
            <h3 class="text-lg font-bold">{{ job.title }}</h3>

            <p class="text-sm text-slate-500 mt-1">
              {{ job.city }} · {{ job.service }}
            </p>

            <!-- Application status badge (NOT the job's open/in-progress/done status) -->
            <div class="mt-2">
              <span
                :class="[
                  'inline-block text-xs font-bold px-3 py-1 rounded-full border',
                  applicationStatus(job.job_id) === 'Accepted'
                    ? 'bg-green-50 text-green-700 border-green-200'
                    : applicationStatus(job.job_id) === 'Rejected'
                    ? 'bg-red-50 text-red-600 border-red-200'
                    : 'bg-yellow-50 text-yellow-700 border-yellow-200'
                ]"
              >
                {{ applicationStatus(job.job_id) }}
              </span>
            </div>

            <div class="mt-2 font-bold text-slate-900">
              ${{ job.price || job.budget || 0 }}
            </div>
          </div>

          <!-- actions -->
          <div class="flex flex-col gap-2">
            <Button @click="openJob(job)">
              View
            </Button>

            <Button
              variant="outline"
              @click="unapply(job.job_id)"
            >
              Remove
            </Button>
          </div>

        </Card>
      </div>

    </div>

    <!-- view modal -->
    <Dialog :open="isDialogOpen" @update:open="isDialogOpen = $event">
      <DialogContent class="max-w-xl">
        <div v-if="selectedJob">
          <h2 class="text-xl font-bold mb-1">{{ selectedJob.title }}</h2>
          <p class="text-sm text-slate-500 mb-5">{{ selectedJob.city }} · {{ selectedJob.service }}</p>

          <p class="text-slate-600 text-sm leading-relaxed mb-6">{{ selectedJob.description }}</p>

          <template v-if="selectedAppData">
            <hr class="border-slate-100 mb-5" />
            <h3 class="font-bold text-slate-800 mb-4">Your Application</h3>
            <div class="grid grid-cols-2 gap-4 text-sm mb-4">
              <div>
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-0.5">Proposed Rate</p>
                <p class="font-semibold text-slate-800">
                  ${{ selectedAppData.proposedRate || '—' }}
                  <span class="font-normal text-slate-500 capitalize"> / {{ selectedAppData.rateType || 'hourly' }}</span>
                </p>
              </div>
              <div>
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-0.5">Availability</p>
                <p class="font-semibold text-slate-800">
                  {{ selectedAppData.availableDate || '—' }}
                  <span v-if="selectedAppData.availableTime" class="font-normal text-slate-500"> at {{ selectedAppData.availableTime }}</span>
                </p>
              </div>
            </div>
            <div v-if="selectedAppData.coverNote">
              <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Cover Note</p>
              <p class="text-sm text-slate-600 bg-slate-50 rounded-lg p-3 leading-relaxed">{{ selectedAppData.coverNote }}</p>
            </div>
            <p class="text-xs text-slate-400 mt-4">
              Applied {{ selectedAppData.appliedAt ? new Date(selectedAppData.appliedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '' }}
            </p>
          </template>

          <!-- Application status inside modal -->
          <div class="mt-5 pt-4 border-t border-slate-100">
            <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Application Status</p>
            <span
              :class="[
                'inline-block text-sm font-bold px-4 py-1.5 rounded-full border',
                applicationStatus(selectedJob.job_id) === 'Accepted'
                  ? 'bg-green-50 text-green-700 border-green-200'
                  : applicationStatus(selectedJob.job_id) === 'Rejected'
                  ? 'bg-red-50 text-red-600 border-red-200'
                  : 'bg-yellow-50 text-yellow-700 border-yellow-200'
              ]"
            >
              {{ applicationStatus(selectedJob.job_id) }}
            </span>
          </div>
        </div>
      </DialogContent>
    </Dialog>

  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useJobStore } from "@/store/jobStore";
import { useUserStore } from "@/store/userStore";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent } from "@/components/ui/dialog";

const jobStore = useJobStore();
const userStore = useUserStore();

const selectedJob = ref(null);
const isDialogOpen = ref(false);
const ready = ref(false);

// ensure applications and decisions are loaded fresh
onMounted(() => {
  jobStore.initApplications();
  jobStore.loadDecisions();
  ready.value = true;
});

// Only jobs current user applied to
const filteredJobs = computed(() => {
  const userId = userStore.currentUser?.id;
  if (!userId) return [];

  const appliedIds = jobStore.getAppliedJobIds(userId);

  return jobStore.getMergedJobs().filter(job =>
    appliedIds.includes(job.job_id)
  );
});

/**
 * Derive a human-readable application status for a given jobId.
 * The decision is stored globally keyed by jobId + providerUserId.
 * Returns: 'Accepted' | 'Rejected' | 'Applied'
 */
function applicationStatus(jobId) {
  const userId = userStore.currentUser?.id;
  if (!userId) return 'Applied';
  const decision = jobStore.getDecision(jobId, userId);
  if (decision === 'accepted') return 'Accepted';
  if (decision === 'rejected') return 'Rejected';
  return 'Applied';
}

// UI actions
function openJob(job) {
  selectedJob.value = job;
  isDialogOpen.value = true;
}

const selectedAppData = computed(() => {
  if (!selectedJob.value) return null;
  const userId = userStore.currentUser?.id;
  return jobStore.getApplicationData(selectedJob.value.job_id, userId);
});

function unapply(jobId) {
  const userId = userStore.currentUser?.id;
  if (!userId) return;

  jobStore.unapplyFromJob(jobId, userId);
}

function navigate(path) {
  window.location.hash = path.replace(/^#\//, "");
}
</script>