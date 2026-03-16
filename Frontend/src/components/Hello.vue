<script setup lang="ts">
import { ref } from "vue"
import { signup } from "@/services/api.js"

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
  // FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

const name = ref("")
const email = ref("")
const password = ref("")
const confirmPassword = ref("")
const errors = ref<string[]>([])

const handleSubmit = async () => {
  errors.value = []

  if (password.value !== confirmPassword.value) {
    errors.value.push("Passwords do not match")
    return
  }

  try {
    await signup({
      name: name.value,
      email: email.value,
      password: password.value,
    })

    alert("Account created!")
  } catch (err) {
    const data = err?.response?.data
    if (data) {
      if (data.errors && Array.isArray(data.errors)) {
        errors.value = data.errors
      } else if (data.error) {
        errors.value = [data.error]
      } else {
        errors.value = ["Signup failed"]
      }
    } else {
      errors.value = ["Signup failed"]
    }
  }
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Create an account</CardTitle>
      <CardDescription>
        Enter your information below to create your account
      </CardDescription>
    </CardHeader>

    <CardContent>
      <form @submit.prevent="handleSubmit">
        <FieldGroup>
          <template v-if="errors.length">
            <ul class="mb-4 text-red-600 list-disc list-inside">
              <li v-for="(err, idx) in errors" :key="idx">{{ err }}</li>
            </ul>
          </template>

          <Field>
            <FieldLabel>Full Name</FieldLabel>
            <Input v-model="name" type="text" required />
          </Field>

          <Field>
            <FieldLabel>Email</FieldLabel>
            <Input v-model="email" type="email" required />
          </Field>

          <Field>
            <FieldLabel>Password</FieldLabel>
            <Input v-model="password" type="password" required />
          </Field>

          <Field>
            <FieldLabel>Confirm Password</FieldLabel>
            <Input v-model="confirmPassword" type="password" required />
          </Field>

          <Button type="submit">
            Create Account
          </Button>

        </FieldGroup>
      </form>
    </CardContent>
  </Card>
</template>
