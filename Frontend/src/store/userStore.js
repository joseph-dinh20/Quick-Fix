// store/userStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";

// Customer demo accounts
const DEMO_CUSTOMERS = [
  {
    email: "juanescobar@gmail.com",
    password: "juan",
    name: "Juan Escobar",
    id: "u_001",
    userType: "customer",
  },
  {
    email: "josephchang@gmail.com",
    password: "joseph",
    name: "Joseph Chang",
    id: "u_002",
    userType: "customer",
  },
  {
    email: "josephdinh@gmail.com",
    password: "joseph",
    name: "Joseph Dinh",
    id: "u_003",
    userType: "customer",
  },
  {
    email: "markdiaz@gmail.com",
    password: "mark",
    name: "Mark Diaz",
    id: "u_004",
    userType: "customer",
  },
  {
    email: "haocui@gmail.com",
    password: "hao",
    name: "Hao Cui",
    id: "u_005",
    userType: "customer",
  },
];

// Provider demo accounts — one per entry in providers.json.
// `providerId` matches `userID` in providers.json so profile/ratings stores can link up.
const DEMO_PROVIDERS = [
  {
    email: "beaulahwintheiserjr@quickfix.com",
    password: "beaulah",
    name: "Beaulah Wintheiser Jr.",
    id: "p_1413",
    userType: "provider",
    providerId: 1413,
  },
  {
    email: "freddierippin@quickfix.com",
    password: "freddie",
    name: "Freddie Rippin",
    id: "p_3421",
    userType: "provider",
    providerId: 3421,
  },
  {
    email: "katieleannon@quickfix.com",
    password: "katie",
    name: "Katie Leannon",
    id: "p_5169",
    userType: "provider",
    providerId: 5169,
  },
  {
    email: "stuartlockmanhowe@quickfix.com",
    password: "stuart",
    name: "Mr. Stuart Lockman-Howe",
    id: "p_359",
    userType: "provider",
    providerId: 359,
  },
  {
    email: "eileenledner@quickfix.com",
    password: "eileen",
    name: "Eileen Ledner",
    id: "p_981",
    userType: "provider",
    providerId: 981,
  },
  {
    email: "melindachamplin@quickfix.com",
    password: "melinda",
    name: "Melinda Champlin",
    id: "p_1039",
    userType: "provider",
    providerId: 1039,
  },
  {
    email: "carolineleannon@quickfix.com",
    password: "caroline",
    name: "Caroline Leannon I",
    id: "p_2193",
    userType: "provider",
    providerId: 2193,
  },
  {
    email: "bartontromp@quickfix.com",
    password: "barton",
    name: "Barton Tromp",
    id: "p_6231",
    userType: "provider",
    providerId: 6231,
  },
  {
    email: "kentonmraz@quickfix.com",
    password: "kenton",
    name: "Kenton Mraz",
    id: "p_4734",
    userType: "provider",
    providerId: 4734,
  },
  {
    email: "janalittel@quickfix.com",
    password: "jana",
    name: "Dr. Jana Littel Jr.",
    id: "p_3749",
    userType: "provider",
    providerId: 3749,
  },
];

export const ALL_USERS = [...DEMO_CUSTOMERS, ...DEMO_PROVIDERS];

export const useUserStore = defineStore(
  "user",
  () => {
    // Per-user customer profile data, keyed by user id.
    // Shape: { [userId]: { name, avatar, phone, address, apartment } }
    const profiles = ref({});
    const currentUser = ref(null);

    const isLoggedIn = computed(() => currentUser.value !== null);
    const isCustomer = computed(
      () => currentUser.value?.userType === "customer",
    );
    const isProvider = computed(
      () => currentUser.value?.userType === "provider",
    );

    function login(email, password) {
      const match = ALL_USERS.find(
        (u) => u.email === email && u.password === password,
      );
      if (!match) {
        return { success: false, message: "Invalid email or password" };
      }

      const { password: _, ...safeUser } = match;

      if (safeUser.userType === "customer") {
        const savedProfile = profiles.value[safeUser.id] || {};
        currentUser.value = {
          ...safeUser,
          name: savedProfile.name || safeUser.name,
          username: savedProfile.name || safeUser.name,
          avatar: savedProfile.avatar || "",
          phone: savedProfile.phone || "",
          address: savedProfile.address || "",
          apartment: savedProfile.apartment || "",
        };
      } else {
        // Providers — provider profile data is in useProviderProfileStore
        currentUser.value = { ...safeUser };
      }

      return {
        success: true,
        message: `Welcome back, ${currentUser.value.name}!`,
      };
    }

    function logout() {
      currentUser.value = null;
    }

    function saveCustomerProfile(updates) {
      if (!currentUser.value) return;
      if (currentUser.value.userType !== "customer") return;

      const userId = currentUser.value.id;
      const existing = profiles.value[userId] || {};
      const merged = { ...existing, ...updates };

      profiles.value = {
        ...profiles.value,
        [userId]: merged,
      };

      currentUser.value = {
        ...currentUser.value,
        ...updates,
      };
    }

    function saveAddress(address, apartment) {
      saveCustomerProfile({
        address: address || "",
        apartment: apartment || "",
      });
    }

    return {
      profiles,
      currentUser,
      isLoggedIn,
      isCustomer,
      isProvider,
      login,
      logout,
      saveCustomerProfile,
      saveAddress,
    };
  },
  {
    persist: true,
  },
);
