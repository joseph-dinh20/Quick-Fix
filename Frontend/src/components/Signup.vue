<!-- <script setup lang="ts">
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
</script> -->

<script setup>
import { reactive } from 'vue'
import { signup } from "@/services/api.js"

const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false
})

const handleSignUp = () => {
  // Logic for account creation
  console.log('Account Data:', { ...formData })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-6">
    <div class="max-w-5xl w-full bg-white rounded-[2.5rem] shadow-2xl overflow-hidden flex flex-col lg:flex-row">
      
      <div class="lg:w-[42%] bg-[#318CF1] p-12 text-white flex flex-col justify-between relative overflow-hidden">
        <div>
          <div class="flex items-center gap-2 mb-16">
            <span class="text-2xl">⚡</span>
            <h1 class="text-2xl font-bold tracking-tight text-white">
              Quick<span class="text-yellow-400">Fix</span>
            </h1>
          </div>
          
          <h2 class="text-4xl font-bold mb-6 leading-tight">Build Your Account</h2>
          <p class="text-blue-50 mb-10 leading-relaxed opacity-90">
            Join QuickFix and manage services, customers, and operations from a powerful desktop platform.
          </p>
          
          <ul class="space-y-5">
            <li v-for="feature in ['Business dashboard', 'Secure cloud storage', 'Multi-device sync', 'Analytics & reporting']" 
                :key="feature" 
                class="flex items-center gap-3 text-sm font-medium">
              <span class="text-blue-200">✔</span> {{ feature }}
            </li>
          </ul>
        </div>
        
        <p class="mt-12 text-xs opacity-70">© 2026 QuickFix</p>
      </div>

      <div class="lg:w-[58%] p-10 lg:p-14 flex flex-col justify-center">
        <header class="mb-8">
          <h3 class="text-2xl font-bold text-gray-800">Create your account</h3>
          <p class="text-gray-400 text-sm mt-1">Start managing your workflow professionally</p>
        </header>
        
        <form @submit.prevent="handleSignUp" class="space-y-5">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">First Name</label>
              <input v-model="formData.firstName" type="text" placeholder="John" class="input-style" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Last Name</label>
              <input v-model="formData.lastName" type="text" placeholder="Doe" class="input-style" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Email</label>
            <input v-model="formData.email" type="email" placeholder="john@example.com" class="input-style" />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Username</label>
            <input v-model="formData.username" type="text" placeholder="username" class="input-style" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Password</label>
              <input v-model="formData.password" type="password" placeholder="••••••••" class="input-style" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Confirm Password</label>
              <input v-model="formData.confirmPassword" type="password" placeholder="••••••••" class="input-style" />
            </div>
          </div>

          <div class="flex items-center gap-2 pt-2">
            <input v-model="formData.agreeToTerms" type="checkbox" id="terms" class="rounded border-gray-300 text-blue-500 focus:ring-blue-500">
            <label for="terms" class="text-xs text-gray-500 leading-none">
              I agree to the <a href="#" class="text-blue-500 hover:underline">Terms of Service</a> and <a href="#" class="text-blue-500 hover:underline">Privacy Policy</a>
            </label>
          </div>

          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <button type="submit" @click = "signup({name: formData.firstName, email: formData.email, password: formData.password})" class="flex-1 bg-[#318CF1] hover:bg-blue-600 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-blue-100">
              Create Account
            </button>
          </div>
            <p class="text-center mt-8 text-sm text-gray-600">
                Already have an account? 
                <a href="#/Login" class="text-blue-500 font-semibold hover:underline">Login</a>
            </p>
        </form>
      </div>
    </div>
  </div>
</template>

<input 
  v-model="formData.firstName" 
  type="text" 
  placeholder="John" 
  class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-sm transition-all focus:ring-2 focus:ring-blue-400 focus:border-transparent outline-none placeholder:text-gray-300" 
/>