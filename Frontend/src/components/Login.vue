<script setup>
// import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
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
import 'vue-toast-notification/dist/theme-sugar.css'
import { useToast } from 'vue-toast-notification'
import { ref } from 'vue'
// const props = defineProps < {
//   class?: HTMLAttributes["class"]
// } > ()

async function getData() {
  const $toast = useToast()
  // geting the total users stored in server.js
  const url = "http://localhost:8080/users"
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Erorr('Response Stat: ${response.status}')
    }
    const result = await response.json()
    let instance = $toast.success(JSON.stringify(result))
    console.log(result)
  }
  catch (error) {
    console.error(error.message)
  }
}

const emit = defineEmits(['login-success'])
const email = ref('')
const password = ref('')

function quickLogin() {
  emit('login-success')
}
async function login() {
  const $toast = useToast()
  const response = await fetch('http://localhost:8080/users/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: email.value,
      password: password.value,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    let instance = $toast.success(data.message)
    console.error('Login Failed', data.message)
    throw new Error(data.message)
  }

  // sends data to App.vue (our root node)
  emit('login-success')
  let instance = $toast.success(data.message)
  console.log('Login Success', data.message)
  return data
}

</script>

<template>
  <!-- <div :class="cn('flex flex-col gap-6', props.class)"> -->
  <div class="login-root flex flex-col gap-6">
    <Card class="text-green-900 font-normal">
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <!-- <form> -->
        <!-- the @submit.prevent stops the page to be reloaded -->
        <!-- reference https://vuejs.org/guide/essentials/event-handling -->
        <form @submit.prevent="login">
          <FieldGroup>
            <Field>
              <FieldLabel for="email">
                Email
              </FieldLabel>
              <Input id="email" type="email" v-model="email" placeholder="abc@abc.com" required />
            </Field>
            <Field>
              <div class="flex items-center">
                <FieldLabel for="password">
                  Password
                </FieldLabel>
                <a href="#" class="ml-auto inline-block text-sm underline-offset-4 hover:underline">
                  Forgot your password?
                </a>
              </div>
              <Input id="password" type="password" v-model="password" placeholder="abc" required />
            </Field>
            <Field>
              <!-- <Button type="submit" @click="login"> -->
              <Button type="submit">
                Login
              </Button>
              <Button variant="outline" type="button">
                Login with Google
              </Button>
              <FieldDescription class="text-center">
                Don't have an account?
                <a href="#">
                  Sign up
                </a>
              </FieldDescription>
            </Field>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
    <Button @click="getData">get users login data</Button>
    <Button @click="quickLogin">Bypass Login</Button>
  </div>
</template>
