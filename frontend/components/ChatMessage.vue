<template>
  <div class="flex" :class="message.role === 'user' ? 'justify-end' : 'justify-start'">
    <div class="chat-bubble" :class="bubbleClass">
      <!-- Avatar and Role -->
      <div class="flex items-start space-x-3">
        <div class="flex-shrink-0">
          <div class="w-4 h-4 flex-shrink-0 flex items-center justify-center mt-1">
            <span v-if="message.role === 'user'" class="text-sm">👤</span>
            <img v-else src="~/assets/logo.png" alt="AI Sage" class="w-full h-full object-contain" />
          </div>
        </div>
        
        <div class="flex-1">
          <!-- Message Content -->
          <div class="prose prose-sm max-w-none">
            <div class="whitespace-pre-wrap" v-html="formattedContent"></div>
          </div>
          
          <!-- Assistant Message Metadata -->
          <div v-if="message.role === 'assistant' && !message.isError" class="mt-3 pt-3 border-t border-gray-200">
            <!-- Metadata (Audio Only) -->
            <div class="flex items-center justify-end text-xs text-gray-500">
              
              <!-- Hindi Audio Button -->
              <button
                @click="$emit('listen-hindi', message)"
                class="flex items-center space-x-1 px-2 py-1 bg-orange-100 text-orange-700 rounded hover-orange transition-colors"
                title="Listen in Hindi"
              >
                <!-- Play Icon -->
                <svg v-if="!isPlaybackActive" class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
                <!-- Pause Icon -->
                <svg v-else class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                </svg>
                <span>{{ isPlaybackActive ? 'Pause' : 'Listen in Hindi' }}</span>
              </button>
            </div>
          </div>
        </div>
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