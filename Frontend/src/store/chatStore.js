// store/chatStore.js
import { defineStore } from "pinia";
import { ref, watch } from "vue";

// ─── Storage Keys ────────────────────────────────────────────────────────────
const CHATS_KEY = "quick-fix-chats-data";
const SNAPSHOTS_KEY = "quick-fix-provider-snapshots";
const PENDING_CHAT_KEY = "quick-fix-pending-chat-id";

// ─── Default seed chats (shown before any real chats are created) ─────────────
const DEFAULT_CHATS = [
    
];

// ─── Helpers ──────────────────────────────────────────────────────────────────
function loadFromStorage(key, fallback) {
    try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
    } catch {
        return fallback;
    }
}

function buildInitials(name) {
    const words = (name || "").trim().split(/\s+/);
    if (words.length >= 2) {
        return (words[0][0] + words[words.length - 1][0]).toUpperCase();
    }
    return (name || "??").slice(0, 2).toUpperCase();
}

// ─── Store ────────────────────────────────────────────────────────────────────
export const useChatStore = defineStore("chats", () => {
    // The full list of chat threads.
    // Each chat may have a `providerId` field that links to a provider snapshot.
    const chats = ref(loadFromStorage(CHATS_KEY, DEFAULT_CHATS));

    // Provider data snapshots keyed by provider.userID (number).
    // Stored so that "View Provider" works even after page reload.
    const providerSnapshots = ref(loadFromStorage(SNAPSHOTS_KEY, {}));

    // Persist chats to localStorage whenever they change
    watch(
        chats,
        (val) => {
            localStorage.setItem(CHATS_KEY, JSON.stringify(val));
        },
        { deep: true },
    );

    // Persist provider snapshots whenever they change
    watch(
        providerSnapshots,
        (val) => {
            localStorage.setItem(SNAPSHOTS_KEY, JSON.stringify(val));
        },
        { deep: true },
    );

    /**
     * Creates a new chat for a provider, or returns the id of the existing one.
     * Also saves a provider snapshot so the profile can be re-opened later.
     *
     * @param {Object} provider - A provider object from providerProfileStore / providers.json
     * @returns {number} The chat id (existing or newly created)
     */
    function openOrCreateChat(provider) {
        // Return existing chat if one already exists for this provider
        const existing = chats.value.find(
            (c) => c.providerId === provider.userID,
        );
        if (existing) return existing.id;

        const name = provider.name || "Unknown";
        const newChat = {
            id: Date.now(),
            providerId: provider.userID,
            name,
            initials: buildInitials(name),
            avatarUrl: provider.avatar || "",
            lastMessageTime: "",
            unread: false,
            messages: [],
        };

        chats.value.push(newChat);

        // Snapshot the fields that Provider.vue / Scheduler.vue need.
        // We intentionally omit fields that are large and not needed (e.g., datesBooked).
        providerSnapshots.value = {
            ...providerSnapshots.value,
            [provider.userID]: {
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

        return newChat.id;
    }

    /**
     * Returns the stored provider snapshot for a given providerId, or null.
     *
     * @param {number} providerId
     * @returns {Object|null}
     */
    function getProviderSnapshot(providerId) {
        return providerSnapshots.value[providerId] ?? null;
    }

    /**
     * Stores the id of the chat that should be auto-selected when ChatMessages mounts.
     * Used when navigating from ProviderList → Messages.
     *
     * @param {number} chatId
     */
    function setPendingChat(chatId) {
        localStorage.setItem(PENDING_CHAT_KEY, String(chatId));
    }

    /**
     * Reads and clears the pending chat id (one-time consume).
     * Returns the id as a number, or null if none was stored.
     *
     * @returns {number|null}
     */
    function consumePendingChat() {
        const raw = localStorage.getItem(PENDING_CHAT_KEY);
        if (!raw) return null;
        localStorage.removeItem(PENDING_CHAT_KEY);
        return Number(raw);
    }

    return {
        chats,
        providerSnapshots,
        openOrCreateChat,
        getProviderSnapshot,
        setPendingChat,
        consumePendingChat,
    };
});
