<script setup>
import { ref } from "vue";
import LogoImage from "@/assets/icons/logo.png";
import { Separator } from "@/components/ui/separator";

const navigate = (hash) => {
  window.location.hash = hash;
};
</script>
<template>
  <div>
    <header class="flex min-w-screen justify-evenly items-center p-2">
      <div class="w-25 items-center h-auto flex justify-center">
        <button @click="navigate('/')">
          <img :src="LogoImage" class="scale-[3] pointer-events-none mt-5" />
        </button>
      </div>
      <div class="button-scope">
        <!-- <button class="big-button" @click="navigate('/')">Home</button> -->
        <!-- <button class="big-button" @click="navigate('/Payment')">Payment</button> -->
        <button class="big-button" @click="navigate('#/Login')">Login</button>
        <!-- <button class="big-button" @click="navigate('#/Provider')">Provider</button> -->
        <!-- <button class="big-button" @click="navigate('#/Test')">Test</button> -->
        <!-- <button class="big-button" @click="navigate('#/Temp')">temp</button> -->
        <button class="big-button" @click="navigate('#/Signup')">Signup</button>
        <button class="big-button" @click="navigate('#/BecomeFixer')">Become Fixer</button>
        <button class="big-button" @click="navigate('#/Form')">Form</button>
        <button class="big-button" @click="navigate('#/Profile')">Profile</button>
        <button class="big-button" @click="navigate('#/ProviderList')">ProviderList</button>
        <button class="big-button" @click="navigate('#/FavoriteProvider')">FavoriteProvider</button>
      </div>
    </header>
    <Separator class="my-3" />
  </div>
</template>

<style scoped>
/*==============================================
/* Lines below are purely for the big buttons */
/*==============================================

/* Wrapper that owns the theme */
.button-scope {
  --backgroundColor: rgba(246, 241, 209);
  --colorShadeA: rgb(106, 163, 137);
  --colorShadeB: rgb(121, 186, 156);
  --colorShadeC: rgb(150, 232, 195);
  --colorShadeD: rgb(187, 232, 211);
  --colorShadeE: rgb(205, 255, 232);
  font-family: "Open Sans", sans-serif;
}

/* Keeping the header buttons aligned top to bottom */
@media (max-width: 600px) {
  /* header adjustment is needed since logo is not part of the buttons */
  header {
    flex-direction: column;
  }

  .button-scope {
    display: flex;
    flex-direction: column;
  }
}

/* Box sizing inside scope */
.button-scope *,
.button-scope *::before,
.button-scope *::after {
  box-sizing: border-box;
}

/* Button base */
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

/* Main button */
/* NOTE: modify size of button here */

.button-scope .big-button {
  padding: 0.5em 1.5em;

  border: 2px solid var(--colorShadeA);
  border-radius: 1em;

  background: var(--colorShadeE);

  transform-style: preserve-3d;

  transition: all 175ms cubic-bezier(0, 0, 1, 1);
}

/* 3D layer */
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

/* Hover */
.button-scope .big-button:hover {
  background: var(--colorShadeD);
  transform: translateY(0.375em);
}

/* Active */
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
