<template>
    <div class="min-h-screen text-slate-900 p-6 md:p-12 font-sans">
        <div class="max-w-4xl mx-auto">
            <!-- Header -->
            <div class="flex justify-between items-center mb-8">
                <div>
                    <h1
                        class="text-3xl font-extrabold tracking-tight text-slate-900">
                        Job Applications
                    </h1>
                    <p class="text-slate-500 mt-1 text-sm">
                        Review and respond to provider applications for your
                        jobs.
                    </p>
                </div>
            </div>

            <!-- Empty state -->
            <div
                v-if="!loading && allApplicationCards.length === 0"
                class="text-center py-20 text-slate-400">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="48"
                    height="48"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="mx-auto mb-4 opacity-40">
                    <path
                        d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" x2="8" y1="13" y2="13"></line>
                    <line x1="16" x2="8" y1="17" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <p class="text-lg font-medium">No applications yet</p>
                <p class="text-sm mt-1">
                    When providers apply to your jobs, they'll appear here.
                </p>
            </div>

            <!-- Application Cards -->
            <div v-else class="flex flex-col gap-4">
                <Card
                    v-for="card in allApplicationCards"
                    :key="card.key"
                    class="border border-slate-200 shadow-sm rounded-xl overflow-hidden">
                    <div
                        class="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <!-- Left: info -->
                        <div class="flex-1 min-w-0">
                            <p
                                class="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-1">
                                Application
                            </p>
                            <h3
                                class="text-base font-bold text-slate-900 leading-snug">
                                Application for
                                <span class="text-primary">{{
                                    card.jobTitle
                                }}</span>
                                from
                                <span class="text-slate-700">{{
                                    card.providerName
                                }}</span>
                            </h3>
                            <div
                                class="flex items-center gap-2 mt-2 text-sm text-slate-500">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="14"
                                    height="14"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <path
                                        d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path>
                                    <circle cx="12" cy="10" r="3"></circle>
                                </svg>
                                {{ card.jobCity }} · {{ card.jobService }}
                                <span class="text-slate-300">·</span>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="14"
                                    height="14"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <polyline
                                        points="12 6 12 12 16 14"></polyline>
                                </svg>
                                {{ formatDate(card.appliedAt) }}
                            </div>
                        </div>

                        <!-- Right: status badge + button -->
                        <div class="flex items-center gap-3 shrink-0">
                            <!-- Status Badge -->
                            <span
                                :class="[
                                    'text-xs font-bold px-3 py-1.5 rounded-full border',
                                    card.decision === 'accepted'
                                        ? 'bg-green-50 text-green-700 border-green-200'
                                        : card.decision === 'rejected'
                                          ? 'bg-red-50 text-red-600 border-red-200'
                                          : 'bg-slate-100 text-slate-500 border-slate-200',
                                ]">
                                {{
                                    card.decision === "accepted"
                                        ? "Accepted"
                                        : card.decision === "rejected"
                                          ? "Declined"
                                          : "Not Decided"
                                }}
                            </span>

                            <Button
                                @click="openApplicationDialog(card)"
                                size="sm"
                                class="font-semibold">
                                View Application
                            </Button>
                        </div>
                    </div>
                </Card>
            </div>
        </div>

        <!-- =========================================================
         VIEW APPLICATION DIALOG
    ========================================================= -->
        <Dialog :open="isViewOpen" @update:open="isViewOpen = $event">
            <DialogContent
                class="max-w-2xl p-0 bg-white border-0 shadow-2xl overflow-hidden rounded-xl">
                <div v-if="selectedCard" class="max-h-[90vh] overflow-y-auto">
                    <!-- Top bar -->
                    <div class="px-8 pt-8 pb-6 border-b border-slate-100">
                        <p
                            class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">
                            Application Review
                        </p>
                        <h2 class="text-xl font-extrabold text-slate-900">
                            {{ selectedCard.jobTitle }}
                        </h2>
                        <p class="text-sm text-slate-500 mt-0.5">
                            {{ selectedCard.jobCity }} ·
                            {{ selectedCard.jobService }}
                        </p>
                    </div>

                    <div class="px-8 py-6 flex flex-col gap-6">
                        <!-- PROVIDER SECTION -->
                        <div
                            class="flex items-start gap-5 p-5 rounded-xl bg-slate-50 border border-slate-100">
                            <!-- Avatar -->
                            <div class="shrink-0">
                                <div
                                    class="w-14 h-14 rounded-full overflow-hidden bg-slate-200 border-2 border-white shadow">
                                    <img
                                        v-if="selectedCard.providerAvatar"
                                        :src="selectedCard.providerAvatar"
                                        :alt="selectedCard.providerName"
                                        class="w-full h-full object-cover" />
                                    <div
                                        v-else
                                        class="w-full h-full flex items-center justify-center text-slate-400 text-xl font-bold">
                                        {{
                                            selectedCard.providerName?.charAt(
                                                0,
                                            ) || "?"
                                        }}
                                    </div>
                                </div>
                            </div>

                            <!-- Name + ratings -->
                            <div class="flex-1 min-w-0">
                                <p
                                    class="font-bold text-slate-900 text-base leading-tight">
                                    {{ selectedCard.providerName }}
                                </p>
                                <div
                                    class="flex items-center gap-1 mt-1 text-sm text-slate-500"
                                    v-if="selectedCard.providerRating">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="14"
                                        height="14"
                                        viewBox="0 0 24 24"
                                        fill="currentColor"
                                        class="text-amber-400">
                                        <polygon
                                            points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                                    </svg>
                                    <span
                                        class="font-semibold text-slate-700"
                                        >{{ selectedCard.providerRating }}</span
                                    >
                                    <span class="text-slate-400"
                                        >({{
                                            selectedCard.providerReviews
                                        }}
                                        reviews)</span
                                    >
                                </div>
                                <p
                                    v-if="selectedCard.providerJobsCompleted"
                                    class="text-xs text-slate-400 mt-0.5">
                                    {{ selectedCard.providerJobsCompleted }}
                                    jobs completed
                                </p>
                            </div>

                            <!-- View Profile -->
                            <div class="shrink-0">
                                <Dialog v-model:open="isProfileOpen">
                                    <DialogTrigger as-child>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            class="font-semibold">
                                            View Profile
                                        </Button>
                                    </DialogTrigger>
                                    <DialogContent
                                        class="m-0 h-full max-h-[95vh] max-w-lg gap-0 p-0">
                                        <DialogHeader class="sr-only">
                                            <DialogTitle
                                                >Provider Profile</DialogTitle
                                            >
                                            <DialogDescription
                                                >Profile
                                                details</DialogDescription
                                            >
                                        </DialogHeader>
                                        <ScrollArea class="h-full max-h-full">
                                            <div class="p-4">
                                                <Provider
                                                    v-if="selectedProviderObj"
                                                    :provider="
                                                        selectedProviderObj
                                                    "
                                                    @select="
                                                        isProfileOpen = false
                                                    " />
                                                <div
                                                    v-else
                                                    class="p-8 text-center text-slate-400">
                                                    Provider profile not found.
                                                </div>
                                            </div>
                                        </ScrollArea>
                                    </DialogContent>
                                </Dialog>
                            </div>
                        </div>

                        <!-- APPLICATION DETAILS SECTION -->
                        <div
                            v-if="selectedCard.appData"
                            class="rounded-xl border border-slate-100 overflow-hidden">
                            <div
                                class="px-5 py-3 bg-slate-50 border-b border-slate-100">
                                <p
                                    class="text-xs font-bold uppercase tracking-widest text-slate-500">
                                    Application Details
                                </p>
                            </div>
                            <div class="p-5 flex flex-col gap-4">
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <p
                                            class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">
                                            Proposed Rate
                                        </p>
                                        <p
                                            class="font-bold text-slate-900 text-base">
                                            ${{
                                                selectedCard.appData
                                                    .proposedRate || "—"
                                            }}
                                            <span
                                                class="font-normal text-slate-500 text-sm capitalize">
                                                /
                                                {{
                                                    selectedCard.appData
                                                        .rateType || "hourly"
                                                }}
                                            </span>
                                        </p>
                                    </div>
                                    <div>
                                        <p
                                            class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">
                                            Availability
                                        </p>
                                        <p class="font-semibold text-slate-800">
                                            {{
                                                selectedCard.appData
                                                    .availableDate || "—"
                                            }}
                                            <span
                                                v-if="
                                                    selectedCard.appData
                                                        .availableTime
                                                "
                                                class="font-normal text-slate-500 text-sm">
                                                at
                                                {{
                                                    selectedCard.appData
                                                        .availableTime
                                                }}
                                            </span>
                                        </p>
                                    </div>
                                </div>

                                <div v-if="selectedCard.appData.coverNote">
                                    <p
                                        class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">
                                        Cover Note
                                    </p>
                                    <p
                                        class="text-sm text-slate-600 bg-slate-50 rounded-lg p-4 leading-relaxed border border-slate-100">
                                        {{ selectedCard.appData.coverNote }}
                                    </p>
                                </div>

                                <p class="text-xs text-slate-400">
                                    Applied
                                    {{
                                        selectedCard.appData.appliedAt
                                            ? new Date(
                                                  selectedCard.appData
                                                      .appliedAt,
                                              ).toLocaleDateString("en-US", {
                                                  month: "short",
                                                  day: "numeric",
                                                  year: "numeric",
                                              })
                                            : ""
                                    }}
                                </p>
                            </div>
                        </div>

                        <!-- Current status display -->
                        <div
                            v-if="selectedCard.decision"
                            class="rounded-xl p-4 flex items-center gap-3"
                            :class="
                                selectedCard.decision === 'accepted'
                                    ? 'bg-green-50 border border-green-200'
                                    : 'bg-red-50 border border-red-200'
                            ">
                            <svg
                                v-if="selectedCard.decision === 'accepted'"
                                xmlns="http://www.w3.org/2000/svg"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="text-green-600 shrink-0">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            <svg
                                v-else
                                xmlns="http://www.w3.org/2000/svg"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="text-red-500 shrink-0">
                                <line x1="18" x2="6" y1="6" y2="18"></line>
                                <line x1="6" x2="18" y1="6" y2="18"></line>
                            </svg>
                            <p
                                class="text-sm font-semibold"
                                :class="
                                    selectedCard.decision === 'accepted'
                                        ? 'text-green-700'
                                        : 'text-red-600'
                                ">
                                You have
                                {{
                                    selectedCard.decision === "accepted"
                                        ? "accepted"
                                        : "declined"
                                }}
                                this application.
                            </p>
                        </div>

                        <!-- Accept / Decline Buttons -->
                        <div class="flex gap-3 pt-2">
                            <Button
                                @click="promptDecision('accepted')"
                                class="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold"
                                :disabled="
                                    selectedCard.decision === 'accepted'
                                ">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2.5"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="mr-2">
                                    <polyline
                                        points="20 6 9 17 4 12"></polyline>
                                </svg>
                                Accept
                            </Button>
                            <Button
                                @click="promptDecision('rejected')"
                                variant="outline"
                                class="flex-1 border-red-200 text-red-600 hover:bg-red-50 font-bold"
                                :disabled="
                                    selectedCard.decision === 'rejected'
                                ">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2.5"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="mr-2">
                                    <line x1="18" x2="6" y1="6" y2="18"></line>
                                    <line x1="6" x2="18" y1="6" y2="18"></line>
                                </svg>
                                Decline
                            </Button>
                        </div>
                    </div>
                </div>
            </DialogContent>
        </Dialog>

        <!-- =========================================================
         CONFIRMATION DIALOG
    ========================================================= -->
        <Dialog :open="isConfirmOpen" @update:open="isConfirmOpen = $event">
            <DialogContent class="max-w-sm rounded-2xl">
                <div class="p-2">
                    <div class="flex items-center gap-3 mb-4">
                        <div
                            class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
                            :class="
                                pendingDecision === 'accepted'
                                    ? 'bg-green-100'
                                    : 'bg-red-100'
                            ">
                            <svg
                                v-if="pendingDecision === 'accepted'"
                                xmlns="http://www.w3.org/2000/svg"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="text-green-600">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            <svg
                                v-else
                                xmlns="http://www.w3.org/2000/svg"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="text-red-500">
                                <line x1="18" x2="6" y1="6" y2="18"></line>
                                <line x1="6" x2="18" y1="6" y2="18"></line>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-slate-900">
                                Confirm Decision
                            </h3>
                            <p class="text-sm text-slate-500 mt-0.5">
                                Are you sure you want to
                                <strong>{{
                                    pendingDecision === "accepted"
                                        ? "accept"
                                        : "decline"
                                }}</strong>
                                this application?
                            </p>
                        </div>
                    </div>

                    <div class="flex gap-2 mt-4">
                        <Button
                            variant="outline"
                            class="flex-1"
                            @click="isConfirmOpen = false">
                            Cancel
                        </Button>
                        <Button
                            class="flex-1 font-bold"
                            :class="
                                pendingDecision === 'accepted'
                                    ? 'bg-green-600 hover:bg-green-700 text-white'
                                    : 'bg-red-600 hover:bg-red-700 text-white'
                            "
                            @click="confirmDecision">
                            Confirm
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useJobStore } from "@/store/jobStore.js";
import { useUserStore, ALL_USERS } from "@/store/userStore";
import { useProviderProfileStore } from "@/store/providerProfileStore";
import { useProviderRatingsStore } from "@/store/providerRatingsStore";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogTrigger,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import Provider from "@/components/Provider.vue";

const jobStore = useJobStore();
const userStore = useUserStore();
const providerProfileStore = useProviderProfileStore();
const ratingsStore = useProviderRatingsStore();

// ── state ──────────────────────────────────────────────────────────────────
const loading = ref(true);
const isViewOpen = ref(false);
const isConfirmOpen = ref(false);
const isProfileOpen = ref(false);
const selectedCard = ref(null);
const pendingDecision = ref(null); // 'accepted' | 'rejected'

// ── helpers ────────────────────────────────────────────────────────────────
function formatDate(dateStr) {
    if (!dateStr) return "";
    return new Date(dateStr).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
}

/**
 * Look up a provider by their *user* id (e.g. "p_3749") or their numeric
 * providerId (e.g. 3749).  Returns the provider object from the profile store.
 */
function findProvider(providerUserId) {
    // providerUserId is like "p_3749" — strip the "p_" prefix to get numeric id
    const numericId =
        typeof providerUserId === "string" && providerUserId.startsWith("p_")
            ? parseInt(providerUserId.replace("p_", ""), 10)
            : parseInt(providerUserId, 10);

    return (
        providerProfileStore
            .getMergedProviders()
            .find((p) => p.userID === numericId) || null
    );
}

function getProviderNameFromUserId(userId) {
    // First check ALL_USERS (which has the demo provider accounts)
    const userAccount = ALL_USERS.find((u) => u.id === userId);
    if (userAccount) return userAccount.name;
    return "Unknown Provider";
}

// ── build cards ────────────────────────────────────────────────────────────
const allApplicationCards = computed(() => {
    const clientId = userStore.currentUser?.id;
    if (!clientId) return [];

    // Get all jobs that belong to this client
  const myJobs = jobStore
        .getMergedJobs()
        .filter((j) => j.user_id === clientId);

        
    console.log(myJobs)

    const cards = [];

  for (const job of myJobs) {
        // Fetch applicants from the global store (persisted by providers when they apply)
    const applicants = jobStore.getGlobalApplicantsForJob(job.job_id);
        
        for (const entry of applicants) {
            const providerUserId =
                typeof entry === "string" ? entry : entry.userId;

            console.log("ID" + providerUserId);
            const appData = typeof entry === "object" ? entry : null;
            const decision = jobStore.getDecision(job.job_id, providerUserId);

            const providerObj = findProvider(providerUserId);
            const providerName =
                providerObj?.name || getProviderNameFromUserId(providerUserId);
            const providerAvatar = providerObj?.avatar || "";
            const providerRating =
                ratingsStore.getAverageFor(providerObj?.userID) || null;
            const providerReviews = providerObj?.userID
                ? ratingsStore.getRatingsFor(providerObj.userID).length
                : 0;
            const providerJobsCompleted = providerObj?.jobsCompleted || null;

            cards.push({
                key: `${job.job_id}_${providerUserId}`,
                jobId: job.job_id,
                jobTitle: job.title,
                jobCity: job.city,
                jobService: job.service,
                providerUserId,
                providerName,
                providerAvatar,
                providerRating,
                providerReviews,
                providerJobsCompleted,
                providerObj,
                appData,
                appliedAt: appData?.appliedAt || null,
                decision,
            });
        }
    }

    return cards;
});

// The full provider object for "View Profile" dialog
const selectedProviderObj = computed(
    () => selectedCard.value?.providerObj || null,
);

// ── actions ────────────────────────────────────────────────────────────────
function openApplicationDialog(card) {
    // Refresh the decision from store before showing
    const freshDecision = jobStore.getDecision(card.jobId, card.providerUserId);
    selectedCard.value = { ...card, decision: freshDecision };
    isViewOpen.value = true;
}

function promptDecision(decision) {
    pendingDecision.value = decision;
    isConfirmOpen.value = true;
}

function confirmDecision() {
    if (!selectedCard.value || !pendingDecision.value) return;

    jobStore.setDecision(
        selectedCard.value.jobId,
        selectedCard.value.providerUserId,
        pendingDecision.value,
    );

    // Update the selected card reactively
    selectedCard.value = {
        ...selectedCard.value,
        decision: pendingDecision.value,
    };

    isConfirmOpen.value = false;
    pendingDecision.value = null;
}

// ── lifecycle ──────────────────────────────────────────────────────────────
onMounted(() => {
    jobStore.loadAllGlobalApplications(); // populate reactive map from localStorage
    jobStore.loadDecisions();
    loading.value = false;
});
</script>