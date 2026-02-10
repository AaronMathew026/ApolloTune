<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <!-- Header with Login/Register -->
    <header class="flex justify-between items-center p-6  -mt-16">
      <div class = "flex items-center gap-2">
        <img src = './assets/logo.png' alt="ApolloTune Logo" class="w-40 h-40 object-contain" />
        <span class="text-2xl font-bold"></span>
      </div>   
      <div class="flex gap-4">
        <button 
          class="px-4 py-2 border border-amber-400 text-amber-400 rounded-lg hover:bg-amber-400 hover:text-white transition"
        >
          Login
        </button>
        <button 
          class="px-4 py-2 border border-amber-400 text-amber-400 rounded-lg hover:bg-amber-400 hover:text-white transition"
        >
          Register
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex flex-col items-center justify-center px-6 py-12">
      <!-- Radio Dial Component -->
      <RadioDial />
      
      <!-- Active Streamers Section -->
      <section class="w-full max-w-2xl">
        <h2 class="text-xl font-semibold mb-4 text-center " hidden="true">Live Now</h2>
        <div class="text-gray-500 text-center" hidden="true">No active streamers</div>
      </section>
    </main>
  </div>
</template>

<script setup>
import RadioDial from './components/RadioDial.vue'
</script>

<style>
</style>