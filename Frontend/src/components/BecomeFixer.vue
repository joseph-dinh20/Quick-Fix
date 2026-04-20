<script setup>
import { ref, onMounted } from "vue";
import { Button } from "@/components/ui/button";

const form = ref({
    skills: [],
    experience: "",
    document: null,
});

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1),
                );
                break;
            }
        }
    }

    return cookieValue;
}

function toggleSkill(skill) {
    if (form.value.skills.includes(skill)) {
        form.value.skills = form.value.skills.filter((s) => s !== skill);
    } else {
        form.value.skills.push(skill);
    }
}

const services = ref([]);

const dropdownOpen = ref(false);

onMounted(async () => {
    const res = await fetch("http://localhost:8000/api/services/");
    const data = await res.json();
    services.value = data;
});

async function submitForm() {
    try {
        const formData = new FormData();

        formData.append(
            "skills",
            JSON.stringify(form.value.skills.map((s) => s.id)),
        );
        formData.append("experience", form.value.experience);

        if (form.value.document) {
            formData.append("document", form.value.document);
        }

        const csrfToken = getCookie("csrftoken");

        const res = await fetch(
            "http://localhost:8000/api/accounts/provider/apply/",
            {
                method: "POST",
                credentials: "include",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                body: formData,
            },
        );

        if (!res.ok) {
            const err = await res.json();
            console.log(err);
            throw new Error("Failed");
        }

        alert("Submitted!");
    } catch (err) {
        console.error(err);
    }
}
</script>

<template>
  <div class="min-h-screen bg-background text-foreground flex items-center justify-center p-6">
    <div class="w-full max-w-2xl bg-white dark:bg-muted rounded-2xl shadow-lg p-8 space-y-6">
      <div class="space-y-2">
        <h1 class="text-3xl font-bold tracking-tight">Become a Fixer</h1>
        <p class="text-muted-foreground">
          Join our network of skilled fixers and start earning by helping people with tasks in your area.
        </p>
      </div>

      <div class="space-y-5">
        <div class="space-y-3">
          <label class="text-sm font-semibold">Select Skills</label>

          <div class="relative">
            <button
              class="w-full border rounded-lg bg-background px-3 py-2 text-left flex items-center justify-between"
              @click="dropdownOpen = !dropdownOpen"
            >
              <span class="text-sm text-muted-foreground">
                {{ form.skills.length ? form.skills.map(s => s.name).join(', ') : 'Choose your skills' }}
              </span>
              <span class="text-xs">▼</span>
            </button>

            <div
              v-if="dropdownOpen"
              class="absolute z-10 mt-2 w-full max-h-48 overflow-y-auto rounded-lg border bg-white dark:bg-muted shadow"
            >
              <div
                v-for="s in services"
                :key="s.id"
                @click="toggleSkill(s)"
                class="px-3 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 flex justify-between items-center"
              >
                <span>{{ s.name }}</span>
                <span v-if="form.skills.includes(s)">✓</span>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap gap-2">
            <span
              v-for="s in form.skills"
              :key="s.id"
              class="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-medium"
            >
              {{ s.name }}
            </span>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-semibold">Experience</label>
          <textarea
            v-model="form.experience"
            placeholder="Tell us about your experience..."
            class="w-full border rounded-lg p-3 min-h-[120px] resize-none focus:outline-none focus:ring-2 focus:ring-primary"
          ></textarea>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-semibold">Upload Document</label>
          <input
            type="file"
            class="w-full border rounded-lg p-2 file:mr-3 file:py-1 file:px-3 file:rounded file:border-0 file:bg-primary file:text-white hover:file:bg-primary/90"
            @change="e => form.document = e.target.files[0]"
          />
        </div>

        <Button
          class="w-full py-3 text-base font-semibold rounded-lg"
          @click="submitForm"
        >
          Apply as Fixer
        </Button>
      </div>
    </div>
  </div>
</template>
