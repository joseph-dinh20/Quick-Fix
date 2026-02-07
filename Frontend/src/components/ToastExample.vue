<!-- App.vue -->
<template>
  <!-- ... -->
  <Toaster />
  <button @click="() => toast('My first toast')">
    Give me a toast
  </button>
</template>

<script lang="ts" setup>
import { Toaster, toast } from 'vue-sonner'
import 'vue-sonner/style.css'
</script>
