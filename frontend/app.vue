<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <h1 class="header-title">
          🏛️ Mahabharata AI Sage
        </h1>
        <p class="header-subtitle">
          Step into the epic world of the Mahabharata! Ask questions, explore characters, and unravel mysteries.
        </p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Chat Container -->
      <div class="chat-container">
        <!-- Chat Messages -->
        <div ref="chatContainer" class="chat-messages">
          <div v-if="messages.length === 0" class="welcome-message">
            <div class="welcome-icon">🕉️</div>
            <h3 class="welcome-title">Welcome to the Mahabharata AI Sage</h3>
            <p class="header-subtitle">Ask me anything about the great epic and its characters!</p>
          </div>
          
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message-fade-in"
          >
            <ChatMessage 
              :message="message" 
              @listen-hindi="handleListenHindi"
            />
          </div>
          
          <!-- Typing Indicator -->
          <div v-if="isTyping" class="typing-indicator">
            <div class="typing-dots">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
            <span style="color: #6b7280;">AI Sage is thinking...</span>
          </div>
        </div>

        <!-- Input Section -->
        <div class="chat-input-section">
          <!-- Example Questions -->
          <div v-if="messages.length === 0" class="examples-section">
            <p class="examples-title">Example Questions:</p>
            <div class="examples-grid">
              <button
                v-for="example in examples"
                :key="example"
                @click="sendMessage(example)"
                :disabled="isLoading"
                class="example-button"
              >
                {{ example }}
              </button>
            </div>
          </div>
          
          <!-- Message Input -->
          <form @submit.prevent="handleSubmit" class="input-form">
            <input
              v-model="currentMessage"
              type="text"
              placeholder="Ask about the Mahabharata..."
              :disabled="isLoading"
              class="input-field"
            />
            <button
              type="submit"
              :disabled="isLoading || !currentMessage.trim()"
              class="btn-primary"
            >
              <span v-if="isLoading">Sending...</span>
              <span v-else>Send</span>
            </button>
          </form>

          <!-- Clear Chat Button -->
          <div v-if="messages.length > 0" style="text-align: center;">
            <button
              @click="clearChat"
              :disabled="isLoading"
              class="btn-secondary"
            >
              🗑️ Clear Chat
            </button>
          </div>
        </div>
      </div>

      <!-- Audio Player (Hidden) -->
      <audio ref="audioPlayer" controls class="hidden" @ended="audioEnded">
        Your browser does not support the audio element.
      </audio>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <p>Powered by GPT-4o • Built with FastAPI & Nuxt.js</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

// Generate UUID without external library
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c == 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

// Reactive data
const messages = ref([])
const currentMessage = ref('')
const isLoading = ref(false)
const isTyping = ref(false)
const chatContainer = ref(null)
const audioPlayer = ref(null)
const sessionId = ref('')

// Configuration
const config = useRuntimeConfig()
const API_BASE = config.public.apiBase

// Example questions
const examples = ref([])

// Initialize session
onMounted(async () => {
  sessionId.value = generateUUID()
  await fetchExamples()
})

// Fetch example questions
async function fetchExamples() {
  try {
    const response = await fetch(`${API_BASE}/examples`)
    const data = await response.json()
    examples.value = data.examples.slice(0, 6) // Show first 6 examples
  } catch (error) {
    console.error('Failed to fetch examples:', error)
    // Fallback examples
    examples.value = [
      "Why did the Mahabharata war happen?",
      "Who killed Karna, and why?",
      "Who killed Ghatotakach?",
      "Who were the siblings of Karna?",
      "What was the role of Krishna during the war?",
      "Who was the wife of all five Pandavas?"
    ]
  }
}

// Handle form submission
async function handleSubmit() {
  if (!currentMessage.value.trim() || isLoading.value) return
  await sendMessage(currentMessage.value)
  currentMessage.value = ''
}

// Send message to API
async function sendMessage(message) {
  if (isLoading.value) return
  
  isLoading.value = true
  isTyping.value = true
  
  // Add user message
  messages.value.push({
    role: 'user',
    content: message,
    timestamp: new Date()
  })
  
  await scrollToBottom()
  
  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        session_id: sessionId.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Add assistant response
    messages.value.push({
      role: 'assistant',
      content: data.message,
      timestamp: new Date(),
      sources: data.sources || [],
      totalTokens: data.total_tokens || 0,
      timeTaken: data.time_taken || 0,
      model: data.model || 'gpt-4o'
    })
    
    sessionId.value = data.session_id
    
  } catch (error) {
    console.error('Error sending message:', error)
    messages.value.push({
      role: 'assistant',
      content: "I'm sorry, there was an error processing your request. Please try again.",
      timestamp: new Date(),
      isError: true
    })
  } finally {
    isLoading.value = false
    isTyping.value = false
    await scrollToBottom()
  }
}

// Handle Hindi audio generation
async function handleListenHindi(messageContent) {
  if (!messageContent) return
  
  try {
    // Show loading state for audio
    const response = await fetch(`${API_BASE}/audio/hindi`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: messageContent
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    // Get audio blob and play
    const audioBlob = await response.blob()
    const audioUrl = URL.createObjectURL(audioBlob)
    
    if (audioPlayer.value) {
      audioPlayer.value.src = audioUrl
      audioPlayer.value.play()
    }
    
  } catch (error) {
    console.error('Error generating Hindi audio:', error)
    alert('Sorry, there was an error generating the Hindi audio. Please try again.')
  }
}

// Audio ended event
function audioEnded() {
  // Clean up object URL
  if (audioPlayer.value && audioPlayer.value.src) {
    URL.revokeObjectURL(audioPlayer.value.src)
  }
}

// Clear chat
async function clearChat() {
  if (isLoading.value) return
  
  try {
    await fetch(`${API_BASE}/chat/${sessionId.value}`, {
      method: 'DELETE'
    })
    
    messages.value = []
    sessionId.value = generateUUID()
    
  } catch (error) {
    console.error('Error clearing chat:', error)
    // Clear locally even if API call fails
    messages.value = []
    sessionId.value = generateUUID()
  }
}

// Scroll to bottom
async function scrollToBottom() {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}
</script>