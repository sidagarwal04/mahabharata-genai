<template>
  <div class="flex" :class="message.role === 'user' ? 'justify-end' : 'justify-start'">
    <div class="chat-bubble" :class="bubbleClass">
      <!-- Avatar and Role -->
      <div class="flex items-start space-x-3">
        <div class="flex-shrink-0">
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-lg">
            <span v-if="message.role === 'user'">👤</span>
            <span v-else>🕉️</span>
          </div>
        </div>
        
        <div class="flex-1">
          <!-- Message Content -->
          <div class="prose prose-sm max-w-none">
            <div class="whitespace-pre-wrap" v-html="formattedContent"></div>
          </div>
          
          <!-- Assistant Message Metadata -->
          <div v-if="message.role === 'assistant' && !message.isError" class="mt-3 pt-3 border-t border-gray-200">
            <!-- Sources -->
            <div v-if="message.sources && message.sources.length > 0" class="mb-2">
              <p class="text-xs font-medium text-gray-600 mb-1">Sources:</p>
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="source in message.sources"
                  :key="source"
                  class="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                >
                  {{ source }}
                </span>
              </div>
            </div>
            
            <!-- Metadata -->
            <div class="flex items-center justify-between text-xs text-gray-500">
              <div class="flex items-center space-x-3">
                <span>{{ message.model || 'GPT-4o' }}</span>
                <span v-if="message.totalTokens">{{ message.totalTokens }} tokens</span>
                <span v-if="message.timeTaken">{{ message.timeTaken.toFixed(2) }}s</span>
              </div>
              
              <!-- Hindi Audio Button -->
              <button
                @click="$emit('listen-hindi', message.content)"
                class="flex items-center space-x-1 px-2 py-1 bg-orange-100 text-orange-700 rounded hover:bg-orange-200 transition-colors"
                title="Listen in Hindi"
              >
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                </svg>
                <span>🇮🇳</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Timestamp -->
      <div class="text-xs text-gray-400 mt-2 text-right">
        {{ formatTime(message.timestamp) }}
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
  }
})

const emit = defineEmits(['listen-hindi'])

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
    return 'Just now'
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