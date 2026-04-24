<template>
  <header class="flex flex-col items-center w-full">
    <!-- Show loading state -->
    <div class="flex flex-col items-center w-full">
      <!-- Navigation Menu from Reka UI -->
      <NavigationMenuRoot v-model="currentTrigger" class="relative z-[1] flex w-full justify-between items-center">
        <NavigationMenuList class="m-0 flex list-none rounded-lg bg-white p-1 shadow-sm border w-full justify-evenly">

          <!-- Logo that is clickable to navigate to Home -->
          <NavigationMenuItem>
            <NavigationMenuTrigger class="flex items-center justify-center gap-2 cursor-pointer" @click="navigateTo('/')">
              <img 
                :src="LogoImage"
                alt="Logo"
                class="w-32 h-auto cursor-pointer"  
              />
            </NavigationMenuTrigger>
          </NavigationMenuItem>

          <!-- Join Us -->
          <NavigationMenuItem>
            <NavigationMenuTrigger class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex select-none items-center justify-between gap-[2px] rounded-[4px] px-3 py-2 text-sm font-medium leading-none outline-none cursor-pointer"
              @click="navigateTo('#/JoinUs')"
              >
              Join Us
            </NavigationMenuTrigger>
          </NavigationMenuItem>

          <!-- Other menu items -->
          <NavigationMenuItem>
            <NavigationMenuTrigger class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex select-none items-center justify-between gap-[2px] rounded-[4px] px-3 py-2 text-sm font-medium leading-none outline-none cursor-pointer"
              @click="navigateTo('#/ProviderList')">
              Search
            </NavigationMenuTrigger>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTrigger class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex select-none items-center justify-between gap-[2px] rounded-[4px] px-3 py-2 text-sm font-medium leading-none outline-none cursor-pointer"
              @click="navigateTo('#/DemoCreateJob')">
              Post Job
            </NavigationMenuTrigger>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTrigger class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex select-none items-center justify-between gap-[2px] rounded-[4px] px-3 py-2 text-sm font-medium leading-none outline-none cursor-pointer"
              @click="navigateTo('#/Settings')">
              Account
            </NavigationMenuTrigger>
          </NavigationMenuItem>

        </NavigationMenuList>
      </NavigationMenuRoot>
    </div>

    <!-- Toaster notifications -->
    <Toaster />
  </header>
</template>

<script setup>
import LogoImage from "@/assets/icons/logo.png";

const navigateTo = (hash) => {
  window.location.hash = hash;
};
</script>

<style scoped>
/* Ensure that the NavigationMenu items are clickable */
.NavigationMenuTrigger {
  cursor: pointer; /* Ensure it's visibly clickable */
  padding-top: 100%;

}

/* Ensure the logo and text items are aligned and don't overlap */
.NavigationMenuRoot {
  position: relative;
  z-index: 10; /* Make sure root element is properly layered */
}

/* Ensure full width of NavigationMenuList */
.NavigationMenuList {
  display: flex;
  justify-content: space-evenly; /* Evenly space items */
  width: 100%; /* Ensures full width */
  align-items: center; /* Ensure vertical centering */
}

/* Styling for the navigation trigger container */
.NavigationMenuTrigger {
  display: flex;
  align-items: center; /* This vertically centers the logo or text */
  justify-content: center; /* This horizontally centers the logo */
  gap: 0.5rem; /* Optional: Adds space between logo and text if needed */
}

img {
  width: 20rem; /* Adjusted logo size (use rem or px) */
  height: auto;
  cursor: pointer; /* Makes logo clickable */
}

.NavigationMenuTrigger:hover {
  background-color: #f0f0f0; /* Add hover effect */
}

.NavigationMenuTrigger:active {
  background-color: #d9d9d9; /* Add active effect */
}
</style>