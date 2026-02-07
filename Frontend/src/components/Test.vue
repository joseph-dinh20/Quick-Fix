<script setup>
import { ref } from 'vue'

// A reactive variable
const message = ref('')
</script>

<template>
  <!-- feel free to copy paste the divs to test more stuff of your interest. - Hao.-->
  <div class="p-4 flex-col gap-[30] border min-w-lg min-h-30">
    <p>v-model testing</p>
    <input v-model="message" type="text" placeholder="type something..." class="border p-2" />
    <p>{{ message }}</p>
  </div>

  <div class="p-4 flex-col gap-[30] border min-w-lg min-h-30">
    <p>v-model testing</p>
    <input v-model="message" type="text" placeholder="type something..." class="border p-2" />
    <p>{{ message }}</p>
  </div>

</template>
