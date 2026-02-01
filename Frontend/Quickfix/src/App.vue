<script setup>
import Header from '@/components/Header.vue'
import Main from '@/components/Main.vue'
import Footer from '@/components/Footer.vue'
import Background from '@/components/Background.vue'
</script>

<template>
  <div>
    <Background />
    <Header />
    <Main />
    <Footer />
  </div>

</template>

<style scoped>
div {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  flex-direction: column;
  /* border: purple solid 1px; */
}
</style>
