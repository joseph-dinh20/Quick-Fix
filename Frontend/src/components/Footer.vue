<script setup>
import { ref } from "vue";
const year = ref("2026");
</script>

<template>
  <footer>
    <span class="text-gray-500">
      Created By Seal Team Seven @copy {{ year }}</span
    >
  </footer>
</template>

<style scoped>
footer {
  color: blue;
  /* border: black solid 1px; */
}
</style>
