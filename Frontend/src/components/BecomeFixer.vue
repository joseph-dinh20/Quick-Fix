<script setup>
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'

const form = ref({
  skills: [],
  experience: '',
  document: null
})

function getCookie(name) {
  let cookieValue = null

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')

    for (let cookie of cookies) {
      cookie = cookie.trim()

      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }

  return cookieValue
}

function toggleSkill(skill) {

  if (form.value.skills.includes(skill)) {
    form.value.skills = form.value.skills.filter(s => s !== skill)
  } else {
    form.value.skills.push(skill)
  }
}

const services = ref([])

const dropdownOpen = ref(false)

onMounted(async () => {
  const res = await fetch("http://localhost:8000/api/services/")
  const data = await res.json()
  services.value = data
})

async function submitForm() {
  try {
    const formData = new FormData()

    formData.append("skills", JSON.stringify(form.value.skills.map(s => s.id)))
    formData.append("experience", form.value.experience)

    if (form.value.document) {
      formData.append("document", form.value.document)
    }

    const csrfToken = getCookie("csrftoken")

    const res = await fetch("http://localhost:8000/api/accounts/provider/apply/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": csrfToken
      },
      body: formData
    })

    if (!res.ok) {
      const err = await res.json()
      console.log(err)
      throw new Error("Failed")
    }

    alert("Submitted!")
  } catch (err) {
    console.error(err)
  }
}

</script>

<template>
  <div class="min-h-screen p-10 bg-background text-foreground">
    <h1 class="text-4xl font-bold mb-6">Become a Fixer</h1>

    <p class="text-muted-foreground mb-8 max-w-xl">
      Join our network of skilled fixers and start earning by helping people with tasks in your area.
    </p>

    <div class="max-w-xl space-y-4">

      <!-- skills dropdown -->
  <div class="space-y-4">

    <!-- dropdown style list -->
    <div class="border rounded p-2">
        <p class="font-bold mb-2">Select Skills</p>

        <!-- dropdown button -->
        <button
            @click="dropdownOpen = !dropdownOpen"
            class="w-full p-2 border rounded bg-white text-left"
        >
            </button>

    <!-- dropdown list -->
    <div v-if="dropdownOpen" class="max-h-48 overflow-y-auto space-y-1 mt-2">
        <div
            v-for="s in services"
            :key="s.id"
            @click="toggleSkill(s)"
            class="p-2 rounded cursor-pointer hover:bg-gray-200"
            :class="form.skills.includes(s) ? 'font-bold' : ''"
        >
         {{ s.name }}
    </div>
  </div>
</div>

    <!-- selected skills (chips) -->
    <div class="flex flex-wrap gap-2">
      <span
        v-for="s in form.skills"
        :key="s.id"
        class="bg-primary text-white px-3 py-1 rounded-full text-sm"
      >
        {{ s.name }}
      </span>
    </div>

  </div>

      <!-- experience -->
      <textarea
        v-model="form.experience"
        placeholder="Experience"
        class="w-full p-3 border rounded"
      ></textarea>

      <!-- file upload -->
      <input
        type="file"
        class="w-full p-3 border rounded"
        @change="e => form.document = e.target.files[0]"
      />

      <!-- submit -->
      <Button
        @click="submitForm"
        class="w-full"
      >
        Apply as Fixer
      </Button>

    </div>
  </div>
</template>