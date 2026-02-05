<script setup>
import { ref } from 'vue'

// A reactive variable
const message = ref('')
</script>

<template>
  <div class="p-4">


    <p>v-model testing</p>
    <input v-model="message" type="text" placeholder="Type something..." class="border p-2" />
    <p>{{ message }}</p>
  </div>
</template>
