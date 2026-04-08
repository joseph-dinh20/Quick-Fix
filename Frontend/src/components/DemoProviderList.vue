<script setup>
import {
  Card,
  CardContent,
  CardDescription,
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
import { Bookmark } from "lucide-vue-next";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
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
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

import { onMounted } from "vue";
import workPhoto1 from "@/assets/workPhotos/bathroom.jpg";
import workPhoto2 from "@/assets/workPhotos/garden.jpg";
import workPhoto3 from "@/assets/workPhotos/kitchen.jpg";
import profAvatar from "@/assets/avatars/avatar.png";
import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import starIcon from "@/assets/icons/star.png";
import checkMarkIcon from "@/assets/icons/checkMark.png";
import aboutMeIcon from "@/assets/icons/aboutMe.png";
import albumIcon from "@/assets/icons/album.png";
import reviewIcon from "@/assets/icons/review.png";
import spainFlag from "@/assets/flags/ES.svg";
import vietnamFlag from "@/assets/flags/VN.svg";
import arabicFlag from "@/assets/flags/SA.svg";
import chinaFlag from "@/assets/flags/CN.svg";
import usFlag from "@/assets/flags/US.svg";

import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";

import { faker } from "@faker-js/faker";
import { Badge } from "@/components/ui/badge";
import Provider from "@/components/DemoProvider.vue";

import {
  loadProviders,
  toggleFavoriteProvider,
  getFavorites,
} from "../services/api";
import { userListStore } from "@/store/userList";
import { storeToRefs } from "pinia";

const BASE_URL = "http://localhost:8000";

function absoluteUrl(path) {
  if (!path) return "";
  return path.startsWith("http") ? path : `${BASE_URL}${path}`;
}

function normalizeProvider(provider) {
  return {
    ...provider,
    avatar: absoluteUrl(provider.avatar),
    price: provider.price_per_hour,
    aboutMe: provider.about_me,
    averageRating: provider.average_rating,
    jobsCompleted: provider.total_rating || 0,
    ratings: provider.ratings || [],
    services: provider.services || [],
    city: provider.city || "",
    state: provider.state || "",
    isBookmarked: false,
    workPhotos: (provider.work_images || []).map((img) =>
      absoluteUrl(img.image),
    ),
  };
}

async function fetchProviders() {
  try {
    const response = await loadProviders();
    providers.value = response.data.map(normalizeProvider);
    await markBookmarkedProviders();
  } catch (error) {
    console.error("Failed to load providers", error);
  }
}

async function markBookmarkedProviders() {
  try {
    const response = await getFavorites();
    const favoriteIds = new Set(response.data.map((provider) => provider.id));
    providers.value.forEach((provider) => {
      provider.isBookmarked = favoriteIds.has(provider.id);
    });
  } catch (error) {
    // Ignore if user is not authenticated or favorites cannot be loaded
    console.warn("Could not load favorite providers", error);
  }
}

async function handleToggleFavorite(provider) {
  try {
    await toggleFavoriteProvider(provider.id);
    provider.isBookmarked = !provider.isBookmarked;
  } catch (error) {
    console.error("Failed to toggle favorite provider", error);
  }
}

// NOTE: grabbing data from pinia from store.js in the /store directory.
const store = userListStore();
const { providers } = storeToRefs(store);

onMounted(fetchProviders);
</script>

<template>
  <div v-if="!providers.length" class="text-sm text-muted-foreground text-center mt-4">
    No results
  </div>
  <div
    v-for="provider in providers"
    :key="provider.id"
    class="flex flex-col items-center m-5"
  >
    <Card class="flex flex-col max-w-150 min-w-150">
      <CardHeader class="justify-between flex-row">
        <div class="flex flex-row gap-20 m-2 pl-10">
          <Avatar class="scale-[4] self-center">
            <AvatarImage :src="provider.avatar" alt="@shadcn" />
            <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{{ provider.name }}</CardTitle>
            <CardDescription class="mt-1 text-sm text-slate-500">
              {{ provider.city || "Location unknown" }},
              {{ provider.state || "" }}
            </CardDescription>
            <CardDescription class="mt-2">
              <Badge variant="outline" size="sm">
                <img class="w-4 inline-block align-top" :src="starIcon" />
                {{ provider.averageRating }}
                ({{ provider.jobsCompleted }}) reviews
              </Badge>
            </CardDescription>

            <CardDescription class="flex flex-col mt-2 items-start">
              <Badge variant="outline">
                <img class="w-4 inline-block" :src="checkMarkIcon" />
                Completed {{ provider.jobsCompleted }} Jobs
              </Badge>
            </CardDescription>
            <div class="flex flex-wrap gap-2 mt-2">
              <template v-for="service in provider.services" :key="service.id">
                <Badge variant="secondary" size="sm">{{ service.name }}</Badge>
              </template>
            </div>
            <div class="mt-3 flex gap-2">
              <Button
                variant="ghost"
                size="sm"
                class="border-transparent bg-transparent text-primary hover:bg-transparent hover:text-primary"
                @click="handleToggleFavorite(provider)"
                aria-label="Toggle bookmark"
              >
                <Bookmark
                  :fill="provider.isBookmarked ? 'currentColor' : 'none'"
                  :class="
                    provider.isBookmarked ? 'text-primary' : 'text-primary'
                  "
                  class="w-5 h-5"
                />
              </Button>
            </div>
            <Dialog>
              <DialogTrigger as-child>
                <Button variant="default" class="mt-3">View Profile</Button>
              </DialogTrigger>
              <DialogContent
                class="h-full max-h-95/100 max-w-150 p-0 gap-0 m-0"
              >
                <DialogHeader class="sr-only">
                  <DialogTitle>Provider Profile</DialogTitle>
                  <DialogDescription
                    >Full provider profile details</DialogDescription
                  >
                </DialogHeader>
                <ScrollArea class="h-full max-h-full">
                  <div class="p-4">
                    <!-- WARN: passing data to Provider.vue -->
                    <Provider :provider="provider" />
                  </div>
                </ScrollArea>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <CardTitle class="w-15 flex flex-col items-center">
          ${{ provider.price }}
          <!-- <Badge variant="outline" class="text-base">${{ provider.price }}</Badge> -->
          <CardDescription>per hour</CardDescription>
        </CardTitle>
      </CardHeader>
      <CardContent class="flex flex-col gap-2">
        <Separator class="my-2" />
        <CardTitle
          ><img class="w-8 inline-block" :src="aboutMeIcon" /> About
          Me</CardTitle
        >
        <span class="line-clamp-4"> {{ provider.aboutMe }} </span>
        <Separator class="my-2" />
      </CardContent>
      <CardFooter class="flex flex-col"> </CardFooter>
    </Card>
  </div>
</template>

<style scoped></style>