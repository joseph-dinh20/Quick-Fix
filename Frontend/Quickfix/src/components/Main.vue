<script setup>
import { ref } from 'vue'
const mainText = ref('JUST SOME RANDOM WORDS TO FILL SPACE')
const headLine = 'Hire skilled workers'
const headLine2 = 'for a fair price'
</script>

<template>
  <main>
    <h1>{{ headLine }}</h1>
    <h1>{{ headLine2 }}</h1>
    <h1>{{ mainText }}</h1>
    <h1>{{ mainText }}</h1>
    <h1>{{ mainText }}</h1>
  </main>
</template>

<style scoped>
main {
  /* border: black solid 1px; */
  color: black;
  min-height: 90dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
