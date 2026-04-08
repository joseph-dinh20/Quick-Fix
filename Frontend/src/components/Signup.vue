<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { ref } from "vue"
import { signup } from "@/services/api.js"

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
  console.log(name.value, email.value, password.value);

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
  <div class="flex flex-col items-center">
    <Card class="text-green-900 font-normal">
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
              <FieldLabel for="name"> Full Name </FieldLabel>
              <Input id="name" type="text" v-model="name" placeholder="John Doe" required />
            </Field>
            <Field>
              <FieldLabel for="email"> Email </FieldLabel>
              <Input
                id="email"
                v-model="email"
                type="email"
                placeholder="John@gmail.com"
                required
              />
              <FieldDescription>
                We'll use this to contact you. We will not share your email with
                anyone else.
              </FieldDescription>
            </Field>
            <Field>
              <FieldLabel for="password"> Password </FieldLabel>
              <Input id="password" type="password" v-model="password" required />
              <FieldDescription
                >Must be at least 8 characters long.</FieldDescription
              >
            </Field>
            <Field>
              <FieldLabel for="confirm-password"> Confirm Password </FieldLabel>
              <Input id="confirm-password" type="password"  v-model="confirmPassword" required />
              <FieldDescription>Please confirm your password.</FieldDescription>
            </Field>
            <FieldGroup>
              <Field>
                <Button type="submit"> Create Account </Button>
                <!-- <Button variant="outline" type="button"> -->
                <!--   Sign up with Google -->
                <!-- </Button> -->
                <FieldDescription class="px-6 text-center">
                  Already have an account? <a href="#/Login">Sign in</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

