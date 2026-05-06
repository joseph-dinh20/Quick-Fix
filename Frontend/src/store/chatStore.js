// store/chatStore.js
import { defineStore } from "pinia";
import { ref, watch } from "vue";

// ─── Storage Keys ─────────────────────────────────────────────────────────────
// Using "v2" so the old quick-fix-chats-data key doesn't interfere.
const CHATS_KEY             = "quick-fix-chats-v2";
const PROVIDER_SNAPSHOTS_KEY = "quick-fix-provider-snapshots";
const JOB_SNAPSHOTS_KEY      = "quick-fix-job-snapshots";
const PENDING_CHAT_KEY       = "quick-fix-pending-chat-id";

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
//   linkedProviderId: number | null   — set for customer→provider chats
//   linkedJobId:      string | null   — set for provider→job-customer chats
//   messages: [{ id, senderId, text }]
//   lastMessageTime: string
//   unreadFor: string[]               — userIds with unread messages
// }

export const useChatStore = defineStore("chats", () => {
  const chats            = ref(safeLoad(CHATS_KEY, []));
  const providerSnapshots = ref(safeLoad(PROVIDER_SNAPSHOTS_KEY, {}));
  const jobSnapshots      = ref(safeLoad(JOB_SNAPSHOTS_KEY, {}));

  watch(chats,            (v) => localStorage.setItem(CHATS_KEY,              JSON.stringify(v)), { deep: true });
  watch(providerSnapshots,(v) => localStorage.setItem(PROVIDER_SNAPSHOTS_KEY, JSON.stringify(v)), { deep: true });
  watch(jobSnapshots,     (v) => localStorage.setItem(JOB_SNAPSHOTS_KEY,      JSON.stringify(v)), { deep: true });

  // ── Queries ────────────────────────────────────────────────────────────────

  /** Returns only chats where userId is a participant — used to scope the sidebar. */
  function getChatsForUser(userId) {
    if (!userId) return [];
    return chats.value.filter(
      (c) => c.participants && Object.prototype.hasOwnProperty.call(c.participants, userId)
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
   * Called when a CUSTOMER clicks "Message" on a provider card (ProviderList.vue).
   * De-duplicates on the customerId ↔ providerId pair.
   *
   * @param {Object} provider    — provider object from providerProfileStore
   * @param {Object} currentUser — useUserStore().currentUser  (the customer)
   * @returns {number} chat id
   */
  function openOrCreateProviderChat(provider, currentUser) {
    const customerId = currentUser.id;          // e.g. "u_001"
    const providerId = "p_" + provider.userID;  // e.g. "p_1413" — matches DEMO_PROVIDERS id

    const existing = chats.value.find(
      (c) =>
        c.participants &&
        Object.prototype.hasOwnProperty.call(c.participants, customerId) &&
        Object.prototype.hasOwnProperty.call(c.participants, providerId)
    );
    if (existing) return existing.id;

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
      linkedProviderId: provider.userID,  // numeric key into providerSnapshots
      linkedJobId: null,
      messages: [],
      lastMessageTime: "",
      unreadFor: [],
    };

    chats.value = [...chats.value, newChat];

    // Snapshot every field the "View Provider" dialog needs
    providerSnapshots.value = {
      ...providerSnapshots.value,
      [provider.userID]: {
        userID:        provider.userID,
        name:          provider.name,
        avatar:        provider.avatar        || "",
        price:         provider.price,
        aboutMe:       provider.aboutMe       || "",
        averageRating: provider.averageRating,
        jobsCompleted: provider.jobsCompleted,
        ratings:       provider.ratings       || [],
        languages:     provider.languages     || [],
        workPhotos:    provider.workPhotos    || [],
        datesBooked:   provider.datesBooked   || [],
      },
    };

    return newChat.id;
  }

  /**
   * Called when a PROVIDER clicks "Message Customer" on a job card (DemoJobListings.vue).
   * De-duplicates on the providerId ↔ customerId ↔ jobId triple.
   *
   * @param {Object} job          — job object (fallback-mapped shape)
   * @param {Object} customerInfo — { id, name, avatarUrl }
   * @param {Object} currentUser  — useUserStore().currentUser  (the provider)
   * @returns {number} chat id
   */
  function openOrCreateJobChat(job, customerInfo, currentUser) {
    const providerId = currentUser.id;     // e.g. "p_1413"
    const customerId = customerInfo.id;   // e.g. "u_001"
    const jobId      = job.job_id || job.id || String(Date.now());

    const existing = chats.value.find(
      (c) =>
        c.linkedJobId === jobId &&
        c.participants &&
        Object.prototype.hasOwnProperty.call(c.participants, providerId) &&
        Object.prototype.hasOwnProperty.call(c.participants, customerId)
    );
    if (existing) return existing.id;

    const newChat = {
      id: Date.now(),
      participants: {
        [providerId]: {
          userId:    providerId,
          name:      currentUser.name || "Provider",
          initials:  buildInitials(currentUser.name),
          avatarUrl: currentUser.avatar || "",
        },
        [customerId]: {
          userId:    customerId,
          name:      customerInfo.name || "Customer",
          initials:  buildInitials(customerInfo.name),
          avatarUrl: customerInfo.avatarUrl || "",
        },
      },
      linkedProviderId: null,
      linkedJobId: jobId,
      messages: [],
      lastMessageTime: "",
      unreadFor: [],
    };

    chats.value = [...chats.value, newChat];

    // Snapshot the entire job object for the "View Job Listing" dialog
    jobSnapshots.value = {
      ...jobSnapshots.value,
      [jobId]: { ...job },
    };

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