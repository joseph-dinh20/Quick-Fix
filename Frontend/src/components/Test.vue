<template>
  <header class="flex flex-col items-center w-full sticky top-0 bg-white z-20">
    <!-- Navigation Menu -->
    <NavigationMenuRoot
      v-model="currentTrigger"
      class="relative flex w-full justify-between items-center px-6 py-2"
    >
    <NavigationMenuList class="flex w-full items-center bg-white rounded-lg shadow-sm border">

        <!-- LEFT: Logo -->
        <div class="flex items-center">
          <NavigationMenuItem>
            <div
              @click="navigateTo('/')"
              class="flex items-center h-12 cursor-pointer"
            >
              <img
                :src="LogoImage"
                alt="Logo"
                class="h-12 w-auto max-w-xs"
              />
            </div>
          </NavigationMenuItem>
        </div>

        <!-- CENTER: Menu -->
        <div class="flex items-center justify-center flex-1">
          <NavigationMenuItem>
            <NavigationMenuTriggerNav
              :show-chevron="false"
              class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
              @click="navigateTo('#/ProviderList')"
            >
            View Service Providers
            </NavigationMenuTriggerNav>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTriggerNav
              :show-chevron="false"
              class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
              @click="navigateTo('#/DemoJobListings')"
            >
            <Search :stroke-width="1.5"
          class="w-4 h-4"
          /> Find Work
            </NavigationMenuTriggerNav>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTriggerNav
              :show-chevron="false"
              class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
              @click="navigateTo(isLoggedIn ? '#/DemoCreateJob' : '#/Login')"
            >
            <CirclePlus                 
            :stroke-width="1.5"
            class="w-4 h-4"
            />
              Make a Job
            </NavigationMenuTriggerNav>
          </NavigationMenuItem>

          <NavigationMenuItem v-if="isLoggedIn">
            <NavigationMenuTriggerNav
              :show-chevron="false"
              class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
              @click="navigateTo('#/FavoriteProvider')"
            >
            <Bookmark                
            :stroke-width="1.5"
            class="w-4 h-4"
            />
              Saved Providers
            </NavigationMenuTriggerNav>
          </NavigationMenuItem>

          <NavigationMenuItem v-if="isLoggedIn">
            <NavigationMenuTriggerNav
              :show-chevron="false"
              class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
              @click="navigateTo('#/FavoriteProvider')"
            >
            <Bookmark                 
            :stroke-width="1.5"
            class="w-4 h-4"
            />
              Saved Jobs
            </NavigationMenuTriggerNav>
          </NavigationMenuItem>
          

        </div>

        <!-- RIGHT: Auth / Account -->
        <div class="flex items-center justify-end gap-2 ml-6">
          <template v-if="isLoggedIn">
            <NavigationMenuItem>
              <NavigationMenuTriggerNav
                :show-chevron="false"
                class="text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded px-3 h-12 text-sm font-medium cursor-pointer transition-colors"
                @click="navigateTo('#/JoinUs')"
              >
                Join Us
              </NavigationMenuTriggerNav>
            </NavigationMenuItem>

        
            <NavigationMenuItem>
              <NavigationMenuTriggerDropdown
                :show-chevron="true"
                class="h-12 px-3 text-grass11 hover:bg-green3 focus:shadow-green7 group flex items-center justify-center gap-1 rounded text-sm font-medium cursor-pointer transition-colors"
                href="#/Profile"
              >
                <CircleUserRound 
                :stroke-width="1.5"
                class="w-4 h-4"
                /> {{ user.username || "Account" }}
              </NavigationMenuTriggerDropdown>

              <NavigationMenuContent
                class="absolute top-full mt-1 w-48 bg-white rounded-lg shadow-lg border z-50 p-1 flex flex-col items-stretch
                data-[motion=from-start]:animate-enterFromLeft
                data-[motion=from-end]:animate-enterFromRight
                data-[motion=to-start]:animate-exitToLeft
                data-[motion=to-end]:animate-exitToRight"
              >
                <NavigationMenuListItem
                  class="py-1.5"
                  href="#/DemoJobListings"
                  title="Your Jobs"
                />
                <NavigationMenuListItem
                  class="py-1.5"
                  href="#/DemoJobListings"
                  title="Your Applications"
                />
                <NavigationMenuListItem
                  class="py-1.5"
                  href="#/ChatMessages"
                  title="Messages"
                />
                <NavigationMenuListItem
                  class="py-1.5"
                  href="#/Settings"
                  title="Provider Profile"
                />
                <NavigationMenuListItem
                  class="py-1.5"
                  href="#/Settings"
                  title="Settings"
                />
                <NavigationMenuListItem
                  class="py-1.5"
                  title="Log Out"
                  @click="logout"
                />
              </NavigationMenuContent>
            </NavigationMenuItem>
          </template>

          <template v-else>

            <NavigationMenuItem>
              <Button 
              @click="navigateTo('#/Login')"
              variant="outline"
              >
                Sign Up
              </Button>
            </NavigationMenuItem>

            <NavigationMenuItem class="px-2">
              <Button @click="navigateTo('#/Login')">
                Login
              </Button>
            </NavigationMenuItem>
          </template>
        </div>

      </NavigationMenuList>
    </NavigationMenuRoot>

    <!-- Toaster notifications -->
    <Toaster />
  </header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import LogoImage from "@/assets/icons/logo.png";
import NavigationMenuListItem from "./ui/navigation-menu/NavigationMenuListItem.vue";
import NavigationMenuTriggerDropdown from "./ui/navigation-menu/NavigationMenuTrigger.vue";
import NavigationMenuTriggerNav from "./ui/navigation-menu/NavigationMenuTrigger.vue";
import { initCsrf, logout as apiLogout } from "@/services/api.js";
import {
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuRoot,
  NavigationMenuViewport,
} from 'reka-ui';
import { Button } from "@/components/ui/button";
import { Bookmark, CircleUserRound, CirclePlus, Search } from "lucide-vue-next";

const props = defineProps({
  isLoggedIn: {
    type: Boolean,
    default: false
  },
  user: {
    type: Object,
    default: {}
  }
});

const emit = defineEmits(["logout-success"]);

async function logout() {
  try {
    await initCsrf();
    await apiLogout();
  } catch (err) {
    console.error("Logout error:", err);
  }

  localStorage.clear();
  emit("logout-success");
  navigateTo("/");
}

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