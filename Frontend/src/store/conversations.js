import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useConversationsStore = defineStore('conversations', () => {
  const conversations = ref([])
  const selectedId = ref(null)

  const activeConvo = computed(() =>
    conversations.value.find(c => c.id === selectedId.value)
  )

  function setConversations(data) {
    conversations.value = data
  }

  function selectConversation(id) {
    selectedId.value = id
    const convo = conversations.value.find(c => c.id === id)
    if (convo) convo.unread = 0
  }

  function sendMessage(text) {
    if (!activeConvo.value) return
    activeConvo.value.messages.push({
      text,
      mine: true,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      date: 'Today',
    })
    const convo = conversations.value.find(c => c.id === selectedId.value)
    if (convo) { convo.preview = text; convo.time = 'Just now' }
  }

  return { conversations, selectedId, activeConvo, setConversations, selectConversation, sendMessage }
})