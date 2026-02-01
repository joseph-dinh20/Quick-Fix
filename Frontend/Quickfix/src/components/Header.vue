<script setup>
import { ref } from 'vue'
const login = ref('Sign up / Login')
const pro = ref('Become a Fixer')
const href = ref("https://yahoo.com")
</script>

<template>
  <header>
    <img src="../assets/logo.png">
    <div class="button-scope">
      <a :href="href"><button class="big-button">{{ login }}</button> </a>
      <a :href="href"><button class="big-button">{{ pro }}</button> </a>
    </div>
  </header>
  <hr>
</template>

<style scoped>
header {
  /* color: black; */
  /* border: black solid 1px; */
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex: 1;
  min-width: 100%;
  font-size: 20px;
}

img {
  width: 125px;
  height: auto;
  margin-top: 25px;
  transform: scale(3);
}

#brand {
  display: flex;
  align-self: flex-start;
  /* border: green solid 1px; */
}

hr {
  border: 1px solid lightgrey;
  width: 100%;
  margin-top: 20px;
}




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

/* Hides the buttons and only shows the logo instead if width gets too small */
@media (max-width: 600px) {
  .button-scope {
    display: none;
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
.button-scope .big-button {
  padding: 1em 3em;

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
