<!-- ProviderProfile.vue -->
<script setup>
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
import { Textarea } from "@/components/ui/textarea";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import { Label } from "@/components/ui/label";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";
import { ChevronDown } from "lucide-vue-next";
import { ref, reactive, computed, watch, onMounted } from "vue";

import { useUserStore } from "@/store/userStore";
import {
  useProviderProfileStore,
  ALL_JOB_CATEGORIES,
} from "@/store/providerProfileStore";
import { useToast } from "vue-toast-notification";

const userStore = useUserStore();
const providerProfileStore = useProviderProfileStore();
const $toast = useToast();

const MAX_IMAGE_BYTES = 500 * 1024;
const MAX_WORK_PHOTOS = 10;

const form = reactive({
  name: "",
  avatar: "",
  price: 0,
  aboutMe: "",
  workPhotos: [],
  jobs: [],
});

const provider = ref(null);

onMounted(() => {
  if (!userStore.currentUser?.providerId) return;
  const merged = providerProfileStore.getMergedProvider(
    userStore.currentUser.providerId,
  );
  if (!merged) return;
  provider.value = merged;
  form.name = merged.name || "";
  form.avatar = merged.avatar || "";
  form.price = merged.price || 0;
  form.aboutMe = merged.aboutMe || "";
  form.workPhotos = [...(merged.workPhotos || [])];
  form.jobs = [...(merged.jobs || [...ALL_JOB_CATEGORIES])];
});

// === Read More logic (kept per your request) ===
const showReadMoreButton = computed(() => {
  if (!provider.value) return false;
  return (provider.value.aboutMe || "").split(" ").length > 80;
});

// === Job categories ===
function isJobChecked(category) {
  return form.jobs.includes(category);
}

function toggleJob(category, checked) {
  if (checked) {
    if (!form.jobs.includes(category)) {
      form.jobs = [...form.jobs, category];
    }
  } else {
    form.jobs = form.jobs.filter((j) => j !== category);
  }
}

const jobsButtonLabel = computed(() => {
  if (form.jobs.length === 0) return "Select services";
  if (form.jobs.length === ALL_JOB_CATEGORIES.length) return "All services";
  return form.jobs.join(", ");
});

// === Image utilities ===
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
  if (file.size > MAX_IMAGE_BYTES) {
    $toast.error("Image too large. Please pick one under 500KB.");
    event.target.value = "";
    return;
  }
  try {
    form.avatar = await fileToBase64(file);
  } catch {
    $toast.error("Failed to read the image.");
  }
}

const photoInputKey = ref(0);

async function handlePhotoUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (form.workPhotos.length >= MAX_WORK_PHOTOS) {
    $toast.error(`Maximum ${MAX_WORK_PHOTOS} photos.`);
    photoInputKey.value++;
    return;
  }
  if (file.size > MAX_IMAGE_BYTES) {
    $toast.error("Image too large. Please pick one under 500KB.");
    photoInputKey.value++;
    return;
  }
  try {
    const b64 = await fileToBase64(file);
    form.workPhotos.push(b64);
  } catch {
    $toast.error("Failed to read the image.");
  } finally {
    photoInputKey.value++;
  }
}

function removePhoto(photo) {
  form.workPhotos = form.workPhotos.filter((p) => p !== photo);
}

const displayedPhotos = computed(() => form.workPhotos.slice(0, 4));

// === Carousel state ===
const api = ref();
const totalCount = computed(() => form.workPhotos.length);
const current = ref(0);

function setApi(val) {
  api.value = val;
}

watch(api, (api) => {
  if (!api) return;
  current.value = api.selectedScrollSnap() + 1;
  api.on("select", () => {
    current.value = api.selectedScrollSnap() + 1;
  });
});

// === Save ===
function handleSave() {
  if (!userStore.currentUser?.providerId) return;
  if (!form.name.trim()) {
    $toast.error("Name cannot be empty.");
    return;
  }
  const numericPrice = Number(form.price);
  if (Number.isNaN(numericPrice) || numericPrice < 0) {
    $toast.error("Rate must be a non-negative number.");
    return;
  }
  if (form.jobs.length === 0) {
    $toast.error("Please select at least one service category.");
    return;
  }

  providerProfileStore.saveProfile(userStore.currentUser.providerId, {
    name: form.name.trim(),
    avatar: form.avatar,
    price: numericPrice,
    aboutMe: form.aboutMe.trim(),
    workPhotos: [...form.workPhotos],
    jobs: [...form.jobs],
  });

  $toast.success("Profile saved.");
}
</script>

<template>
  <div class="m-10 flex flex-col items-center">
    <Card class="min-h-200 max-w-200 min-w-150 p-6">
      <CardTitle class="flex justify-center text-2xl">Profile Setup</CardTitle>

      <CardHeader class="flex flex-row items-center justify-between">
        <div class="flex flex-row items-center gap-5">
          <Label for="avatar" class="cursor-pointer">
            <Input
              id="avatar"
              type="file"
              accept="image/png, image/jpeg"
              class="hidden"
              @change="handleAvatarUpload"
            />
            <Avatar class="m-4 scale-[2]">
              <AvatarImage :src="form.avatar" alt="provider avatar" />
              <AvatarFallback>
                {{ form.name?.[0]?.toUpperCase() || "?" }}
              </AvatarFallback>
            </Avatar>
          </Label>
          <CardTitle>
            Full Name
            <Input type="text" v-model="form.name" class="max-w-50" />
          </CardTitle>
        </div>
        <div>
          <CardTitle>
            Hourly Rate
            <Input
              type="number"
              v-model="form.price"
              placeholder="$00"
              min="0"
            />
          </CardTitle>
        </div>
      </CardHeader>

      <CardContent>
        <!-- Services offered -->
        <div class="mb-5 flex flex-col gap-2">
          <Label class="p-2">Services Offered</Label>
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="outline" class="w-fit justify-between gap-2">
                <span>{{ jobsButtonLabel }}</span>
                <ChevronDown class="size-4 opacity-60" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" class="w-56">
              <DropdownMenuLabel>Pick all that apply</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuCheckboxItem
                v-for="category in ALL_JOB_CATEGORIES"
                :key="category"
                :model-value="isJobChecked(category)"
                @update:model-value="(v) => toggleJob(category, v)"
                @select.prevent
              >
                {{ category }}
              </DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <div v-if="form.jobs.length > 0" class="flex flex-wrap gap-1">
            <Badge
              v-for="job in form.jobs"
              :key="job"
              variant="outline"
              class="bg-green-600 text-white"
            >
              {{ job }}
            </Badge>
          </div>
        </div>

        <Label class="p-2">Profile Description</Label>
        <Textarea
          v-model="form.aboutMe"
          id="description"
          class="min-h-50 min-w-full text-pretty"
          placeholder="Write a concise but detailed description on how you can help the customers."
        />

        <!-- Work photos -->
        <Label v-if="form.workPhotos.length > 0" class="mt-5 mb-2">
          Work Photos
        </Label>
        <div id="workPhotos" class="flex">
          <div v-for="photo in displayedPhotos" :key="photo">
            <HoverCard :open-delay="50" :close-delay="0">
              <div class="flex w-25 flex-col">
                <HoverCardTrigger>
                  <div class="flex flex-col">
                    <AspectRatio :ratio="1 / 1">
                      <img
                        :src="photo"
                        class="h-full rounded-lg object-cover p-0.5"
                      />
                    </AspectRatio>
                  </div>
                </HoverCardTrigger>
                <Button
                  class="hover:bg-destructive self-center hover:text-white"
                  @click="removePhoto(photo)"
                  variant="outline"
                  size="sm"
                >
                  X
                </Button>
              </div>
              <HoverCardContent class="w-130 border-0">
                <AspectRatio :ratio="3 / 2">
                  <img :src="photo" class="h-full w-full rounded-lg" />
                </AspectRatio>
              </HoverCardContent>
            </HoverCard>
          </div>

          <!-- Overflow (4+) -->
          <div v-if="form.workPhotos.length > 4">
            <Dialog>
              <DialogTrigger as-child>
                <button class="flex h-full w-25 flex-col">
                  <AspectRatio :ratio="1 / 1">
                    <div class="relative h-full w-full">
                      <img
                        :src="form.workPhotos[4]"
                        class="h-full rounded-lg object-cover p-0.5"
                      />
                      <div
                        class="absolute inset-0.5 flex items-center justify-center rounded-lg bg-black/50"
                      >
                        <span class="text-xl font-bold text-white">
                          {{ form.workPhotos.length - 4 }}+
                        </span>
                      </div>
                    </div>
                  </AspectRatio>
                </button>
              </DialogTrigger>
              <DialogContent class="flex max-w-170 min-w-100 justify-center">
                <DialogHeader>
                  <DialogTitle></DialogTitle>
                  <DialogDescription></DialogDescription>
                  <Carousel
                    class="flex flex-col items-center"
                    :opts="{ startIndex: 4, loop: true, duration: 10 }"
                    @init-api="setApi"
                  >
                    <CarouselContent>
                      <CarouselItem
                        v-for="photo in form.workPhotos"
                        :key="photo"
                      >
                        <div class="flex aspect-square flex-col items-center">
                          <img
                            :src="photo"
                            class="h-full w-full rounded-lg object-cover"
                          />
                          <Button
                            class="hover:bg-destructive mt-2 mb-5 w-20 hover:text-white"
                            @click="removePhoto(photo)"
                            variant="outline"
                          >
                            Remove
                          </Button>
                        </div>
                      </CarouselItem>
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                    <Badge
                      class="mt-2 bg-blue-500 text-sm text-white"
                      variant="outline"
                    >
                      {{ current }} of {{ totalCount }} photos
                    </Badge>
                  </Carousel>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <Label for="picture" class="mt-5">
          Photo Upload ({{ form.workPhotos.length }}/{{ MAX_WORK_PHOTOS }})
        </Label>
        <Input
          id="picture"
          :key="photoInputKey"
          type="file"
          accept="image/png, image/jpeg"
          class="w-50 cursor-pointer"
          :disabled="form.workPhotos.length >= MAX_WORK_PHOTOS"
          @change="handlePhotoUpload"
        />
      </CardContent>

      <CardFooter>
        <Button @click="handleSave">Save Profile</Button>
      </CardFooter>
    </Card>
  </div>
</template>
