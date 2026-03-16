<script setup>
import LogoImage from '@/assets/icons/logo.png'
import { Separator } from '@/components/ui/separator'

defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['logout'])

const navigate = (hash) => {
  window.location.hash = hash
}

function handleLogout() {
  emit('logout')
}
</script>

<template>
  <div>
    <header class="header-bar">
      <!-- LEFT -->
      <div class="logo-wrap">
        <img :src="LogoImage" class="logo-image pointer-events-none" />
      </div>

      <!-- CENTER -->
      <div class="button-scope nav-buttons">
        <!-- <button class="big-button" @click="navigate('/')">Home</button> -->
        <button class="big-button" @click="navigate('/Payment')">Payment</button>
        <button class="big-button" @click="navigate('#/Login')">Login</button>
        <button class="big-button" @click="navigate('#/Signup')">Signup</button>
        <button class="big-button" @click="navigate('#/Form')">Form</button>
        <button class="big-button" @click="navigate('#/Profile')">Profile</button>
        <!-- <button class="big-button" @click="navigate('#/Provider')">Provider</button> -->
        <button class="big-button" @click="navigate('#/Test')">Test</button>
        <button class="big-button" @click="navigate('#/Temp')">Temp</button>
        <button class="big-button" @click="navigate('#/ProviderList')">ProviderList</button>
        <button class="big-button" @click="navigate('#/Main')">Main</button>
        <button class="big-button" @click="navigate('#/JoinUs')">Join Us</button>
      </div>

      <!-- RIGHT -->
      <div class="user-panel">
        <template v-if="user">
          <div class="user-email">
            Logged in as: {{ user.email }}
          </div>
          <button class="logout-link" @click="handleLogout">
            Logout
          </button>
        </template>
      </div>
    </header>

    <Separator class="my-3" />
  </div>
</template>

<style scoped>
.header-bar {
  width: 100%;
  display: grid;
  grid-template-columns: 320px 1fr 220px;
  align-items: center;
  gap: 20px;
  padding: 12px 20px;
}

.logo-wrap {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 80px;
  overflow: hidden;
}

.logo-image {
  width: 400px;
  height: auto;
  display: block;
}

.logo-image:hover {
  opacity: 0.9;
  cursor: pointer;
}

.nav-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
}

.user-panel {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  min-height: 60px;
  gap: 6px;
}

.user-email {
  font-size: 0.85rem;
  color: #374151;
  text-align: right;
  word-break: break-word;
}

.logout-link {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.85rem;
  text-decoration: underline;
  cursor: pointer;
  color: #111827;
}

.logout-link:hover {
  opacity: 0.8;
}

/*==============================================*/
/* Lines below are purely for the big buttons   */
/*==============================================*/

.button-scope {
  --backgroundColor: rgba(246, 241, 209);
  --colorShadeA: rgb(106, 163, 137);
  --colorShadeB: rgb(121, 186, 156);
  --colorShadeC: rgb(150, 232, 195);
  --colorShadeD: rgb(187, 232, 211);
  --colorShadeE: rgb(205, 255, 232);
  font-family: "Open Sans", sans-serif;
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
  padding: 0.8em 2em;
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

@media (max-width: 1100px) {
  .header-bar {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .logo-wrap {
    justify-content: center;
  }

  .logo-image {
    transform-origin: center;
  }

  .user-panel {
    align-items: center;
  }

  .user-email {
    text-align: center;
  }
}

@media (max-width: 600px) {
  .nav-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>