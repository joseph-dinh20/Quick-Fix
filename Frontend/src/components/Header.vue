<script setup>
import LogoImage from "@/assets/icons/logo.png";
import { Separator } from "@/components/ui/separator";
import { storeToRefs } from "pinia";
import { useUserStore } from "@/store/userStore";
import "vue-toast-notification/dist/theme-sugar.css";
import { useToast } from "vue-toast-notification";

const userStore = useUserStore();
const { isLoggedIn, isCustomer, isProvider } = storeToRefs(userStore);
const $toast = useToast();

const navigate = (hash) => {
  window.location.hash = hash;
};

function handleLogout() {
  const name = userStore.currentUser?.name;
  userStore.logout();
  $toast.success(name ? `Goodbye, ${name}!` : "Logged out");
  window.location.hash = "/";
}
</script>

<template>
  <div>
    <header class="flex min-w-screen items-center justify-evenly p-2">
      <div class="flex h-auto w-25 items-center justify-center">
        <button @click="navigate('/')">
          <img :src="LogoImage" class="pointer-events-none mt-5 scale-[3]" />
        </button>
      </div>

      <div class="button-scope">
        <!-- Logged out -->
        <div v-if="!isLoggedIn">
          <button class="big-button" @click="navigate('#/Login')">Login</button>
          <button class="big-button" @click="navigate('#/Signup')">
            Signup
          </button>
        </div>

        <!-- Customer -->
        <div v-else-if="isCustomer">
          <button class="big-button" @click="handleLogout">Logout</button>
          <button class="big-button" @click="navigate('#/Profile')">
            Profile
          </button>
          <button class="big-button" @click="navigate('#/OrderHistory')">
            Orders
          </button>
        </div>

        <!-- Provider -->
        <div v-else-if="isProvider">
          <button class="big-button" @click="handleLogout">Logout</button>
          <button
            class="big-button"
            @click="navigate('#/ProviderOrderHistory')"
          >
            Bookings
          </button>
          <button class="big-button" @click="navigate('#/Profile')">
            Profile
          </button>
        </div>
      </div>
    </header>
    <Separator class="my-3" />
  </div>
</template>

<style scoped>
.button-scope {
  --backgroundColor: rgba(246, 241, 209);
  --colorShadeA: rgb(106, 163, 137);
  --colorShadeB: rgb(121, 186, 156);
  --colorShadeC: rgb(150, 232, 195);
  --colorShadeD: rgb(187, 232, 211);
  --colorShadeE: rgb(205, 255, 232);
  font-family: "Open Sans", sans-serif;
}

@media (max-width: 600px) {
  header {
    flex-direction: column;
  }

  .button-scope {
    display: flex;
    flex-direction: column;
  }
}

.button-scope *,
.button-scope *::before,
.button-scope *::after {
  box-sizing: border-box;
}

.button-scope button {
  position: relative;
  display: inline-block;
  cursor: pointer;
  outline: none;
  border: 0;
  vertical-align: middle;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--colorShadeA);
  font-family: inherit;
}

.button-scope .big-button {
  padding: 0.5em 1.5em;
  border: 2px solid var(--colorShadeA);
  border-radius: 1em;
  background: var(--colorShadeE);
  transform-style: preserve-3d;
  transition: all 175ms cubic-bezier(0, 0, 1, 1);
}

.button-scope .big-button::before {
  content: "";
  position: absolute;
  inset: 0;
  background: var(--colorShadeC);
  border-radius: inherit;
  box-shadow:
    0 0 0 2px var(--colorShadeB),
    0 0.75em 0 0 var(--colorShadeA);
  transform: translate3d(0, 0.75em, -1em);
  transition: all 175ms cubic-bezier(0, 0, 1, 1);
}

.button-scope .big-button:hover {
  background: var(--colorShadeD);
  transform: translateY(0.375em);
}

.button-scope .big-button:active {
  transform: translateY(0.75em);
}

.button-scope .big-button:active::before {
  transform: translate3d(0, 0, -1em);
  box-shadow:
    0 0 0 2px var(--colorShadeB),
    0 0.25em 0 0 var(--colorShadeB);
}
</style>
