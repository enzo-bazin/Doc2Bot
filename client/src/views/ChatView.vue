<script setup>
import { ref, nextTick } from 'vue'
import api from '@/api'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const uploadFile = ref(null)
const uploading = ref(false)
const uploadStatus = ref('')
const messagesEnd = ref(null)

async function sendMessage() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', text })
  input.value = ''
  loading.value = true
  await scrollBottom()

  try {
    const { data } = await api.post('/chatbot/chat', { message: text })
    messages.value.push({ role: 'bot', text: data.response })
  } catch (e) {
    messages.value.push({ role: 'error', text: e.response?.data?.detail || 'Erreur serveur' })
  } finally {
    loading.value = false
    await scrollBottom()
  }
}

async function uploadDocument(e) {
  const file = e.target.files[0]
  if (!file) return

  uploadFile.value = file.name
  uploading.value = true
  uploadStatus.value = ''

  const form = new FormData()
  form.append('file', file)

  try {
    await api.post('/session/create', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    uploadStatus.value = 'success'
    messages.value.push({ role: 'system', text: `Document "${file.name}" envoyé, traitement en cours...` })
  } catch (e) {
    uploadStatus.value = 'error'
    messages.value.push({ role: 'error', text: e.response?.data?.detail || 'Échec de l\'upload' })
  } finally {
    uploading.value = false
    e.target.value = ''
    await scrollBottom()
  }
}

async function scrollBottom() {
  await nextTick()
  messagesEnd.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="layout">
    <header class="topbar">
      <span class="brand">Doc2Bot</span>
      <div class="topbar-right">
        <label class="upload-btn" :class="{ loading: uploading }">
          <input type="file" accept=".pdf,.txt,.docx" @change="uploadDocument" />
          {{ uploading ? 'Upload...' : '+ Document' }}
        </label>
      </div>
    </header>

    <main class="messages" ref="messagesContainer">
      <div v-if="messages.length === 0" class="empty">
        Envoyez un message ou chargez un document pour commencer.
      </div>

      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['message', msg.role]"
      >
        <span class="bubble">{{ msg.text }}</span>
      </div>

      <div v-if="loading" class="message bot">
        <span class="bubble typing">...</span>
      </div>

      <div ref="messagesEnd" />
    </main>

    <footer class="inputbar">
      <input
        v-model="input"
        type="text"
        placeholder="Votre message..."
        @keydown.enter.prevent="sendMessage"
      />
      <button @click="sendMessage" :disabled="loading || !input.trim()">Envoyer</button>
    </footer>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0f172a;
  color: #f8fafc;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  background: #1e293b;
  border-bottom: 1px solid #334155;
  flex-shrink: 0;
}

.brand {
  font-size: 1.2rem;
  font-weight: 700;
  color: #6366f1;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.upload-btn {
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  background: #334155;
  color: #f8fafc;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
}

.upload-btn input {
  display: none;
}

.upload-btn:hover {
  background: #475569;
}

.upload-btn.loading {
  opacity: 0.6;
  cursor: not-allowed;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty {
  text-align: center;
  color: #475569;
  margin: auto;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.bot,
.message.system {
  justify-content: flex-start;
}

.message.error {
  justify-content: center;
}

.bubble {
  max-width: 70%;
  padding: 0.6rem 1rem;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 0.95rem;
  white-space: pre-wrap;
  word-break: break-word;
}

.user .bubble {
  background: #6366f1;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.bot .bubble {
  background: #1e293b;
  color: #f8fafc;
  border-bottom-left-radius: 4px;
}

.system .bubble {
  background: #164e63;
  color: #7dd3fc;
  font-size: 0.85rem;
}

.error .bubble {
  background: #450a0a;
  color: #f87171;
  font-size: 0.85rem;
}

.typing {
  letter-spacing: 0.2em;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.inputbar {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: #1e293b;
  border-top: 1px solid #334155;
  flex-shrink: 0;
}

.inputbar input {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #0f172a;
  color: #f8fafc;
  font-size: 1rem;
}

.inputbar input:focus {
  outline: none;
  border-color: #6366f1;
}

.inputbar button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.inputbar button:hover:not(:disabled) {
  background: #4f46e5;
}

.inputbar button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
