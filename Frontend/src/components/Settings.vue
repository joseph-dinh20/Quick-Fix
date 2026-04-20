<script setup>
import { ref, onMounted } from 'vue'
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { Search, PlusCircle, User, PencilLine, Settings, Shield, Lock } from 'lucide-vue-next'

// Import your API functions
import { me, updateProfile, updateSecurity } from '@/services/api' // Adjust path if needed

const navLinks = ref([
  { name: 'Settings', target: 'settings', icon: Settings },
  { name: 'Profile', target: 'profile', icon: User },
  { name: 'Security & sign-in', target: 'security', icon: Shield },
  { name: 'Data & Privacy', target: 'privacy', icon: Lock }
])

// Personal Info State
const personalData = ref({
  name: '',
  email: ''
})
const editedData = ref({ name: '', email: '' })
const isEditing = ref(false)

// Password State
const isEditingPassword = ref(false)
const passwordForm = ref({ newPassword: '', confirmPassword: '' })
const passwordError = ref('')
const passwordSuccess = ref('')

// Load user data on mount
onMounted(async () => {
  try {
    const res = await me()
    // Populate the form using the MeSerializer payload
    personalData.value.name = res.data.name || '' // Name comes from Profile
    personalData.value.email = res.data.email || '' // Email comes from User
    
    // Copy to editable state
    editedData.value = { ...personalData.value }
  } catch (error) {
    console.error("Failed to load user data:", error)
  }
})

const saveChanges = async () => {
  try {
    // 1. Update Profile (Name) if changed
    if (editedData.value.name !== personalData.value.name) {
      await updateProfile({ name: editedData.value.name })
      personalData.value.name = editedData.value.name
    }

    // 2. Update User (Email/Username) if changed
    if (editedData.value.email !== personalData.value.email) {
      await updateSecurity({ email: editedData.value.email })
      personalData.value.email = editedData.value.email
    }

    isEditing.value = false
  } catch (error) {
    console.error("Failed to update profile:", error)
    alert(error.response?.data?.error || "Failed to save changes.")
  }
}

const cancelChanges = () => {
  editedData.value = { ...personalData.value }
  isEditing.value = false
}

const savePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = ''

  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = "Passwords do not match."
    return
  }

  try {
    await updateSecurity({ new_password: passwordForm.value.newPassword })
    passwordSuccess.value = "Password updated successfully!"
    isEditingPassword.value = false
    passwordForm.value = { newPassword: '', confirmPassword: '' }
  } catch (error) {
    // Handle password validation errors returned by the backend
    if (error.response?.data?.errors) {
      passwordError.value = error.response.data.errors.join(", ")
    } else {
      passwordError.value = "Failed to update password."
    }
  }
}

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<template>
    <div class="min-h-screen bg-background font-poppins text-foreground py-12 px-10 w-full">
        <div class="max-w-none w-full grid grid-cols-1 md:grid-cols-[280px_1fr] gap-16">
            
            <aside class="space-y-8">
                <nav class="space-y-1">
                    <Button
                    v-for="link in navLinks"
                    :key="link.name"
                    variant="ghost"
                    class="w-full justify-between hover:bg-muted"
                    @click="scrollToSection(link.target)"
                    >
                    <div class="flex items-center gap-3">
                        <component
                            :is="link.icon"
                            class="w-5 h-5 text-muted-foreground"
                        />
                        {{ link.name }}
                    </div>
                    </Button>
                </nav>

                <div class="space-y-3">
                    <Button class="w-full text-white font-bold h-12">
                        <Search class="w-4 h-4 mr-2" />
                        FIND WORK
                    </Button>
                    <Button variant="outline" class="w-full font-bold h-12 border-primary text-primary hover:bg-primary hover:text-primary-foreground border-2">
                        <PlusCircle class="w-4 h-4 mr-2" />
                        MAKE A JOB
                    </Button>
                </div>
            </aside>

            <main class="space-y-10 w-full">
                <h1 class="text-5xl font-extrabold mb-10 tracking-tight" id="settings">
                    Your Account
                </h1>

                <Card class="rounded-3xl shadow-sm bg-card" id="profile">
                    <CardHeader class="flex flex-row justify-between items-start space-y-0">
                        <div>
                            <CardTitle class="text-2xl mb-1">Personal Information</CardTitle>
                            <CardDescription class="text-sm">Manage your public and private details.</CardDescription>
                        </div>
                        <div class="bg-muted p-3 rounded-full">
                            <User class="w-6 h-6 text-muted-foreground" />
                        </div>
                    </CardHeader>
                    
                    <Separator class="my-2 mx-6 w-auto" />

                    <CardContent class="pt-6">
                        <div class="space-y-2">
                            <div class="flex justify-between items-center text-lg py-3 group border-b border-transparent hover:border-muted transition-all">
                                <span class="font-bold w-48 text-foreground shrink-0">Full Name</span>
                                <div class="flex-1 pr-10 min-w-0">
                                    <Input v-if="isEditing" v-model="editedData.name" class="w-full" />
                                    <span v-else @click="isEditing = true" class="block w-full truncate text-muted-foreground cursor-pointer hover:text-foreground transition-colors">
                                        {{ personalData.name || 'Not set' }}
                                    </span>
                                </div>
                                <PencilLine class="w-5 h-5 text-muted-foreground/30 group-hover:text-primary transition-colors shrink-0 cursor-pointer" @click="isEditing = true" />
                            </div>

                            <div class="flex justify-between items-center text-lg py-3 group border-b border-transparent hover:border-muted transition-all">
                                <span class="font-bold w-48 text-foreground shrink-0">Email</span>
                                <div class="flex-1 pr-10 min-w-0">
                                    <Input v-if="isEditing" v-model="editedData.email" type="email" class="w-full" />
                                    <span v-else @click="isEditing = true" class="block w-full truncate text-muted-foreground cursor-pointer hover:text-foreground transition-colors">
                                        {{ personalData.email || 'Not set' }}
                                    </span>
                                </div>
                                <PencilLine class="w-5 h-5 text-muted-foreground/30 group-hover:text-primary transition-colors shrink-0 cursor-pointer" @click="isEditing = true" />
                            </div>
                        </div>

                        <div v-if="isEditing" class="mt-8 flex gap-4 animate-in fade-in slide-in-from-bottom-2">
                            <Button @click="saveChanges" class=" text-white font-bold h-12 px-8 rounded-xl shadow-lg ">
                                Save Changes
                            </Button>
                            <Button @click="cancelChanges" variant="secondary" class="font-bold h-12 px-8 rounded-xl">
                                Cancel
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                <Card class="rounded-3xl shadow-sm" id="security">
                    <CardHeader>
                        <CardTitle class="text-2xl">Security & sign-in</CardTitle>
                    </CardHeader>
                    <Separator class="mb-6 mx-6 w-auto" />
                    <CardContent class="space-y-6">
                        
                        <div v-if="!isEditingPassword">
                            <button @click="isEditingPassword = true" class="block text-blue-500 font-medium hover:underline text-lg">
                                Change Password
                            </button>
                            <span v-if="passwordSuccess" class="text-green-500 text-sm mt-2 block">{{ passwordSuccess }}</span>
                        </div>

                        <div v-else class="space-y-4 max-w-md animate-in fade-in slide-in-from-bottom-2">
                            <div class="space-y-2">
                                <label class="font-semibold">New Password</label>
                                <Input v-model="passwordForm.newPassword" type="password" placeholder="Enter new password" />
                            </div>
                            <div class="space-y-2">
                                <label class="font-semibold">Confirm Password</label>
                                <Input v-model="passwordForm.confirmPassword" type="password" placeholder="Confirm new password" />
                            </div>
                            
                            <p v-if="passwordError" class="text-red-500 text-sm">{{ passwordError }}</p>

                            <div class="flex gap-4 mt-4">
                                <Button @click="savePassword" class=" text-white font-bold">
                                    Update Password
                                </Button>
                                <Button @click="isEditingPassword = false" variant="secondary" class="font-bold">
                                    Cancel
                                </Button>
                            </div>
                        </div>

                        <a href="#" class="block text-blue-500 font-medium hover:underline text-lg mt-4">Enable two-factor authentication</a>
                    </CardContent>
                </Card>

                <Card class="rounded-3xl shadow-sm" id="privacy">
                    <CardHeader>
                        <CardTitle class="text-2xl">Data & Privacy</CardTitle>
                    </CardHeader>
                    <Separator class="mb-6 mx-6 w-auto" />
                    <CardContent class="space-y-6">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-lg">Use data to improve site</span>
                            <Switch default-checked />
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-lg">Use data to personalize experience</span>
                            <Switch default-checked />
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-lg">Make Account Visible</span>
                            <Switch default-checked />
                        </div>
                    </CardContent>
                </Card>
            </main>
        </div>
    </div>
</template>