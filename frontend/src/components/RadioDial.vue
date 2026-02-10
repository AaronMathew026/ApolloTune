<template>
    <!-- Radio Dial Component -->
    <div class="radio-dial-container items-center justify-center px-6 py-12">
        <div class = "dial">
            <div class = "pointer"></div>
                <div class = "display">
                    <div class = "frequency">88.5</div>
                    <div class = "station">Jazz FM</div>
                </div>
        </div>
    </div>


</template>

<style scoped>
.radio-dial-container {
    width: 300px;
    height: 300px;
    border-radius: 60%;
    background: radial-gradient(circle, #a77905, #111827);
    box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
    display: flex;
}
.dial {
    width: 2px;
    height: 10px;

}
</style>