<script setup lang="ts">
import { NavigationMenuLink } from 'reka-ui'

const props = defineProps({
  title: String,
})
</script>

<template>
  <li>
    <NavigationMenuLink as-child>
      <a
        v-bind="$attrs"
        class="block select-none rounded-md px-3 py-1.5 text-sm no-underline outline-none transition-colors
               hover:bg-accent hover:text-accent-foreground
               focus:bg-accent focus:text-accent-foreground"
      >
        {{ props.title }}
      </a>
    </NavigationMenuLink>
  </li>
</template>