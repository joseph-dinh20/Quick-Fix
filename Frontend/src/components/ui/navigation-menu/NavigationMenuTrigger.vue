<script setup lang="ts">
import type { NavigationMenuTriggerProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { ChevronDown } from "lucide-vue-next"
import { NavigationMenuTrigger, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<NavigationMenuTriggerProps & { class?: HTMLAttributes["class"], showChevron?: boolean }>()

const delegatedProps = reactiveOmit(props, "class", "showChevron")
const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <NavigationMenuTrigger
    v-bind="forwardedProps"
    :class="
      cn(
        'group inline-flex h-9 w-max items-center justify-center rounded-md bg-transparent px-4 py-2 text-sm font-medium transition-colors hover:bg-gray-100 focus:bg-gray-100  focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[state=open]:bg-gray-100',
        props.class,
      )
    "
  >
    <slot />
    <ChevronDown
      v-if="showChevron !== false"
      class="relative top-[1px] ml-1.5 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180"
      aria-hidden="true"
    />
  </NavigationMenuTrigger>
</template>
