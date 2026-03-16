<script setup>
import { Button } from "@/components/ui/button"
</script>

<template>
  <div class="flex flex-col items-center text-center px-6 py-16 text-green-800">
    <h1 class="text-5xl font-bold mb-6">
      Become a QuickFix Provider
    </h1>

    <p class="max-w-2xl text-lg mb-10">
      Earn money helping people in your community. Offer services like plumbing,
      gardening, cleaning, and home repair. Set your own schedule and choose
      the services you want to offer.
    </p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mb-12">
      <div class="p-6 border rounded-xl">
        <h3 class="font-semibold text-lg mb-2">Choose Services</h3>
        <p>Select what jobs you want to offer.</p>
      </div>

      <div class="p-6 border rounded-xl">
        <h3 class="font-semibold text-lg mb-2">Set Your Price</h3>
        <p>Charge hourly or per job.</p>
      </div>

      <div class="p-6 border rounded-xl">
        <h3 class="font-semibold text-lg mb-2">Get Hired</h3>
        <p>Customers book your services.</p>
      </div>
    </div>

    <a href="#/Form">
      <Button size="lg">
        Become a Provider
      </Button>
    </a>
  </div>
</template>