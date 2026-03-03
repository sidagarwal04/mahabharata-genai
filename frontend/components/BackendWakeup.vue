<template>
  <div class="wakeup-container">
    <div class="wakeup-content">
      <!-- Logo -->
      <!-- <div class="wakeup-logo-section">
        <img src="~/assets/logo.png" alt="Mahabharata AI Sage Logo" class="wakeup-logo" />
      </div> -->
      
      <!-- Title -->
      <h1 class="wakeup-title">Mahabharata AI Sage</h1>
      
      <!-- Loading Message -->
      <div class="wakeup-message">
        <p class="wakeup-text">{{ message }}</p>
      </div>
      
      <!-- Animated Loading Indicator -->
      <div class="wakeup-loader">
        <div class="spinner"></div>
        <p class="wakeup-status">{{ statusMessage }}</p>
      </div>
      
      <!-- Motivational Quote -->
      <div class="wakeup-quote">
        <p class="quote-text">"All great journeys begin with a single moment of patience..."</p>
        <p class="quote-author">— Wisdom from the Mahabharata</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  retryCount: {
    type: Number,
    default: 0
  }
})

const loadingStages = [
  'Awakening the cosmic service...',
  'Connecting to the ancient wisdom library...',
  'Initializing the AI Sage...',
  'Preparing the knowledge base...',
  'Channeling the divine insights...'
]

const currentStageIndex = ref(0)
let stageInterval = null

const message = computed(() => {
  return "Waking up the service, kindly wait..."
})

const statusMessage = computed(() => {
  return loadingStages[currentStageIndex.value % loadingStages.length]
})

onMounted(() => {
  // Cycle through loading messages
  stageInterval = setInterval(() => {
    currentStageIndex.value += 1
  }, 2500)
})

onUnmounted(() => {
  if (stageInterval) {
    clearInterval(stageInterval)
  }
})
</script>

<style scoped>
.wakeup-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1a1f35 50%, #2a1a3a 100%);
  padding: 20px;
}

.wakeup-content {
  text-align: center;
  max-width: 500px;
}

.wakeup-logo-section {
  margin-bottom: 40px;
  animation: fadeInScale 0.8s ease-out;
}

.wakeup-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  filter: drop-shadow(0 0 20px rgba(34, 211, 238, 0.3));
}

.wakeup-title {
  font-size: 2rem;
  font-weight: 700;
  color: #22d3ee;
  margin-bottom: 20px;
  letter-spacing: 0.05em;
  animation: fadeIn 0.8s ease-out 0.2s both;
}

.wakeup-message {
  margin-bottom: 40px;
  animation: fadeIn 0.8s ease-out 0.4s both;
}

.wakeup-text {
  font-size: 1.25rem;
  color: #e0f2fe;
  line-height: 1.6;
  font-weight: 500;
}

.wakeup-loader {
  margin-bottom: 60px;
  animation: fadeIn 0.8s ease-out 0.6s both;
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 20px;
  border: 3px solid rgba(34, 211, 238, 0.2);
  border-top-color: #22d3ee;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.wakeup-status {
  font-size: 0.95rem;
  color: #a8d8ea;
  min-height: 24px;
  animation: fadeInText 0.5s ease-in-out;
}

.wakeup-quote {
  font-style: italic;
  color: #94a3b8;
  animation: fadeIn 0.8s ease-out 0.8s both;
}

.quote-text {
  font-size: 0.95rem;
  margin-bottom: 10px;
  color: #cbd5e1;
}

.quote-author {
  font-size: 0.85rem;
  color: #64748b;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeInText {
  from {
    opacity: 0.5;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .wakeup-title {
    font-size: 1.5rem;
  }

  .wakeup-text {
    font-size: 1rem;
  }

  .wakeup-logo {
    width: 60px;
    height: 60px;
  }
}
</style>
