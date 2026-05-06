// store/chatStore.js
import { defineStore } from "pinia";
import { ref, watch } from "vue";

// ─── Storage Keys ─────────────────────────────────────────────────────────────
const CHATS_KEY = "quick-fix-chats-v2";
const PROVIDER_SNAPSHOTS_KEY = "quick-fix-provider-snapshots";
const JOB_SNAPSHOTS_KEY = "quick-fix-job-snapshots";
const PENDING_CHAT_KEY = "quick-fix-pending-chat-id";

// ─── Helpers ──────────────────────────────────────────────────────────────────
function safeLoad(key, fallback) {
    try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
    } catch {
        return fallback;
    }
}

function buildInitials(name) {
    const words = (name || "").trim().split(/\s+/);
    if (words.length >= 2)
        return (words[0][0] + words[words.length - 1][0]).toUpperCase();
    return (name || "??").slice(0, 2).toUpperCase();
}

// ─── Chat Shape ───────────────────────────────────────────────────────────────
// {
//   id: number
//   participants: {
//     [userId: string]: { userId, name, initials, avatarUrl }
//   }
//   linkedProviderId: number | null   — numeric providerId (from providers.json userID)
//   linkedJobId:      string | null   — jobId for the job snapshot
//   messages: [{ id, senderId, text }]
//   lastMessageTime: string
//   unreadFor: string[]               — userIds with unread messages
// }
//
// KEY INVARIANT: there is exactly ONE chat per (customerId, providerId) pair.
// Both openOrCreateProviderChat (customer side) and openOrCreateJobChat
// (provider side) look up the same chat by that pair and re-use it.
// When the provider side opens the chat it fills in linkedJobId + the job
// snapshot; when the customer side opens it it fills in linkedProviderId +
// the provider snapshot.  Both buttons ("View Provider" / "View Job Listing")
// therefore appear in a single, shared conversation.

export const useChatStore = defineStore("chats", () => {
    const chats = ref(safeLoad(CHATS_KEY, []));
    const providerSnapshots = ref(safeLoad(PROVIDER_SNAPSHOTS_KEY, {}));
    const jobSnapshots = ref(safeLoad(JOB_SNAPSHOTS_KEY, {}));

    watch(chats, (v) => localStorage.setItem(CHATS_KEY, JSON.stringify(v)), {
        deep: true,
    });
    watch(
        providerSnapshots,
        (v) => localStorage.setItem(PROVIDER_SNAPSHOTS_KEY, JSON.stringify(v)),
        { deep: true },
    );
    watch(
        jobSnapshots,
        (v) => localStorage.setItem(JOB_SNAPSHOTS_KEY, JSON.stringify(v)),
        { deep: true },
    );

    // ── Internal: canonical chat lookup by customer ↔ provider pair ───────────
    // customerId is always a "u_xxx" string.
    // providerId is always a "p_xxx" string.
    // This is the single source of truth for deduplication — used by BOTH
    // openOrCreateProviderChat and openOrCreateJobChat.
    function _findPairChat(customerId, providerId) {
        return (
            chats.value.find(
                (c) =>
                    c.participants &&
                    Object.prototype.hasOwnProperty.call(
                        c.participants,
                        customerId,
                    ) &&
                    Object.prototype.hasOwnProperty.call(
                        c.participants,
                        providerId,
                    ),
            ) ?? null
        );
    }

    // ── Queries ────────────────────────────────────────────────────────────────

    /** Returns only chats where userId is a participant — used to scope the sidebar. */
    function getChatsForUser(userId) {
        if (!userId) return [];
        return chats.value.filter(
            (c) =>
                c.participants &&
                Object.prototype.hasOwnProperty.call(c.participants, userId),
        );
    }

    function getProviderSnapshot(providerId) {
        return providerSnapshots.value[providerId] ?? null;
    }

    function getJobSnapshot(jobId) {
        return jobSnapshots.value[jobId] ?? null;
    }

    // ── Chat Creation ──────────────────────────────────────────────────────────

    /**
     * Called when a CUSTOMER clicks "Message" on a provider card or in OrderHistory.
     * De-duplicates on the customerId ↔ providerId pair (the "p_xxx" participant key).
     * If the chat already exists it updates the provider snapshot and linkedProviderId
     * so the "View Provider" button is always available even if the provider initiated
     * the chat first.
     *
     * @param {Object} provider    — provider object from providerProfileStore
     * @param {Object} currentUser — useUserStore().currentUser  (the customer)
     * @returns {number} chat id
     */
    function openOrCreateProviderChat(provider, currentUser) {
        const customerId = currentUser.id; // e.g. "u_001"
        const providerId = "p_" + provider.userID; // e.g. "p_1413"
        const numericProviderId = provider.userID; // e.g. 1413 — key into providerSnapshots

        // Always (re-)save the provider snapshot so "View Provider" has fresh data
        providerSnapshots.value = {
            ...providerSnapshots.value,
            [numericProviderId]: {
                userID: provider.userID,
                name: provider.name,
                avatar: provider.avatar || "",
                price: provider.price,
                aboutMe: provider.aboutMe || "",
                averageRating: provider.averageRating,
                jobsCompleted: provider.jobsCompleted,
                ratings: provider.ratings || [],
                languages: provider.languages || [],
                workPhotos: provider.workPhotos || [],
                datesBooked: provider.datesBooked || [],
            },
        };

        const existing = _findPairChat(customerId, providerId);
        if (existing) {
            // Patch in linkedProviderId if it was missing (e.g. provider created first)
            if (!existing.linkedProviderId) {
                existing.linkedProviderId = numericProviderId;
            }
            return existing.id;
        }

        const newChat = {
            id: Date.now(),
            participants: {
                [customerId]: {
                    userId: customerId,
                    name: currentUser.name || "Customer",
                    initials: buildInitials(currentUser.name),
                    avatarUrl: currentUser.avatar || "",
                },
                [providerId]: {
                    userId: providerId,
                    name: provider.name || "Provider",
                    initials: buildInitials(provider.name),
                    avatarUrl: provider.avatar || "",
                },
            },
            linkedProviderId: numericProviderId,
            linkedJobId: null,
            messages: [],
            lastMessageTime: "",
            unreadFor: [],
        };

        chats.value = [...chats.value, newChat];
        return newChat.id;
    }

    /**
     * Called when a PROVIDER clicks "Message Customer" on a job card or in
     * ProviderOrderHistory.
     * De-duplicates on the same customerId ↔ providerId pair.
     * If the chat already exists it updates the job snapshot and linkedJobId
     * so the "View Job Listing" button is always available even if the customer
     * initiated the chat first.
     *
     * @param {Object} job          — job object (fallback-mapped shape)
     * @param {Object} customerInfo — { id, name, avatarUrl }
     * @param {Object} currentUser  — useUserStore().currentUser  (the provider)
     * @returns {number} chat id
     */
    function openOrCreateJobChat(job, customerInfo, currentUser) {
        // currentUser.id is already "p_xxx" for providers
        const providerId = currentUser.id; // e.g. "p_1413"
        const customerId = customerInfo.id; // e.g. "u_001"
        const jobId = job.job_id || job.id || String(Date.now());

        // Always (re-)save the job snapshot so "View Job Listing" has fresh data
        jobSnapshots.value = {
            ...jobSnapshots.value,
            [jobId]: { ...job },
        };

        const existing = _findPairChat(customerId, providerId);
        if (existing) {
            // Patch in linkedJobId if it was missing (e.g. customer created first)
            if (!existing.linkedJobId) {
                existing.linkedJobId = jobId;
            }
            return existing.id;
        }

        const newChat = {
            id: Date.now(),
            participants: {
                [providerId]: {
                    userId: providerId,
                    name: currentUser.name || "Provider",
                    initials: buildInitials(currentUser.name),
                    avatarUrl: currentUser.avatar || "",
                },
                [customerId]: {
                    userId: customerId,
                    name: customerInfo.name || "Customer",
                    initials: buildInitials(customerInfo.name),
                    avatarUrl: customerInfo.avatarUrl || "",
                },
            },
            linkedProviderId: null, // will be filled when customer side opens the chat
            linkedJobId: jobId,
            messages: [],
            lastMessageTime: "",
            unreadFor: [],
        };

        chats.value = [...chats.value, newChat];
        return newChat.id;
    }

    // ── Navigation Handshake ───────────────────────────────────────────────────

    /** Write the chat id that ChatMessages should auto-select on mount. */
    function setPendingChat(chatId) {
        localStorage.setItem(PENDING_CHAT_KEY, String(chatId));
    }

    /** Read + clear the pending chat id (one-time consume). */
    function consumePendingChat() {
        const raw = localStorage.getItem(PENDING_CHAT_KEY);
        if (!raw) return null;
        localStorage.removeItem(PENDING_CHAT_KEY);
        return Number(raw);
    }

    return {
        chats,
        providerSnapshots,
        jobSnapshots,
        getChatsForUser,
        getProviderSnapshot,
        getJobSnapshot,
        openOrCreateProviderChat,
        openOrCreateJobChat,
        setPendingChat,
        consumePendingChat,
    };
});
