<template>
    <!-- Radio Dial Component -->
    <div 
        class="radio-dial-wrapper" 
        ref="dialWrapper"
        tabindex="0"
        @mousemove="handleMouseMove"
        @click="selectFrequency"
    >
        <!-- Spinning wheel ring -->
        <div class="spinning-wheel" :style="{ transform: `rotate(${rotation}deg)` }">
            <div class="tick" v-for="n in 60" :key="n" :style="{ transform: `rotate(${n * 6}deg)` }">
                <div :class="['tick-mark', n % 5 === 0 ? 'tick-major' : 'tick-minor']"></div>
            </div>
        </div>
        
        <!-- Main dial container -->
        <div class="radio-dial-container items-center justify-center">
            <div class="dial">
                <div class="pointer" :style="{ transform: `rotate(${rotation}deg)` }"></div>
                <div class="display">
                    <div class="frequency">{{ currentFrequency.toFixed(1) }}</div>
                    <div class="station">{{ selectedStation || 'Tune In' }}</div>
                    <div class="hint">Press Enter to select</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['frequencySelected'])

const dialWrapper = ref(null)
const rotation = ref(0)
const selectedStation = ref('')

// FM frequency range: 88.0 - 108.0 MHz
const MIN_FREQ = 88.0
const MAX_FREQ = 108.0

const currentFrequency = computed(() => {
    // Map rotation (0-360) to frequency (88.0-108.0)
    const normalizedRotation = ((rotation.value % 360) + 360) % 360
    return MIN_FREQ + (normalizedRotation / 360) * (MAX_FREQ - MIN_FREQ)
})

function handleMouseMove(event) {
    if (!dialWrapper.value) return
    
    const rect = dialWrapper.value.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2
    
    const deltaX = event.clientX - centerX
    const deltaY = event.clientY - centerY
    
    // Calculate angle in degrees
    let angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI)
    // Adjust so 0 degrees is at the top
    angle = angle + 90
    
    rotation.value = angle
}

function selectFrequency() {
    const freq = currentFrequency.value.toFixed(1)
    selectedStation.value = `${freq} FM`
    emit('frequencySelected', {
        frequency: parseFloat(freq),
        rotation: rotation.value
    })
}
</script>

<style scoped>
.radio-dial-wrapper {
    position: relative;
    width: 340px;
    height: 340px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: crosshair;
    outline: none;
}

.radio-dial-wrapper:focus {
    outline: 2px solid #fbbf24;
    outline-offset: 10px;
    border-radius: 50%;
}

.spinning-wheel {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    transition: transform 0.1s ease-out;
}

.tick {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
}

.tick-mark {
    position: absolute;
    top: 0;
    background: linear-gradient(to bottom, #fbbf24, #a77905);
    border-radius: 2px;
}

.tick-major {
    width: 4px;
    height: 16px;
    box-shadow: 0 0 6px rgba(251, 191, 36, 0.6);
}

.tick-major-major {
    width: 4px;
    height: 16px;
    box-shadow: 0 0 6px rgba(251, 191, 36, 0.6);
}

.tick-minor {
    width: 2px;
    height: 8px;
    opacity: 0.5;
}

.radio-dial-container {
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle, #a77905, #111827);
    box-shadow: 
        0 0 20px rgba(251, 191, 36, 0.3),
        inset 0 0 30px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
}

.dial {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.display {
    text-align: center;
}

.frequency {
    font-size: 2.5rem;
    font-weight: bold;
    color: #fbbf24;
    text-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
}

.station {
    font-size: 1rem;
    color: #d4a017;
    margin-top: 0.5rem;
}

.hint {
    font-size: 0.75rem;
    color: #888;
    margin-top: 0.75rem;
    opacity: 0.7;
}


</style>

