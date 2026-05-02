<template>
  <div class="min-h-screen bg-slate-50 p-6">
    <div class="max-w-7xl mx-auto">
      <div class="mb-6">
        <p class="text-sm font-semibold text-blue-600 uppercase tracking-wide">
          QuickFix Location Search
        </p>
        <h1 class="text-3xl font-bold text-slate-900 mt-1">
          Find help or work near you
        </h1>
        <p class="text-slate-600 mt-2">
          Browse nearby providers and jobs using location, radius, service type, and search.
        </p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 mb-6">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div class="flex bg-slate-100 rounded-xl p-1 w-fit">
            <button
              @click="switchView('providers')"
              :class="activeView === 'providers' ? activeTab : inactiveTab"
              class="flex items-center gap-2"
            >
              <Wrench class="w-4 h-4" />
              Providers
            </button>

            <button
              @click="switchView('jobs')"
              :class="activeView === 'jobs' ? activeTab : inactiveTab"
              class="flex items-center gap-2"
            >
              <Briefcase class="w-4 h-4" />
              Jobs
            </button>
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <button
              @click="useMyLocation"
              class="px-4 py-2 rounded-xl bg-purple-600 text-white font-semibold hover:bg-purple-700 transition flex items-center justify-center gap-2"
            >
              <MapPin class="w-4 h-4" />
              Use My Location
            </button>

            <select
              v-model="radiusMiles"
              class="border border-slate-300 rounded-xl px-4 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option :value="5">Within 5 miles</option>
              <option :value="10">Within 10 miles</option>
              <option :value="15">Within 15 miles</option>
              <option :value="25">Within 25 miles</option>
              <option :value="50">Within 50 miles</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-5">
          <div class="flex gap-2">
            <input
              v-model="searchQuery"
              @keyup.enter="handleSearchLocation"
              type="text"
              placeholder="Search name, job, service, or city..."
              class="border border-slate-300 rounded-xl px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button
              @click="handleSearchLocation"
              class="px-4 py-2 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition flex items-center gap-2"
            >
              <Search class="w-4 h-4" />
              Search
            </button>
          </div>

          <select
            v-model="selectedService"
            class="border border-slate-300 rounded-xl px-4 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="All">All Services</option>
            <option v-for="service in services" :key="service" :value="service">
              {{ service }}
            </option>
          </select>
        </div>

        <div class="flex flex-wrap gap-3 mt-4 text-sm text-slate-600">
          <span class="bg-slate-100 px-3 py-1 rounded-full">
            Center: <strong>{{ userLocation.city }}</strong>
          </span>
          <span class="bg-slate-100 px-3 py-1 rounded-full">
            Radius: <strong>{{ radiusMiles }} miles</strong>
          </span>
          <span class="bg-slate-100 px-3 py-1 rounded-full">
            Results: <strong>{{ filteredItems.length }}</strong>
          </span>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="flex items-center justify-between px-5 py-4 border-b border-slate-200">
            <div>
              <h2 class="font-bold text-slate-900">
                {{ activeView === 'providers' ? 'Provider Map' : 'Job Map' }}
              </h2>
              <p class="text-sm text-slate-500">
                Click a pin or listing to view more details.
              </p>
            </div>

            <p v-if="activeView === 'jobs' && loadingJobs" class="text-sm text-slate-500">
              Loading jobs...
            </p>
          </div>

          <div id="map" class="h-[620px] w-full"></div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-200">
            <h2 class="text-xl font-bold text-slate-900">
              {{ activeView === 'providers' ? 'Nearby Providers' : 'Nearby Jobs' }}
            </h2>
            <p class="text-sm text-slate-500">
              {{ filteredItems.length }} result(s) near {{ userLocation.city }}
            </p>
          </div>

          <div class="p-4 h-[620px] overflow-y-auto">
            <div
              v-if="filteredItems.length === 0"
              class="border border-dashed border-slate-300 rounded-xl p-6 text-center text-slate-500"
            >
              No results found. Try increasing the radius or changing the filters.
            </div>

            <div
              v-for="item in filteredItems"
              :key="`${activeView}-${item.id}`"
              @click="focusItem(item)"
              class="border rounded-xl p-4 mb-3 cursor-pointer transition hover:shadow-sm hover:border-blue-300"
              :class="selectedItem && selectedItem.id === item.id ? 'border-blue-500 bg-blue-50' : 'border-slate-200 bg-white'"
            >
              <div class="flex justify-between gap-3">
                <div>
                  <h3 class="font-bold text-slate-900">
                    {{ activeView === 'providers' ? item.name : item.title }}
                  </h3>
                  <p class="text-sm text-slate-600 mt-1">{{ item.service }}</p>
                  <p class="text-sm text-slate-500 mt-1">
                    {{ item.city }} · {{ getDistanceMiles(item).toFixed(1) }} miles away
                  </p>
                </div>

                <div class="text-slate-500">
                  <Wrench v-if="activeView === 'providers'" class="w-5 h-5" />
                  <Briefcase v-else class="w-5 h-5" />
                </div>
              </div>

              <div class="mt-3 flex items-center justify-between">
                <span v-if="activeView === 'providers'" class="text-sm font-semibold text-slate-700 flex items-center gap-1">
                  <Star class="w-4 h-4" />
                  {{ item.averageRating }}
                </span>

                <span v-else class="text-sm font-semibold text-slate-700">
                  {{ item.budgetDisplay }}
                </span>

                <button
                  @click.stop="openItem(item)"
                  class="text-sm font-semibold text-blue-600 hover:text-blue-700"
                >
                  {{ activeView === 'providers' ? 'View Provider' : 'View Job' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- PROVIDER POPUP -->
      <div
        v-if="activeView === 'providers' && selectedProviderForDetail"
        class="fixed inset-0 z-[9999] bg-black/40 flex items-center justify-center p-4"
        @click.self="closeProviderPopup"
      >
        <div class="bg-white rounded-2xl shadow-xl border border-slate-200 p-5 w-full max-w-4xl max-h-[90vh] overflow-y-auto relative">
          <button
            @click="closeProviderPopup"
            class="absolute top-4 right-4 text-slate-500 hover:text-slate-900 text-2xl font-bold z-10"
          >
            ×
          </button>

          <h2 class="text-xl font-bold text-slate-900 mb-4">
            Provider Profile
          </h2>

          <div @click.capture="handleProviderClickCapture">
            <Provider
              :provider="selectedProviderForDetail"
              @select="handleProviderSelect"
            />
          </div>
        </div>
      </div>

      <!-- JOB POPUP -->
      <div
        v-if="activeView === 'jobs' && selectedJobForPopup"
        class="fixed inset-0 z-[9999] bg-black/40 flex items-center justify-center p-4"
        @click.self="closeJobPopup"
      >
        <div class="bg-white rounded-2xl shadow-xl border border-slate-200 p-6 w-full max-w-lg relative">
          <button
            @click="closeJobPopup"
            class="absolute top-4 right-4 text-slate-500 hover:text-slate-900 text-2xl font-bold"
          >
            ×
          </button>

          <p class="text-sm font-semibold text-blue-600 flex items-center gap-2">
            <Briefcase class="w-4 h-4" />
            Selected Job
          </p>

          <h2 class="text-2xl font-bold text-slate-900 mt-1 pr-8">
            {{ selectedJobForPopup.title }}
          </h2>

          <p class="text-slate-600 mt-2">
            {{ selectedJobForPopup.service }}
          </p>

          <p class="text-slate-500 mt-1 flex items-center gap-1">
            <MapPin class="w-4 h-4" />
            {{ selectedJobForPopup.city }} · {{ getDistanceMiles(selectedJobForPopup).toFixed(1) }} miles away
          </p>

          <div class="mt-4 border-t border-slate-200 pt-4">
            <p class="font-semibold text-slate-800">
              Budget: {{ selectedJobForPopup.budgetDisplay }}
            </p>

            <p v-if="selectedJobForPopup.description" class="text-slate-600 mt-3">
              {{ selectedJobForPopup.description }}
            </p>
          </div>

          <div class="flex gap-3 mt-6">
            <button
              @click="goToJobsPage"
              class="flex-1 px-5 py-2 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition"
            >
              View Job
            </button>

            <button
              @click="closeJobPopup"
              class="px-5 py-2 rounded-xl border border-slate-300 text-slate-700 font-semibold hover:bg-slate-100 transition"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <Dialog v-model:open="schedulerOpen">
      <DialogContent class="max-w-md p-0 border-0">
        <DialogHeader class="sr-only">
          <DialogTitle>Schedule</DialogTitle>
          <DialogDescription>Select a date and time</DialogDescription>
        </DialogHeader>

        <Scheduler
          v-if="selectedProviderForScheduler"
          :provider="selectedProviderForScheduler"
        />
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import {
  Wrench,
  Briefcase,
  MapPin,
  Search,
  Star,
} from "lucide-vue-next";

import Provider from "@/components/Provider.vue";
import Scheduler from "@/components/Scheduler.vue";
import fallbackJobs from "../data/mapJobs.json";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

import { userListStore } from "@/store/userList";
import { storeToRefs } from "pinia";
import { searchJobs } from "@/services/api";

const store = userListStore();
const { providers } = storeToRefs(store);

const activeView = ref("providers");
const selectedItem = ref(null);
const selectedJobForPopup = ref(null);
const selectedProviderForDetail = ref(null);
const selectedProviderForScheduler = ref(null);
const schedulerOpen = ref(false);

const searchQuery = ref("");
const selectedService = ref("All");
const radiusMiles = ref(10);
const jobs = ref([]);
const loadingJobs = ref(false);

const userLocation = ref({
  id: "user-location",
  city: "Long Beach",
  lat: 33.7701,
  lng: -118.1937,
});

let map;
let markers = [];
let userMarker = null;
let radiusCircle = null;

const activeTab =
  "px-4 py-2 rounded-lg bg-white text-blue-600 font-semibold shadow-sm";

const inactiveTab =
  "px-4 py-2 rounded-lg text-slate-600 font-semibold hover:text-slate-900";

const fallbackCoords = [
  { lat: 33.7701, lng: -118.1937 },
  { lat: 33.7890, lng: -118.1892 },
  { lat: 33.7560, lng: -118.2019 },
  { lat: 33.7361, lng: -118.2922 },
  { lat: 33.7858, lng: -118.2645 },
  { lat: 33.8317, lng: -118.2817 },
  { lat: 33.8034, lng: -118.1670 },
  { lat: 33.8358, lng: -118.3406 },
  { lat: 33.7683, lng: -118.3644 },
  { lat: 33.8847, lng: -118.4109 },
];

const cityCoordinates = {
  "long beach": { city: "Long Beach", lat: 33.7701, lng: -118.1937 },
  "san pedro": { city: "San Pedro", lat: 33.7361, lng: -118.2922 },
  "wilmington": { city: "Wilmington", lat: 33.7858, lng: -118.2645 },
  "carson": { city: "Carson", lat: 33.8317, lng: -118.2817 },
  "lakewood": { city: "Lakewood", lat: 33.8536, lng: -118.1339 },
  "torrance": { city: "Torrance", lat: 33.8358, lng: -118.3406 },
  "lomita": { city: "Lomita", lat: 33.7922, lng: -118.3151 },
  "gardena": { city: "Gardena", lat: 33.8883, lng: -118.3089 },
  "redondo beach": { city: "Redondo Beach", lat: 33.8492, lng: -118.3884 },
  "manhattan beach": { city: "Manhattan Beach", lat: 33.8847, lng: -118.4109 },
};

const mapProviders = computed(() => {
  return providers.value.map((provider, index) => {
    const coords = getFallbackCoords(index);

    return {
      ...provider,
      id: provider.id ?? index + 1,
      name: provider.name || "Unnamed Provider",
      city: provider.city || "Long Beach",
      state: provider.state || "CA",
      service: getProviderService(provider),
      lat: Number(provider.latitude ?? provider.lat ?? coords.lat),
      lng: Number(provider.longitude ?? provider.lng ?? coords.lng),
      price: provider.price ?? provider.price_per_hour ?? 75,
      averageRating: provider.averageRating ?? provider.average_rating ?? 4.8,
      jobsCompleted: provider.jobsCompleted ?? provider.total_rating ?? 0,
      aboutMe: provider.aboutMe ?? provider.about_me ?? "No provider description available.",
      workPhotos: provider.workPhotos ?? provider.work_images ?? [],
      ratings: provider.ratings ?? [],
      services: provider.services ?? [],
    };
  });
});

const mapJobs = computed(() => {
  return jobs.value.map((job, index) => {
    const coords = getFallbackCoords(index + 4);

    return {
      ...job,
      id: job.id ?? index + 1,
      title: job.title || "Untitled Job",
      city: job.city || "Long Beach",
      state: job.state || "CA",
      service: getJobService(job),
      lat: Number(job.latitude ?? job.lat ?? coords.lat),
      lng: Number(job.longitude ?? job.lng ?? coords.lng),
      budgetDisplay: job.budget ? `$${job.budget}` : "$0",
    };
  });
});

const currentItems = computed(() => {
  return activeView.value === "providers" ? mapProviders.value : mapJobs.value;
});

const services = computed(() => {
  const uniqueServices = currentItems.value.map((item) => item.service).filter(Boolean);
  return [...new Set(uniqueServices)];
});

const filteredItems = computed(() => {
  return currentItems.value.filter((item) => {
    const nameOrTitle = activeView.value === "providers" ? item.name : item.title;
    const query = searchQuery.value.toLowerCase().trim();

    const matchesSearch =
      !query ||
      nameOrTitle.toLowerCase().includes(query) ||
      item.service.toLowerCase().includes(query) ||
      item.city.toLowerCase().includes(query) ||
      item.state.toLowerCase().includes(query);

    const matchesService =
      selectedService.value === "All" || item.service === selectedService.value;

    const insideRadius = getDistanceMiles(item) <= radiusMiles.value;

    return matchesSearch && matchesService && insideRadius;
  });
});

function getFallbackCoords(index) {
  return fallbackCoords[index % fallbackCoords.length];
}

function getProviderService(provider) {
  if (provider.service) return provider.service;

  if (provider.services && provider.services.length > 0) {
    return provider.services[0].name || "General Repair";
  }

  return "General Repair";
}

function getJobService(job) {
  if (job.service) return job.service;

  if (job.services && job.services.length > 0) {
    return job.services[0].name || "General Repair";
  }

  return job.request_type || "General Repair";
}

function switchView(view) {
  activeView.value = view;
  selectedItem.value = null;
  selectedJobForPopup.value = null;
  selectedProviderForDetail.value = null;
  selectedProviderForScheduler.value = null;
  schedulerOpen.value = false;
  searchQuery.value = "";
  selectedService.value = "All";
}

function handleSearchLocation() {
  const query = searchQuery.value.toLowerCase().trim();

  if (!query) return;

  const cityMatch = cityCoordinates[query];

  if (cityMatch) {
    userLocation.value = {
      id: "user-location",
      city: cityMatch.city,
      lat: cityMatch.lat,
      lng: cityMatch.lng,
    };

    selectedItem.value = null;
    selectedJobForPopup.value = null;
    selectedProviderForDetail.value = null;
    selectedProviderForScheduler.value = null;
    schedulerOpen.value = false;

    refreshMap();
    return;
  }

  const itemMatch = currentItems.value.find((item) => {
    return (
      item.city.toLowerCase().includes(query) ||
      item.service.toLowerCase().includes(query) ||
      (activeView.value === "providers"
        ? item.name.toLowerCase().includes(query)
        : item.title.toLowerCase().includes(query))
    );
  });

  if (itemMatch) {
    userLocation.value = {
      id: "user-location",
      city: itemMatch.city,
      lat: itemMatch.lat,
      lng: itemMatch.lng,
    };

    selectedItem.value = itemMatch;
    refreshMap();
    focusItem(itemMatch);
  }
}

function createIcon(type) {
  const iconSvg =
    type === "provider"
      ? `
        <svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.4-3.4a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.4 3.4z"/>
        </svg>
      `
      : `
        <svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          <rect width="20" height="14" x="2" y="6" rx="2"/>
        </svg>
      `;

  const borderColor = type === "provider" ? "#2563eb" : "#059669";

  return L.divIcon({
    html: `
      <div style="
        width: 40px;
        height: 40px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:white;
        border:3px solid ${borderColor};
        border-radius:50%;
        box-shadow:0 4px 10px rgba(15,23,42,0.35);
      ">
        ${iconSvg}
      </div>
    `,
    className: "",
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -38],
  });
}

function createUserIcon() {
  return L.divIcon({
    html: `
      <div style="
        width: 44px;
        height: 44px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#7c3aed;
        color:white;
        border:3px solid white;
        border-radius:50%;
        box-shadow:0 4px 10px rgba(15,23,42,0.35);
      ">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>
          <circle cx="12" cy="10" r="3"/>
        </svg>
      </div>
    `,
    className: "",
    iconSize: [44, 44],
    iconAnchor: [22, 44],
    popupAnchor: [0, -40],
  });
}

function clearMarkers() {
  markers.forEach((marker) => map.removeLayer(marker));
  markers = [];
}

function updateUserLocationVisuals() {
  if (userMarker) {
    map.removeLayer(userMarker);
  }

  if (radiusCircle) {
    map.removeLayer(radiusCircle);
  }

  userMarker = L.marker([userLocation.value.lat, userLocation.value.lng], {
    icon: createUserIcon(),
  })
    .addTo(map)
    .bindPopup(`<strong>Your Location</strong><br/>${userLocation.value.city}`);

  radiusCircle = L.circle([userLocation.value.lat, userLocation.value.lng], {
    radius: radiusMiles.value * 1609.34,
    color: "#7c3aed",
    fillColor: "#7c3aed",
    fillOpacity: 0.08,
    weight: 2,
  }).addTo(map);
}

function addMarkers() {
  clearMarkers();

  const type = activeView.value === "providers" ? "provider" : "job";

  filteredItems.value.forEach((item) => {
    const marker = L.marker([item.lat, item.lng], {
      icon: createIcon(type),
    }).addTo(map);

    const title = type === "provider" ? item.name : item.title;
    const distance = getDistanceMiles(item).toFixed(1);
    const detailText = type === "provider" ? `Rating: ${item.averageRating}` : item.budgetDisplay;

    marker.bindPopup(`
      <div style="min-width:210px;font-family:Arial,sans-serif">
        <div style="font-weight:700;font-size:15px;margin-bottom:4px">${title}</div>
        <div style="color:#475569;margin-bottom:2px">${item.service}</div>
        <div style="color:#64748b;font-size:13px;margin-bottom:6px">${item.city} · ${distance} miles away</div>
        <div style="font-weight:600;margin-bottom:10px">${detailText}</div>
        <button
          class="quickfix-map-view-btn"
          style="
            width:100%;
            padding:8px 10px;
            background:#2563eb;
            color:white;
            border:none;
            border-radius:10px;
            cursor:pointer;
            font-weight:700;
          ">
          ${type === "provider" ? "View Provider" : "View Job"}
        </button>
      </div>
    `);

    marker.on("click", () => {
      selectedItem.value = item;

      if (activeView.value === "jobs") {
        selectedJobForPopup.value = item;
      } else {
        selectedProviderForDetail.value = item;
      }
    });

    marker.on("popupopen", () => {
      setTimeout(() => {
        const popupElement = marker.getPopup()?.getElement();
        const button = popupElement?.querySelector(".quickfix-map-view-btn");

        if (button) {
          button.onclick = () => openItem(item);
        }
      }, 0);
    });

    markers.push(marker);
  });
}

function refreshMap() {
  if (!map) return;

  updateUserLocationVisuals();
  addMarkers();

  const groupItems = [userMarker, ...markers];

  if (groupItems.length > 1) {
    const group = L.featureGroup(groupItems);
    map.fitBounds(group.getBounds().pad(0.2));
  } else {
    map.setView([userLocation.value.lat, userLocation.value.lng], 12);
  }
}

function focusItem(item) {
  selectedItem.value = item;
  map.setView([item.lat, item.lng], 14);

  const marker = markers.find((m) => {
    const latLng = m.getLatLng();
    return latLng.lat === item.lat && latLng.lng === item.lng;
  });

  if (marker) {
    marker.openPopup();
  }

  if (activeView.value === "jobs") {
    selectedJobForPopup.value = item;
  } else {
    selectedProviderForDetail.value = item;
  }
}

function openItem(item) {
  selectedItem.value = item;

  if (activeView.value === "providers") {
    selectedProviderForDetail.value = item;
  } else {
    selectedJobForPopup.value = item;
  }
}

function closeJobPopup() {
  selectedJobForPopup.value = null;
}

function closeProviderPopup() {
  selectedProviderForDetail.value = null;
}

function handleProviderSelect() {
  selectedProviderForScheduler.value = selectedProviderForDetail.value;
  schedulerOpen.value = true;
}

function handleProviderClickCapture(event) {
  const clickedText = event.target?.innerText?.trim()?.toLowerCase();

  if (clickedText === "select" || clickedText === "select me") {
    handleProviderSelect();
  }
}

function goToJobsPage() {
  window.location.hash = "/DemoJobListings";
}

function useMyLocation() {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by this browser.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
      (position) => {
        userLocation.value = {
          id: "user-location",
          city: "Your Current Location",
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        selectedItem.value = null;
        selectedJobForPopup.value = null;
        selectedProviderForDetail.value = null;
        selectedProviderForScheduler.value = null;
        schedulerOpen.value = false;
        refreshMap();
      },
      () => {
        alert("Could not access your location. Using Long Beach as default.");
      }
  );
}

function getDistanceMiles(item) {
  const earthRadiusMiles = 3958.8;

  const lat1 = degreesToRadians(userLocation.value.lat);
  const lng1 = degreesToRadians(userLocation.value.lng);
  const lat2 = degreesToRadians(item.lat);
  const lng2 = degreesToRadians(item.lng);

  const latDiff = lat2 - lat1;
  const lngDiff = lng2 - lng1;

  const a =
      Math.sin(latDiff / 2) * Math.sin(latDiff / 2) +
      Math.cos(lat1) *
      Math.cos(lat2) *
      Math.sin(lngDiff / 2) *
      Math.sin(lngDiff / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return earthRadiusMiles * c;
}

function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
}

async function fetchJobsForMap() {
  loadingJobs.value = true;

  try {
    const res = await searchJobs({});
    const apiJobs = res.data.results || res.data || [];

    if (apiJobs.length > 0) {
      jobs.value = apiJobs;
    } else {
      console.warn("No API jobs found, using fallback JSON jobs");
      jobs.value = fallbackJobs;
    }
  } catch (err) {
    console.error("Failed to load jobs for map, using fallback:", err);
    jobs.value = fallbackJobs;
  } finally {
    loadingJobs.value = false;
  }
}

onMounted(async () => {
  await fetchJobsForMap();

  map = L.map("map").setView([userLocation.value.lat, userLocation.value.lng], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap",
  }).addTo(map);

  refreshMap();
});

watch([activeView, selectedService, radiusMiles, mapProviders, mapJobs], () => {
  selectedItem.value = null;
  selectedJobForPopup.value = null;
  selectedProviderForDetail.value = null;
  selectedProviderForScheduler.value = null;
  schedulerOpen.value = false;
  refreshMap();
});

watch(searchQuery, () => {
  selectedItem.value = null;
  selectedJobForPopup.value = null;
  selectedProviderForDetail.value = null;
  selectedProviderForScheduler.value = null;
  schedulerOpen.value = false;
  refreshMap();
});
</script>