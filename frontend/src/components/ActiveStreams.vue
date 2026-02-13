<template>
    <div class = "mt-15 border border-amber-400 rounded-lg p-4">
        <h2 class = "text-2xl font-bold mb-4 text-center">Active Streamers</h2>
        <ul v-if="streamers.length" class="space-y-3">
            <li 
                v-for="streamer in streamers" 
                :key="streamer.id"
                class="flex items-center justify-between p-4 bg-gray-800 rounded-lg border border-gray-700 hover:border-amber-400 transition"
            >
                <div>
                <span class="font-semibold text-white">{{ streamer.name }}</span>
                <span class="text-sm text-gray-400 ml-2">{{ streamer.genre }}</span>
                </div>
                <div class="flex items-center gap-3">
                <span class="text-amber-400 font-mono">{{ streamer.frequency }} FM</span>
                <span class="text-xs text-green-400">● LIVE</span>
                </div>
            </li>
        </ul>
        <p v-else class="text-gray-500">No active streams right now.</p>
    </div>
</template>



<script setup>
defineProps({
    streamers: {
        type: Array,
        required: true,
        default: () => []
    }
})
</script>
