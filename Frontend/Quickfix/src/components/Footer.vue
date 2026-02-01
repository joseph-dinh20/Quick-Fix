<script setup>
import { ref } from 'vue'
const year = ref("2026")
const href = ref("https://yahoo.com")
</script>

<template>
  <footer>
    <a :href="href"><span> Created By Seal Team Seven @copy {{ year }}</span></a>
  </footer>
</template>

<style scoped>
footer {
  color: blue;
  /* border: black solid 1px; */
}
</style>
