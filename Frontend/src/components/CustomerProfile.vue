<!-- CustomerProfile.vue -->
<script setup>
import { ref, reactive, onMounted } from "vue";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useUserStore } from "@/store/userStore";
import { useToast } from "vue-toast-notification";

const userStore = useUserStore();
const $toast = useToast();

const form = reactive({
  name: "",
  avatar: "",
  phone: "",
  address: "",
  apartment: "",
});

const email = ref(""); // read-only display

onMounted(() => {
  if (!userStore.currentUser) return;
  form.name = userStore.currentUser.name || "";
  form.avatar = userStore.currentUser.avatar || "";
  form.phone = userStore.currentUser.phone || "";
  form.address = userStore.currentUser.address || "";
  form.apartment = userStore.currentUser.apartment || "";
  email.value = userStore.currentUser.email || "";
});

// Soft cap to keep localStorage healthy
const MAX_AVATAR_BYTES = 500 * 1024;

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function handleAvatarUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (file.size > MAX_AVATAR_BYTES) {
    $toast.error("Image too large. Please pick one under 500KB.");
    event.target.value = "";
    return;
  }
  try {
    const b64 = await fileToBase64(file);
    form.avatar = b64;
  } catch {
    $toast.error("Failed to read the image.");
  }
}

function handleSave() {
  if (!form.name.trim()) {
    $toast.error("Name cannot be empty.");
    return;
  }
  userStore.saveCustomerProfile({
    name: form.name.trim(),
    avatar: form.avatar,
    phone: form.phone.trim(),
    address: form.address.trim(),
    apartment: form.apartment.trim(),
  });
  $toast.success("Profile saved.");
}
</script>

<template>
  <div class="m-10 flex flex-col items-center">
    <Card class="max-w-200 min-w-150 p-6">
      <CardTitle class="flex justify-center text-2xl">My Profile</CardTitle>

      <CardHeader class="flex flex-row items-center gap-6">
        <Label for="avatar" class="cursor-pointer">
          <Input
            id="avatar"
            type="file"
            accept="image/png, image/jpeg"
            class="hidden"
            @change="handleAvatarUpload"
          />
          <Avatar class="m-2 scale-[1.8]">
            <AvatarImage :src="form.avatar" alt="profile avatar" />
            <AvatarFallback>
              {{ form.name?.[0]?.toUpperCase() || "?" }}
            </AvatarFallback>
          </Avatar>
        </Label>
        <p class="text-muted-foreground text-sm">
          Click avatar to upload a new image (PNG/JPEG, &lt;500KB)
        </p>
      </CardHeader>

      <CardContent class="flex flex-col gap-4">
        <div class="flex flex-col gap-2">
          <Label for="name">Full Name</Label>
          <Input id="name" type="text" v-model="form.name" />
        </div>

        <div class="flex flex-col gap-2">
          <Label for="email">Email</Label>
          <Input id="email" type="email" :value="email" disabled />
          <p class="text-muted-foreground text-xs">
            Email is tied to your account and cannot be changed.
          </p>
        </div>

        <div class="flex flex-col gap-2">
          <Label for="phone">Phone</Label>
          <Input
            id="phone"
            type="tel"
            v-model="form.phone"
            placeholder="(555) 123-4567"
          />
        </div>

        <div class="flex flex-col gap-2">
          <Label for="address">Address</Label>
          <Input
            id="address"
            type="text"
            v-model="form.address"
            placeholder="323 W Salt Lake, Long Beach, CA, 90100"
          />
        </div>

        <div class="flex flex-col gap-2">
          <Label for="apartment">Apartment (optional)</Label>
          <Input
            id="apartment"
            type="text"
            v-model="form.apartment"
            placeholder="Unit 101"
          />
        </div>
      </CardContent>

      <CardFooter>
        <Button @click="handleSave">Save Profile</Button>
      </CardFooter>
    </Card>
  </div>
</template>
