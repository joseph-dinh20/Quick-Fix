<template>
  <header class="flex flex-col items-center w-full sticky top-0 bg-white z-20">
    <!-- Navigation Menu -->
    <NavigationMenuRoot v-model="currentTrigger" class="relative flex w-full justify-between items-center px-6 py-2">
      <NavigationMenuList class="flex w-full items-center justify-between bg-white rounded-lg shadow-sm border px-4">
        
        <!-- Logo -->
        <NavigationMenuItem>
          <div @click="navigateTo('/')" class="flex items-center justify-center h-12 cursor-pointer">
            <img :src="LogoImage" alt="Logo" class="h-12 w-auto max-w-xs" />
          </div>
        </NavigationMenuItem>

        <!-- Menu Items -->
        <NavigationMenuItem>
          <NavigationMenuTrigger
            class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
            @click="navigateTo('#/ProviderList')"
          >
            Search
          </NavigationMenuTrigger>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuTrigger
            class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
            @click="navigateTo('#/DemoCreateJob')"
          >
            Post Job
          </NavigationMenuTrigger>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuTrigger
            class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
            @click="navigateTo('#/JoinUs')"
          >
            Join Us
          </NavigationMenuTrigger>
        </NavigationMenuItem>



    <NavigationMenuItem>
      <NavigationMenuTrigger class="h-12 px-3 text-sm font-medium cursor-pointer">
        Account
      </NavigationMenuTrigger>
      <NavigationMenuContent class="absolute top-full mt-1 w-48 bg-white rounded-lg shadow-lg border z-50
      data-[motion=from-start]:animate-enterFromLeft data-[motion=from-end]:animate-enterFromRight data-[motion=to-start]:animate-exitToLeft data-[motion=to-end]:animate-exitToRight absolute top-0 right-0 w-full sm:w-auto
      ">
      
        <NavigationMenuListItem
          href="#/Settings"
          title="Settings"
        >
        </NavigationMenuListItem>
        <NavigationMenuListItem
          href="#/ChatMessages"
          title="Messages"
        >
        </NavigationMenuListItem>
        <NavigationMenuListItem 
          href="/"
          title="Log Out"
        >
        </NavigationMenuListItem>
      </NavigationMenuContent>
    </NavigationMenuItem>


      </NavigationMenuList>
    </NavigationMenuRoot>

    <!-- Toaster notifications -->
    <Toaster />
  </header>
</template>

<script setup>
import { ref } from "vue";
import LogoImage from "@/assets/icons/logo.png";
import NavigationMenuListItem from "./ui/navigation-menu/NavigationMenuListItem.vue";
import {
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuRoot,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from 'reka-ui'

const currentTrigger = ref(null);
const navigateTo = (path) => {
  window.location.hash = path;
};
</script>

<style scoped>
/* General header styling */
header {
  z-index: 20;
}

/* Navigation menu root */
.NavigationMenuRoot {
  position: relative;
  z-index: 10;
}

/* Navigation menu triggers */
.NavigationMenuTrigger {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.NavigationMenuTrigger:hover {
  background-color: #f0f0f0;
}

.NavigationMenuTrigger:active {
  background-color: #d9d9d9;
}

/* Navigation menu list */
.NavigationMenuList {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.NavigationMenuContent {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

/* Ensure logo scales nicely */
img {
  display: block;
  height: auto;
}
</style>