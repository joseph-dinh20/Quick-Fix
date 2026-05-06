import { defineStore } from "pinia";
import { ref } from "vue";
import jobsData from "@/store/data/jobs.json";
import { useUserStore } from "@/store/userStore";

// ---------------------------------------------------------------------------
// DECISION STORAGE — stored under a single global key so ALL users see the
// same accept/reject outcomes regardless of who is logged in.
// ---------------------------------------------------------------------------
const DECISIONS_KEY = "jobApplicationDecisions";

function loadDecisionsFromStorage() {
    try {
        return JSON.parse(localStorage.getItem(DECISIONS_KEY) || "{}");
    } catch {
        return {};
    }
}

function saveDecisionsToStorage(decisions) {
    localStorage.setItem(DECISIONS_KEY, JSON.stringify(decisions));
}

export const useJobStore = defineStore(
    "job",
    () => {
        const jobList = ref(jobsData);
        const edits = ref({});
        const favorites = ref(new Set());
        const applications = ref({});

        // Reactive mirror of all globalApplications_<jobId> localStorage keys.
        // Shape: { [jobId]: ApplicationEntry[] }
        // Kept in sync by _mergeApplicationIntoGlobal and loadAllGlobalApplications.
        const globalApplicantsMap = ref({});

        // decisions shape: { [jobId]: { [providerUserId]: 'accepted' | 'rejected' } }
        // Loaded from and saved to a GLOBAL localStorage key (not per-user).
        const decisions = ref(loadDecisionsFromStorage());

        // ------------------------------------------------------------------
        // FAVORITES
        // ------------------------------------------------------------------
        function getFavoritesKey() {
            const userStore = useUserStore();
            return `favoritedJobs_${userStore.currentUser?.id || "guest"}`;
        }

        function loadFavorites() {
            favorites.value = new Set(
                JSON.parse(localStorage.getItem(getFavoritesKey()) || "[]"),
            );
        }

        function toggleFavorite(jobId) {
            if (favorites.value.has(jobId)) {
                favorites.value.delete(jobId);
            } else {
                favorites.value.add(jobId);
            }
            localStorage.setItem(
                getFavoritesKey(),
                JSON.stringify([...favorites.value]),
            );
        }

        function isFavorited(jobId) {
            return favorites.value.has(jobId);
        }

        // ------------------------------------------------------------------
        // APPLICATIONS (per-user persistence, provider-scoped)
        // ------------------------------------------------------------------
        function getApplicationsKey() {
            const userStore = useUserStore();
            return `applications_${userStore.currentUser?.id || "guest"}`;
        }

        function loadApplications() {
            applications.value = JSON.parse(
                localStorage.getItem(getApplicationsKey()) || "{}",
            );
        }

        function initApplications() {
            loadApplications();
        }

        function saveApplications() {
            localStorage.setItem(
                getApplicationsKey(),
                JSON.stringify(applications.value),
            );
        }

        function applyToJob(jobId, userId, formData = {}) {
            if (!applications.value[jobId]) {
                applications.value[jobId] = [];
            }

            const existing = applications.value[jobId].find(
                (entry) =>
                    (typeof entry === "string" ? entry : entry.userId) ===
                    userId,
            );
            if (existing) return false;

            applications.value[jobId].push({
                userId,
                proposedRate: formData.proposedRate ?? "",
                rateType: formData.rateType ?? "hourly",
                availableDate: formData.availableDate ?? "",
                availableTime: formData.availableTime ?? "",
                coverNote: formData.coverNote ?? "",
                appliedAt: new Date().toISOString(),
            });

            saveApplications();

            // Also persist into the GLOBAL applications store so the client can
            // see it without needing to be logged in as the provider.
            _mergeApplicationIntoGlobal(jobId, applications.value[jobId]);

            return true;
        }

        // Write a copy of this job's applicant list into a global key so every
        // user account can read it (clients need to see provider applications).
        function _mergeApplicationIntoGlobal(jobId, entries) {
            const globalKey = `globalApplications_${jobId}`;
            localStorage.setItem(globalKey, JSON.stringify(entries));
            // Keep the reactive map in sync so computed properties update.
            globalApplicantsMap.value = {
                ...globalApplicantsMap.value,
                [jobId]: entries,
            };
        }

        // Read all applicants for a job — from the reactive map (which mirrors localStorage).
        function getGlobalApplicantsForJob(jobId) {
            // Return from the reactive map so Vue computed properties track this correctly.
            if (globalApplicantsMap.value[jobId] !== undefined) {
                return globalApplicantsMap.value[jobId];
            }
            // Fallback: read from localStorage for any jobId not yet in the map.
            try {
                return JSON.parse(
                    localStorage.getItem(`globalApplications_${jobId}`) || "[]",
                );
            } catch {
                return [];
            }
        }

        // Populate globalApplicantsMap from localStorage for all known jobs.
        // Call this on mount in any client-side component that needs to see applications.
        function loadAllGlobalApplications() {
            const updated = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith("globalApplications_")) {
                    const jobId = key.replace("globalApplications_", "");
                    try {
                        updated[jobId] = JSON.parse(
                            localStorage.getItem(key) || "[]",
                        );
                    } catch {
                        updated[jobId] = [];
                    }
                }
            }
            globalApplicantsMap.value = updated;
        }

        // Return all job IDs that have at least one application (globally)
        function getAllAppliedJobIds() {
            const result = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith("globalApplications_")) {
                    const jobId = key.replace("globalApplications_", "");
                    const entries = getGlobalApplicantsForJob(jobId);
                    if (entries.length > 0) result.push(jobId);
                }
            }
            return result;
        }

        function hasApplied(jobId, userId) {
            return (
                applications.value[jobId]?.some(
                    (entry) =>
                        (typeof entry === "string" ? entry : entry.userId) ===
                        userId,
                ) || false
            );
        }

        function getApplicationData(jobId, userId) {
            const entry = applications.value[jobId]?.find(
                (e) => (typeof e === "string" ? e : e.userId) === userId,
            );
            return typeof entry === "object" ? entry : null;
        }

        function getAppliedJobIds(userId) {
            return Object.entries(applications.value)
                .filter(([jobId, entries]) =>
                    entries.some(
                        (entry) =>
                            (typeof entry === "string"
                                ? entry
                                : entry.userId) === userId,
                    ),
                )
                .map(([jobId]) => jobId);
        }

        function unapplyFromJob(jobId, userId) {
            if (!applications.value[jobId]) return;

            applications.value[jobId] = applications.value[jobId].filter(
                (entry) =>
                    (typeof entry === "string" ? entry : entry.userId) !==
                    userId,
            );

            if (applications.value[jobId].length === 0) {
                delete applications.value[jobId];
            }

            saveApplications();
            _mergeApplicationIntoGlobal(jobId, applications.value[jobId] || []);
        }

        // ------------------------------------------------------------------
        // DECISIONS  (accept / reject — global, keyed by jobId + providerUserId)
        // ------------------------------------------------------------------

        /**
         * Record a decision for a specific applicant on a specific job.
         * @param {string} jobId
         * @param {string} providerUserId  — the `userId` stored in the application entry
         * @param {'accepted'|'rejected'} decision
         */
        function setDecision(jobId, providerUserId, decision) {
            if (!decisions.value[jobId]) {
                decisions.value[jobId] = {};
            }
            decisions.value[jobId][providerUserId] = decision;
            saveDecisionsToStorage(decisions.value);
        }

        /**
         * Get the decision for a specific applicant.
         * Returns 'accepted' | 'rejected' | null
         */
        function getDecision(jobId, providerUserId) {
            return decisions.value[jobId]?.[providerUserId] ?? null;
        }

        /**
         * Reload decisions from localStorage (call after switching users).
         */
        function loadDecisions() {
            decisions.value = loadDecisionsFromStorage();
        }

        // ------------------------------------------------------------------
        // JOB EDITING
        // ------------------------------------------------------------------
        function saveJob(jobId, updates) {
            const existing = edits.value[jobId] || {};
            edits.value = {
                ...edits.value,
                [jobId]: { ...existing, ...updates },
            };
        }

        function getMergedJob(jobId) {
            const seed = jobsData.find((j) => j.job_id === jobId);
            if (!seed) return null;
            const edit = edits.value[jobId] || {};
            return { ...seed, ...edit };
        }

        function getMergedJobs() {
            return jobsData.map((j) => getMergedJob(j.job_id));
        }

        function getJobsByUser(userId) {
            return getMergedJobs().filter((job) => job.user_id === userId);
        }

        function getJobsByProvider(providerId) {
            return getMergedJobs().filter(
                (job) => job.provider_id === providerId,
            );
        }

        function getJobsByService(service) {
            return getMergedJobs().filter((job) => job.service === service);
        }

        function getJobsByUrgency(urgency) {
            return getMergedJobs().filter((job) => job.urgency === urgency);
        }

        function getFavoritedJobs() {
            return getMergedJobs().filter((job) => isFavorited(job.job_id));
        }

        /**
         * Return jobs that have been ACCEPTED for a specific provider user id.
         * Used by DemoAssignedJobs.
         */
        function getAcceptedJobsForProvider(providerUserId) {
            loadDecisions(); // always fresh
            const result = [];
            for (const [jobId, jobDecisions] of Object.entries(
                decisions.value,
            )) {
                if (jobDecisions[providerUserId] === "accepted") {
                    const job = getMergedJob(jobId);
                    if (job) result.push(job);
                }
            }
            return result;
        }

        return {
            jobList,
            edits,
            favorites,
            decisions,
            saveJob,
            getMergedJob,
            getMergedJobs,
            getJobsByUser,
            getJobsByProvider,
            getJobsByService,
            getJobsByUrgency,
            getFavoritedJobs,
            loadFavorites,
            toggleFavorite,
            isFavorited,
            applications,
            applyToJob,
            hasApplied,
            getAppliedJobIds,
            loadApplications,
            initApplications,
            unapplyFromJob,
            getApplicationData,
            getGlobalApplicantsForJob,
            getAllAppliedJobIds,
            loadAllGlobalApplications,
            setDecision,
            getDecision,
            loadDecisions,
            getAcceptedJobsForProvider,
        };
    },
    {
        persist: {
            pick: ["edits", "applications"],
        },
    },
);
