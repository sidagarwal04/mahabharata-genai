<template>
  <div class="app-layout">
    <!-- Content Container (for centered layout) -->
    <div class="content-container">
      <!-- Header -->
      <header class="header">
        <div class="header-content">
          <NuxtLink to="/" class="header-brand-link">
            <h1 class="header-title">
              <img src="~/assets/logo.png" alt="Logo" />
              MAHABHARATA AI SAGE
            </h1>
            <p class="header-subtitle">
              Voyage through the cosmic tapestry of the Great Epic
            </p>
          </NuxtLink>
        </div>
      </header>

      <!-- Main Content -->
      <main class="main-content">
      <!-- Chat Container -->
      <div class="chat-container">
        <!-- Chat Messages -->
        <div ref="chatContainer" class="chat-messages">
          <div v-if="messages.length === 0" class="welcome-message">
            <div class="welcome-icon">
              <img src="~/assets/logo.png" alt="Logo" />
            </div>
            <h3 class="welcome-title">The AI Sage Awaits</h3>
            <p class="welcome-description">
              Seek the ancient wisdom of the Bharata. Inquire about the divine laws of Dharma, 
              the legendary warriors of the Kuru dynasty, and the cosmic tapestry of the Great Epic.
            </p>
            
            <!-- Example Questions Moved Here -->
            <div class="examples-section w-full max-w-2xl px-4">
              <p class="examples-title mb-4 opacity-50 text-xs tracking-widest uppercase">Divine Inquiries</p>
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
          </div>
          
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message-fade-in"
          >
            <ChatMessage 
              :message="message" 
              :active-audio-id="activeAudioId"
              :is-audio-playing="isAudioPlaying"
              :generating-audio-id="generatingAudioId"
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
            <span style="color: var(--accent-cyan);">AI Sage is recalling....</span>
          </div>
        </div>

        <!-- Input Section -->
        <div class="chat-input-section">
          
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
              <span v-if="isLoading">Channeling...</span>
              <span v-else>Seek Wisdom</span>
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
      <audio 
        ref="audioPlayer" 
        class="hidden" 
        @ended="audioEnded"
        @play="handleAudioPlay"
        @pause="handleAudioPause"
      >
        Your browser does not support the audio element.
      </audio>
    </main>
    </div>
    <!-- End Content Container -->

    <!-- Footer (Full Width) -->
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-links">
          <a href="#" @click.prevent="openAboutModal" class="footer-link">
            <span class="footer-icon">🕉️</span>
            About
          </a>
          <a href="#" class="footer-link">
            <span class="footer-icon">⚖️</span>
            Dharma
          </a>
          <a href="https://sidagarwal04.medium.com/list/mahabharatachatbot-cbf1d049d017" target="_blank" class="footer-link">
            <span class="footer-icon">🏹</span>
            Wisdom
          </a>
          <a href="https://github.com/sidagarwal04/mahabharata-genai" target="_blank" class="footer-link">
            <span class="footer-icon">📖</span>
            Repository
          </a>
        </div>
        
        <div class="footer-credits">
          <span class="footer-powered">Powered by AI • Built with ❤️ for seekers of ancient wisdom</span>
          <div class="footer-copyright">
            © 2026 Mahabharata AI Sage • <a href="https://meetsid.dev" target="_blank" class="footer-author">meetsid.dev</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- About Modal -->
    <div v-if="showAboutModal" class="modal-overlay" @click="closeAboutModal">
      <div class="modal-container" @click.stop>
        <button class="modal-close-btn" @click="closeAboutModal">
          <span class="close-icon">✕</span>
        </button>
        
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-brand">
              <img src="~/assets/logo.png" alt="Mahabharata AI Logo" class="modal-logo" />
              <div class="modal-brand-text">
                <h2 class="modal-title">Mahabharata AI Sage</h2>
                <p class="modal-tagline">Step into the epic world of the Mahabharata</p>
              </div>
            </div>
          </div>
          
          <div class="modal-body">
            <!-- Features Grid -->
            <div class="features-grid">
              <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">GPT-5.2 Powered</h3>
                <p class="feature-text">Advanced AI responses using OpenAI's latest model</p>
              </div>
              
              <div class="feature-card">
                <div class="feature-icon">🗄️</div>
                <h3 class="feature-title">Graph Database</h3>
                <p class="feature-text">Neo4j-powered knowledge graph for rich contextual information</p>
              </div>
              
              <div class="feature-card">
                <div class="feature-icon">🇮🇳</div>
                <h3 class="feature-title">Hindi Audio</h3>
                <p class="feature-text">Listen to responses in Hindi using Sarvam AI TTS</p>
              </div>
              
              <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3 class="feature-title">Responsive Design</h3>
                <p class="feature-text">Works perfectly on desktop and mobile devices</p>
              </div>
            </div>
            
            <!-- Tech Stack -->
            <div class="tech-section">
              <h3 class="tech-title">🏗️ Modern Architecture</h3>
              <div class="tech-stack">
                <div class="tech-item">
                  <span class="tech-label">Frontend:</span>
                  <span class="tech-value">Nuxt.js 3, TypeScript, Tailwind CSS</span>
                </div>
                <div class="tech-item">
                  <span class="tech-label">Backend:</span>
                  <span class="tech-value">FastAPI, Neo4j, OpenAI GPT-5.2</span>
                </div>
                <div class="tech-item">
                  <span class="tech-label">AI Services:</span>
                  <span class="tech-value">Sarvam AI TTS, Graph-based RAG</span>
                </div>
              </div>
            </div>
            
            <!-- Credits & Links -->
            <div class="credits-section">
              <div class="credits-content">
                <div class="credits-text">
                  <p>📖 <a href="https://sidagarwal04.medium.com/list/mahabharatachatbot-cbf1d049d017" target="_blank" class="credit-link">Read the Blog Series</a></p>
                  <p>🔗 <a href="https://github.com/sidagarwal04/mahabharata-genai" target="_blank" class="credit-link">Explore the Code</a></p>
                </div>
                <div class="credits-author">
                  <p>Built with ❤️ by <a href="https://meetsid.dev" target="_blank" class="credit-link">meetsid.dev</a></p>
                  <p class="credits-purpose">Making ancient wisdom accessible through modern AI</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'

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
const generatingAudioId = ref(null)
const showAboutModal = ref(false)

// Watch for messages change to scroll to bottom
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// Watch for typing state to scroll
watch(isTyping, (val) => {
  if (val) {
    scrollToBottom()
  }
})

// Audio playback state
const activeAudioId = ref(null)
const isAudioPlaying = ref(false)

// Configuration
const config = useRuntimeConfig()
const API_BASE = config.public.apiBase

// Example questions
const examples = ref([])

// Initialize session
onMounted(async () => {
  sessionId.value = generateUUID()
  await fetchExamples()
  
  // Add ESC key listener for modal
  document.addEventListener('keydown', handleKeyDown)
})

// Cleanup event listener
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

// Handle ESC key press
function handleKeyDown(event) {
  if (event.key === 'Escape' && showAboutModal.value) {
    closeAboutModal()
  }
}

// Modal control functions
function openAboutModal() {
  showAboutModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeAboutModal() {
  showAboutModal.value = false
  document.body.style.overflow = 'auto'
}

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
    id: generateUUID(),
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
    const assistantMessage = {
      id: generateUUID(),
      role: 'assistant',
      content: data.message,
      timestamp: new Date(),
      sources: data.sources || [],
      totalTokens: data.total_tokens || 0,
      timeTaken: data.time_taken || 0,
      model: data.model || 'gpt-5.2'
    }
    messages.value.push(assistantMessage)
    
    sessionId.value = data.session_id
    
    // Pre-generate audio in background without playing
    handleListenHindi(assistantMessage, false)
    
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

// Handle Hindi audio generation and playback
async function handleListenHindi(message, autoplay = true) {
  if (!message.content || generatingAudioId.value === message.id) return
  
  // If message already has pre-generated audio, just play/toggle it
  if (message.audioUrl) {
    if (activeAudioId.value === message.id) {
      if (autoplay) toggleAudio()
    } else {
      activeAudioId.value = message.id
      audioPlayer.value.src = message.audioUrl
      if (autoplay) {
        audioPlayer.value.play()
        isAudioPlaying.value = true
      }
    }
    return
  }

  try {
    generatingAudioId.value = message.id
    const response = await fetch(`${API_BASE}/audio/hindi`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: message.content
      })
    })
    
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    
    const audioBlob = await response.blob()
    const audioUrl = URL.createObjectURL(audioBlob)
    
    // Store URL on message so it's ready for instant playback
    message.audioUrl = audioUrl
    
    // Only play if autoplay is requested (manual clicks)
    if (autoplay && audioPlayer.value) {
      activeAudioId.value = message.id
      audioPlayer.value.src = audioUrl
      audioPlayer.value.play()
      isAudioPlaying.value = true
    }
    
  } catch (error) {
    console.error('Error generating Hindi audio:', error)
    alert('Sorry, there was an error generating the Hindi audio.')
    activeAudioId.value = null
  } finally {
    generatingAudioId.value = null
  }
}

function toggleAudio() {
  if (!audioPlayer.value) return
  
  if (audioPlayer.value.paused) {
    audioPlayer.value.play()
    isAudioPlaying.value = true
  } else {
    audioPlayer.value.pause()
    isAudioPlaying.value = false
  }
}

function handleAudioPlay() {
  isAudioPlaying.value = true
}

function handleAudioPause() {
  isAudioPlaying.value = false
}

// Audio ended event
function audioEnded() {
  isAudioPlaying.value = false
  activeAudioId.value = null
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