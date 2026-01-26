<template>
  <div class="flex" :class="message.role === 'user' ? 'justify-end' : 'justify-start'">
    <div class="chat-bubble" :class="bubbleClass">
      <!-- Avatar and Role -->
      <div class="flex items-start message-header">
        <!-- Optimized Avatar Size -->
        <div class="flex-shrink-0 mr-3">
          <div class="w-6 h-6 rounded-full flex items-center justify-center bg-white/10 border border-white/20 overflow-hidden">
            <span v-if="message.role === 'user'" class="text-xs leading-none">👤</span>
            <img v-else src="~/assets/logo.png" alt="AI Sage" class="w-3 h-3 object-contain" />
          </div>
        </div>
        
        <div class="flex-1 min-w-0">
          <!-- Message Content -->
          <div class="prose prose-invert prose-sm max-w-none">
            <div class="content-text leading-tight" v-html="formattedContent"></div>
          </div>
        </div>
      </div>
      
      <!-- Assistant Actions Below Content -->
      <div v-if="message.role === 'assistant' && !message.isError" class="mt-4 pl-9">
        <button
          @click="$emit('listen-hindi', message)"
          class="listen-btn"
          :class="{ 'playing': isPlaybackActive, 'generating': isGeneratingAudio }"
        >
          <div class="flex items-center gap-2">
            <!-- Loading Spinner for Generating -->
            <svg v-if="isGeneratingAudio" class="animate-spin h-3.5 w-3.5 text-cyan-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <!-- Play Icon -->
            <svg v-else-if="!isPlaybackActive" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            </svg>
            <!-- Pause Icon -->
            <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6" />
            </svg>
            <span class="font-medium tracking-wide">{{ isGeneratingAudio ? 'Engraving the Eternal Word...' : (isPlaybackActive ? 'Pause Playback' : 'Listen in Hindi') }}</span>
          </div>
        </button>
      </div>
      

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  activeAudioId: {
    type: String,
    default: null
  },
  isAudioPlaying: {
    type: Boolean,
    default: false
  },
  generatingAudioId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['listen-hindi'])

const isPlaybackActive = computed(() => {
  return props.activeAudioId === props.message.id && props.isAudioPlaying
})

const isGeneratingAudio = computed(() => {
  return props.generatingAudioId === props.message.id
})

const bubbleClass = computed(() => {
  if (props.message.role === 'user') {
    return 'user-bubble'
  } else if (props.message.isError) {
    return 'assistant-bubble border-red-200 bg-red-50'
  } else {
    return 'assistant-bubble'
  }
})

const formattedContent = computed(() => {
  let content = props.message.content
  
  // Convert newlines to HTML breaks
  content = content.replace(/\n/g, '<br>')
  
  // Simple markdown-like formatting
  content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  content = content.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Convert URLs to links
  content = content.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">$1</a>'
  )
  
  return content
})

function formatTime(timestamp) {
  if (!timestamp) return ''
  
  const now = new Date()
  const messageTime = new Date(timestamp)
  const diffInSeconds = Math.floor((now - messageTime) / 1000)
  
  if (diffInSeconds < 60) {
    return messageTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60)
    return `${minutes} min${minutes === 1 ? '' : 's'} ago`
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600)
    return `${hours} hour${hours === 1 ? '' : 's'} ago`
  } else {
    return messageTime.toLocaleString()
  }
}
</script>