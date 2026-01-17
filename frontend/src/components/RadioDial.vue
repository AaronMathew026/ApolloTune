<script setup>
import {ref, onMounted, onUnmounted} from 'vue';

const props = defineProps({
    modelValue: { type : Number, required: true},
    min: { type : Number, default: 88.0},
    max: { type : Number, default: 108.0},
})

const emit = defineEmits(['update:modelValue'])

</script>