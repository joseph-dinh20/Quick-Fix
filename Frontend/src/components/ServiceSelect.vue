<script setup>
import { Badge } from '@/components/ui/badge'
import { ref, onMounted, computed } from 'vue'
import { getServices } from '@/services/api'

const allServices = ref([])
const loading = ref(true)

const props = defineProps({
  modelValue: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:modelValue'])

async function fetchServices() {
  try {
    const res = await getServices()
    allServices.value = res.data
  } catch (err) {
    console.error('Failed to load services', err)
  } finally {
    loading.value = false
  }
}

function toggle(id) {
  const updated = props.modelValue.includes(id)
    ? props.modelValue.filter(s => s !== id)
    : [...props.modelValue, id]
  emit('update:modelValue', updated)
}

const selected = computed(() =>
  allServices.value.filter(s => props.modelValue.includes(s.id))
)

onMounted(fetchServices)
</script>

<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-wrap gap-2 min-h-8">
      <Badge
        v-for="service in selected"
        :key="service.id"
        variant="secondary"
        class="cursor-pointer gap-1"
        @click="toggle(service.id)"
      >
        {{ service.name }}
        <span class="text-xs opacity-60 hover:opacity-100">✕</span>
      </Badge>
      <span v-if="selected.length === 0" class="text-sm text-gray-500 self-center">
        No services selected.
      </span>
    </div>

    <details class="border rounded-md p-3 w-full max-w-full overflow-hidden">
      <summary class="cursor-pointer font-medium select-none">Edit Services</summary>
      <div v-if="loading" class="text-sm text-gray-500 mt-3">Loading...</div>
      <div v-else class="flex flex-wrap gap-2 mt-3">
        <button
          v-for="service in allServices"
          :key="service.id"
          type="button"
          class="flex items-center gap-2 border rounded-md px-3 py-1.5 text-sm cursor-pointer transition-colors"
          :class="props.modelValue.includes(service.id)
            ? 'bg-primary text-primary-foreground border-primary'
            : 'hover:bg-muted'"
          @click="toggle(service.id)"
        >
          <span v-if="props.modelValue.includes(service.id)" class="text-xs">✓</span>
          {{ service.name }}
        </button>
      </div>
    </details>
  </div>
</template>