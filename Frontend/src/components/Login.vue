<!-- NOTE: Login.vue -->
<script setup>
import { Button } from "@/components/ui/button";
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
import { Input } from "@/components/ui/input";
import "vue-toast-notification/dist/theme-sugar.css";
import { useToast } from "vue-toast-notification";
import { ref } from "vue";
import { useUserStore } from "@/store/userStore";

const userStore = useUserStore();
const $toast = useToast();

const email = ref("");
const password = ref("");

function login() {
  const result = userStore.login(email.value, password.value);

  if (!result.success) {
    $toast.error(result.message);
    return;
  }

  $toast.success(result.message);

  // Providers always go to their booking inbox
  if (userStore.isProvider) {
    sessionStorage.removeItem("redirectAfterLogin"); // clear any stale customer redirect
    window.location.hash = "/ProviderOrderHistory";
    return;
  }

  // Customers: honor any saved redirect, else go home
  const redirect = sessionStorage.getItem("redirectAfterLogin");
  sessionStorage.removeItem("redirectAfterLogin");
  window.location.hash = redirect || "/";
}
</script>

<template>
  <div class="login-root flex flex-col items-center gap-6">
    <Card>
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="login">
          <FieldGroup>
            <Field>
              <FieldLabel for="email">Email</FieldLabel>
              <Input
                id="email"
                type="email"
                v-model="email"
                placeholder="abc@abc.com"
                required
              />
            </Field>
            <Field>
              <div class="flex items-center">
                <FieldLabel for="password">Password</FieldLabel>
              </div>
              <Input
                id="password"
                type="password"
                v-model="password"
                placeholder="abc"
                required
              />
            </Field>
            <Field>
              <Button type="submit">Login</Button>
              <FieldDescription class="text-center">
                Don't have an account?
                <a href="#/Signup">Sign up</a>
              </FieldDescription>
            </Field>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
