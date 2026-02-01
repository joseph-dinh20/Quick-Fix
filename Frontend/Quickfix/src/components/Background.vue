<script setup>
</script>

<template>
  <ul class="background">
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
  </ul>
</template>

<style scoped>
@keyframes animate {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
    border-radius: 0;
  }

  100% {
    transform: translateY(-1000px) rotate(720deg);
    opacity: 0;
    border-radius: 50%;
  }
}

.background {
  position: fixed;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  margin: 0;
  padding: 0;
  background: #8ebebe;
  overflow: hidden;
  z-index: -1;
}

.background li {
  position: absolute;
  display: block;
  list-style: none;
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.2);
  animation: animate 35s linear infinite;
}

.background li:nth-child(0) {
  left: 78%;
  width: 74px;
  height: 74px;
  bottom: -74px;
  animation-delay: 1s;
}

.background li:nth-child(1) {
  left: 2%;
  width: 49px;
  height: 49px;
  bottom: -49px;
  animation-delay: 1s;
}

.background li:nth-child(2) {
  left: 0%;
  width: 57px;
  height: 57px;
  bottom: -57px;
  animation-delay: 1s;
}

.background li:nth-child(3) {
  left: 1%;
  width: 50px;
  height: 50px;
  bottom: -50px;
  animation-delay: 9s;
}

.background li:nth-child(4) {
  left: 13%;
  width: 49px;
  height: 49px;
  bottom: -49px;
  animation-delay: 19s;
}

.background li:nth-child(5) {
  left: 80%;
  width: 72px;
  height: 72px;
  bottom: -72px;
  animation-delay: 25s;
}

.background li:nth-child(6) {
  left: 18%;
  width: 84px;
  height: 84px;
  bottom: -84px;
  animation-delay: 2s;
}

.background li:nth-child(7) {
  left: 44%;
  width: 64px;
  height: 64px;
  bottom: -64px;
  animation-delay: 18s;
}

.background li:nth-child(8) {
  left: 67%;
  width: 39px;
  height: 39px;
  bottom: -39px;
  animation-delay: 14s;
}

.background li:nth-child(9) {
  left: 39%;
  width: 67px;
  height: 67px;
  bottom: -67px;
  animation-delay: 41s;
}
</style>
