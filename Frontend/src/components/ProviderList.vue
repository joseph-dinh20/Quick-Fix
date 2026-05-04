<!-- NOTE: ProviderList.vue -->
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
import { AspectRatio } from "@/components/ui/aspect-ratio";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import { ref, computed } from "vue";
import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import starIcon from "@/assets/icons/star.png";
import checkMarkIcon from "@/assets/icons/checkMark.png";
import aboutMeIcon from "@/assets/icons/aboutMe.png";

import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import Provider from "@/components/Provider.vue";
import Scheduler from "@/components/Scheduler.vue";

import { useProviderProfileStore } from "@/store/providerProfileStore";

const providerProfileStore = useProviderProfileStore();

// Reactively merged: any saved edit reflects automatically.
const providers = computed(() => providerProfileStore.getMergedProviders());

const profileOpen = ref({});
const schedulerOpen = ref(false);
const selectedProvider = ref(null);


const navigate = (hash) => {
  window.location.hash = hash;
};

function handleSelect(provider, index) {
  profileOpen.value[index] = false;
  selectedProvider.value = provider;
  schedulerOpen.value = true;
}
</script>

<template>
    <div class="flex justify-evenly items-center mb-8">
    <h1 class="text-3xl font-extrabold">
      Find work
    </h1>
    
    <Button variant="ghost" size="icon"     class="text-slate-700"
    @click="navigate('#/DemoMap')"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" x2="9" y1="3" y2="18"></line><line x1="15" x2="15" y1="6" y2="21"></line></svg>
      
    </Button>
  </div>
  <div>
    <div
      v-for="(provider, index) in providers"
      :key="provider.userID"
      class="m-5 flex flex-col items-center"
    >
      <Card class="flex max-w-150 min-w-150 flex-col">
        <CardHeader class="flex-row justify-between">
          <div class="m-2 flex flex-row gap-20 pl-10">
            <Avatar class="scale-[3] self-center">
              <AvatarImage :src="provider.avatar" alt="provider avatar" />
              <AvatarFallback><img :src="defaultAvatar" /></AvatarFallback>
            </Avatar>
            <div>
              <CardTitle>{{ provider.name }}</CardTitle>
              <CardDescription class="mt-1">
                <Badge variant="outline">
                  <img class="inline-block w-4 align-top" :src="starIcon" />
                  {{ provider.averageRating }}
                  ({{ provider.ratings.length }}) reviews
                </Badge>
              </CardDescription>

              <CardDescription class="flex flex-col items-start">
                <Badge variant="outline">
                  <img class="inline-block w-4" :src="checkMarkIcon" />
                  <span>Completed ({{ provider.jobsCompleted }}) Jobs</span>
                </Badge>
              </CardDescription>
              <Dialog v-model:open="profileOpen[index]">
                <DialogTrigger as-child>
                  <Button
                    variant="default"
                    class="mt-3 cursor-pointer rounded-3xl"
                  >
                    View Profile
                  </Button>
                </DialogTrigger>
                <DialogContent
                  class="m-0 h-full max-h-95/100 max-w-150 gap-0 p-0"
                >
                  <DialogHeader class="sr-only">
                    <DialogTitle>Provider Profile</DialogTitle>
                    <DialogDescription>Profile details</DialogDescription>
                  </DialogHeader>
                  <ScrollArea class="h-full max-h-full">
                    <div class="p-4">
                      <Provider
                        :provider="provider"
                        @select="handleSelect(provider, index)"
                      />
                    </div>
                  </ScrollArea>
                </DialogContent>
              </Dialog>
            </div>
          </div>
          <CardTitle class="flex w-15 flex-col items-center">
            ${{ provider.price }}
            <CardDescription>per hour</CardDescription>
          </CardTitle>
        </CardHeader>
        <CardContent class="flex flex-col gap-2">
          <Separator class="my-2" />
          <CardTitle>
            <img class="inline-block w-8" :src="aboutMeIcon" /> About Me
          </CardTitle>
          <span class="line-clamp-4">{{ provider.aboutMe }}</span>
        </CardContent>
        <CardFooter class="flex flex-col"></CardFooter>
      </Card>
    </div>

    <Dialog v-model:open="schedulerOpen">
      <DialogContent class="max-w-md border-0 p-0">
        <DialogHeader class="sr-only">
          <DialogTitle>Schedule</DialogTitle>
          <DialogDescription>Select a date and time</DialogDescription>
        </DialogHeader>
        <Scheduler v-if="selectedProvider" :provider="selectedProvider" />
      </DialogContent>
    </Dialog>
  </div>
</template>

<style scoped></style>
