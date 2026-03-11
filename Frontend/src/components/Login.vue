<!-- <script setup>
// import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { initCsrf, login as apiLogin } from "@/services/api"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,x   
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import 'vue-toast-notification/dist/theme-sugar.css'
import { useToast } from 'vue-toast-notification'
import { ref } from 'vue'
// const props = defineProps < {
//   class?: HTMLAttributes["class"]
// } > () -->


<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const rememberMe = ref(false)

const handleLogin = () => {
  console.log('Logging in with:', { 
    username: username.value, 
    password: password.value, 
    remember: rememberMe.value 
  })
}
</script>

<template>
  <div class="min-h-screen bg-white-100 flex items-center justify-center p-4">
    <div class="max-w-4xl w-full bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
      
      <div class="md:w-1/2 bg-[#FF7D1F] p-10 md:p-16 text-white flex flex-col justify-between">
        <div>
          <div class="flex items-center gap-2 mb-12">
            <span class="text-2xl">⚡</span>
            <h1 class="text-2xl font-bold tracking-tight">Quick <span class="text-yellow-300">Fix</span></h1>
          </div>
          
          <h2 class="text-4xl font-bold mb-6">Welcome Back</h2>
          <p class="text-orange-50 mb-8 leading-relaxed">
            Manage your services, bookings, and operations from one powerful dashboard designed for speed and simplicity.
          </p>
          
          <ul class="space-y-4">
            <li class="flex items-center gap-3">
              <span class="text-sm">✔</span> Smart scheduling
            </li>
            <li class="flex items-center gap-3">
              <span class="text-sm">✔</span> Secure authentication
            </li>
            <li class="flex items-center gap-3">
              <span class="text-sm">✔</span> Business analytics
            </li>
            <li class="flex items-center gap-3">
              <span class="text-sm">✔</span> Cloud sync
            </li>
          </ul>
        </div>
        
        <p class="mt-12 text-sm opacity-80">© 2026 QuickFix</p>
      </div>

      <div class="md:w-1/2 p-10 md:p-16 flex flex-col justify-center">
        <h3 class="text-2xl font-bold text-gray-800 mb-8">Login to your account</h3>
        
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label class="block text-sm font-semibold text-gray-600 mb-2">Username</label>
            <input 
              v-model="username"
              type="text" 
              placeholder="Enter your username"
              class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500 focus:outline-none transition-all"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-600 mb-2">Password</label>
            <input 
              v-model="password"
              type="password" 
              placeholder="Enter your password"
              class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500 focus:outline-none transition-all"
            />
          </div>

          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="rememberMe" type="checkbox" class="rounded border-gray-300 text-orange-500 focus:ring-orange-500">
              <span class="text-gray-600">Remember me</span>
            </label>
            <a href="#" class="text-blue-500 hover:underline">Forgot password?</a>
          </div>

          <button 
            type="submit"
            class="w-full bg-[#FF7D1F] hover:bg-orange-600 text-white font-bold py-3 rounded-lg transition-colors shadow-lg shadow-orange-200"
          >
            Login
          </button>
        </form>

        <p class="text-center mt-8 text-sm text-gray-600">
          Don't have an account? 
          <a href="#/Signup" class="text-blue-500 font-semibold hover:underline">Sign Up</a>
        </p>
      </div>
    </div>
  </div>
</template>
