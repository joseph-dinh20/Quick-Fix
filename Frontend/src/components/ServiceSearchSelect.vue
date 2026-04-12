<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import {
  Combobox,
  ComboboxAnchor,
  ComboboxEmpty,
  ComboboxGroup,
  ComboboxInput,
  ComboboxItem,
  ComboboxItemIndicator,
  ComboboxList,
  ComboboxTrigger,
} from '@/components/ui/combobox'
import { Check, ChevronsUpDown, Loader2 } from 'lucide-vue-next'

// --- Types ---
interface Service {
  id: number | string
  name: string
}

// --- Props & Emits ---
defineProps<{
  placeholder?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: Service | null]
}>()

// --- State ---
const services = ref<Service[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const searchQuery = ref('')
const debouncedQuery = ref('')
const selectedService = ref(null)
const isOpen = ref(false)

// --- Debounce ---
let debounceTimer: ReturnType<typeof setTimeout> | null = null
const DEBOUNCE_MS = 400

watch(searchQuery, (query) => {
  if (selectedService.value && query !== selectedService.value.name) {
    selectedService.value = null
    emit('update:modelValue', null)
  }
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    debouncedQuery.value = query
  }, DEBOUNCE_MS)
})

// --- Filtered list (only recomputes after debounce settles) ---
const filteredServices = computed(() => {
  const q = debouncedQuery.value.toLowerCase().trim()
  if (!q) return []
  return services.value.filter((s) => s.name.toLowerCase().includes(q))
})

// --- API (fetch once) ---
async function fetchServices() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch("http://localhost:8000/api/services/")
    services.value = await response.json()
  } catch (e) {
    error.value = 'Failed to load services.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchServices)

// --- Handlers ---
function handleSelect(service) {
  searchQuery.value = service.name
  debouncedQuery.value = ''
  selectedService.value = service
  emit('update:modelValue', service)
}
</script>

<template>
  <div class="relative w-full">
    <Combobox
      @update:model-value="handleSelect"
      class="w-full"
    >
      <ComboboxAnchor class="w-full border rounded-md">
        <ComboboxInput
          :value="searchQuery"
          @input="searchQuery = $event.target.value"
          @focus="isOpen = true"
          @blur="isOpen = false"
          :placeholder="placeholder ?? 'Search services...'"
          class="w-full"
        />
      </ComboboxAnchor>

      <ComboboxList class="w-full mx-10">
        <ComboboxEmpty>
          <span v-if="loading">Loading…</span>
          <span v-else-if="error" class="text-destructive">{{ error }}</span>
          <span v-else>No services found.</span>
        </ComboboxEmpty>

        <ComboboxGroup class="w-full">
          <ComboboxItem
            v-for="service in filteredServices"
            :key="service.id"
            :value="service"
            class="w-full"
          >
            {{ service.name }}
            <!-- <ComboboxItemIndicator>
              <Check class="ml-auto h-4 w-4" />
            </ComboboxItemIndicator> -->
          </ComboboxItem>
        </ComboboxGroup>
      </ComboboxList>
    </Combobox>
  </div>
</template>