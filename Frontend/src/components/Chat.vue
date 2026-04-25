<template>
  <div class="chat-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="brand">
          <div class="brand-avatar">
            <Avatar>
              <AvatarImage src="https://api.dicebear.com/9.x/thumbs/svg?seed=me" />
              <AvatarFallback>Me</AvatarFallback>
            </Avatar>
          </div>
          <div>
            <p class="brand-name">Messages</p>
            <!-- <p class="brand-status">● Online</p> -->
          </div>
        </div>
        <!-- <Button variant="ghost" size="icon" class="compose-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
        </Button> -->
      </div>

      <div class="search-wrap">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </div>
        <Input v-model="searchQuery" placeholder="Search conversations…" class="search-input" />
      </div>

      <ScrollArea class="sidebar-scroll">
        <div class="convo-list">
          <button
            v-for="convo in filteredConversations"
            :key="convo.id"
            class="convo-item"
            :class="{ active: selectedId === convo.id }"
            @click="store.selectConversation(convo.id)"
          >
            <div class="convo-avatar-wrap">
              <Avatar class="convo-avatar">
                <AvatarImage :src="convo.avatar" />
                <AvatarFallback>{{ convo.initials }}</AvatarFallback>
              </Avatar>
              <!-- <span v-if="convo.online" class="online-dot" /> -->
            </div>
            <div class="convo-info">
              <div class="convo-top">
                <span class="convo-name">{{ convo.name }}</span>
                <span class="convo-time">{{ convo.time }}</span>
              </div>
              <div class="convo-bottom">
                <span class="convo-preview">{{ convo.preview }}</span>
                <Badge v-if="convo.unread" class="unread-badge">{{ convo.unread }}</Badge>
              </div>
            </div>
          </button>
        </div>
      </ScrollArea>
    </aside>

    <!-- Main Chat -->
    <main class="chat-main">
      <template v-if="activeConvo">
        <!-- Chat Header -->
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar-wrap">
              <Avatar>
                <AvatarImage :src="activeConvo.avatar" />
                <AvatarFallback>{{ activeConvo.initials }}</AvatarFallback>
              </Avatar>
              <!-- <span v-if="activeConvo.online" class="online-dot" /> -->
            </div>
            <div>
              <p class="chat-name">{{ activeConvo.name }}</p>
              <!-- <p class="chat-status">{{ activeConvo.online ? 'Active now' : 'Offline' }}</p> -->
            </div>
          </div>
          <div class="chat-actions">
            <Button variant="ghost" size="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.41 2 2 0 0 1 3.6 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.61a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.73 16z"/></svg>
            </Button>
            <Button variant="ghost" size="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/></svg>
            </Button>
            <Button variant="ghost" size="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
            </Button>
          </div>
        </div>

        <!-- Messages -->
        <ScrollArea class="messages-scroll" ref="messagesScrollRef">
          <div class="messages-area" ref="messagesEndRef">
            <template v-for="(group, gi) in groupedMessages" :key="gi">
              <!-- Date divider -->
              <div class="date-divider">
                <span>{{ group.date }}</span>
              </div>

              <div
                v-for="(msg, mi) in group.messages"
                :key="mi"
                class="message-row"
                :class="{ 'message-row--mine': msg.mine }"
              >
                <Avatar v-if="!msg.mine" class="msg-avatar" :class="{ invisible: !msg.showAvatar }">
                  <AvatarImage :src="activeConvo.avatar" />
                  <AvatarFallback>{{ activeConvo.initials }}</AvatarFallback>
                </Avatar>

                <div class="bubble-group" :class="{ 'bubble-group--mine': msg.mine }">
                  <div
                    class="bubble"
                    :class="[
                      msg.mine ? 'bubble--mine' : 'bubble--theirs',
                      msg.tail === 'start' ? 'bubble--tail-start' : '',
                      msg.tail === 'end' ? (msg.mine ? 'bubble--tail-end-mine' : 'bubble--tail-end') : '',
                    ]"
                  >
                    {{ msg.text }}
                  </div>
                  <span v-if="msg.showTime" class="msg-time">{{ msg.time }}</span>
                </div>

                <Avatar v-if="msg.mine" class="msg-avatar" :class="{ invisible: !msg.showAvatar }">
                  <AvatarImage src="https://api.dicebear.com/9.x/thumbs/svg?seed=me" />
                  <AvatarFallback>Me</AvatarFallback>
                </Avatar>
              </div>
            </template>

            <!-- Typing indicator -->
            <div v-if="isTyping" class="message-row">
              <Avatar class="msg-avatar">
                <AvatarImage :src="activeConvo.avatar" />
                <AvatarFallback>{{ activeConvo.initials }}</AvatarFallback>
              </Avatar>
              <div class="typing-bubble">
                <span class="dot" />
                <span class="dot" />
                <span class="dot" />
              </div>
            </div>
          </div>
        </ScrollArea>

        <!-- Input Bar -->
        <div class="input-bar">
          <Button variant="ghost" size="icon" class="attach-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
          </Button>
          <Button variant="ghost" size="icon" class="attach-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/></svg>
          </Button>
          <div class="input-wrap">
            <Textarea
              v-model="draft"
              placeholder="Write a message…"
              class="chat-textarea"
              :rows="1"
              @keydown.enter.exact.prevent="sendMessage"
              @click="sendMessage"
            />
          </div>
          <Button
            size="icon"
            class="send-btn"
            :disabled="!draft.trim()"
            @keydown.enter.exact.prevent="sendMessage"
            @click="sendMessage"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
          </Button>
        </div>
      </template>

      <!-- Empty state -->
      <div v-else class="empty-state">
        <div class="empty-icon">💬</div>
        <p class="empty-title">Your messages</p>
        <p class="empty-sub">Select a conversation to start chatting</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'

import { useConversationsStore } from '@/store/conversations'
import conversationData from '@/store/data/conversations.json'
import { storeToRefs } from 'pinia'

// ── Data ──────────────────────────────────────────────────────────────────────
const store = useConversationsStore()
store.setConversations(conversationData)
const { conversations, selectedId, activeConvo } = storeToRefs(store)

const searchQuery = ref('')
const draft = ref('')
const isTyping = ref(false)
const messagesEndRef = ref(null)

// ── Computed ──────────────────────────────────────────────────────────────────

const filteredConversations = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return conversations.value.filter(c =>
    c.name.toLowerCase().includes(q) || c.preview.toLowerCase().includes(q)
  )
})


async function sendMessage() {
  if (!draft.value.trim()) return
  store.sendMessage(draft.value)
  draft.value = ''
  await scrollToBottom()

  // isTyping.value = true
  await scrollToBottom()

  // setTimeout(async () => {
  //   isTyping.value = false
  //   // const replies = ["That's awesome! 😄", "Totally agree!", "Oh interesting, tell me more!", "Got it, thanks!", "Sure, sounds good 👍"]
  //   // store.receiveMessage(replies[Math.floor(Math.random() * replies.length)])
  //   await scrollToBottom()
  // }, 1800)
}

const groupedMessages = computed(() => {
  if (!activeConvo.value) return []
  const msgs = activeConvo.value.messages
  const dateMap = {}

  msgs.forEach((msg, i) => {
    const prev = msgs[i - 1]
    const next = msgs[i + 1]
    const sameAuthorPrev = prev && prev.mine === msg.mine
    const sameAuthorNext = next && next.mine === msg.mine

    let tail = 'middle'
    if (!sameAuthorPrev && !sameAuthorNext) tail = 'solo'
    else if (!sameAuthorPrev) tail = 'start'
    else if (!sameAuthorNext) tail = 'end'

    const enriched = {
      ...msg,
      tail,
      showAvatar: !sameAuthorNext,
      showTime: !sameAuthorNext,
    }

    if (!dateMap[msg.date]) dateMap[msg.date] = []
    dateMap[msg.date].push(enriched)
  })

  return Object.entries(dateMap).map(([date, messages]) => ({ date, messages }))
})

// ── Methods ───────────────────────────────────────────────────────────────────


async function scrollToBottom() {
  await nextTick()
  messagesEndRef.value?.lastElementChild?.scrollIntoView({ behavior: 'smooth' })
}

watch(selectedId, () => nextTick(() => scrollToBottom()))
</script>

<style scoped>
/* ── Layout ──────────────────────────────────────────────────────────────────── */
.chat-layout {
  display: flex;
  height: 100vh;
  background: #fdf8f3;
  font-family: 'Georgia', serif;
  overflow: hidden;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────────── */
.sidebar {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: #fff8f1;
  border-right: 1.5px solid #f0dece;
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 16px 12px;
  border-bottom: 1px solid #f0dece;
}

.brand { display: flex; align-items: center; gap: 10px; }
.brand-name { font-size: 1rem; font-weight: 700; color: #3d2c1e; letter-spacing: -0.01em; }
.brand-status { font-size: 0.72rem; color: #84b87a; font-family: sans-serif; }

.compose-btn { color: #b87a5a; }

.search-wrap {
  position: relative;
  padding: 10px 14px;
}
.search-icon {
  position: absolute;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);
  color: #c4a48a;
  pointer-events: none;
}
.search-input {
  padding-left: 2rem;
  background: #fdf0e6;
  border: 1px solid #e8cdb0;
  border-radius: 999px;
  font-size: 0.85rem;
  color: #3d2c1e;
}
.search-input::placeholder { color: #c4a48a; }

.sidebar-scroll { flex: 1; overflow: hidden; }

.convo-list { display: flex; flex-direction: column; padding: 4px 8px; }

.convo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 10px;
  border-radius: 14px;
  border: none;
  background: transparent;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
  width: 100%;
}
.convo-item:hover { background: #fdeede; }
.convo-item.active { background: #fde3c8; }

.convo-avatar-wrap { position: relative; flex-shrink: 0; }
.convo-avatar { width: 44px; height: 44px; }

.online-dot {
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 10px;
  height: 10px;
  background: #84b87a;
  border-radius: 50%;
  border: 2px solid #fff8f1;
}

.convo-info { flex: 1; min-width: 0; }
.convo-top { display: flex; justify-content: space-between; align-items: baseline; }
.convo-name { font-size: 0.9rem; font-weight: 700; color: #3d2c1e; }
.convo-time { font-size: 0.72rem; color: #b89878; font-family: sans-serif; flex-shrink: 0; }
.convo-bottom { display: flex; justify-content: space-between; align-items: center; margin-top: 2px; }
.convo-preview {
  font-size: 0.8rem;
  color: #9a7a62;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  font-family: sans-serif;
}
.unread-badge {
  background: #e07840;
  color: white;
  border-radius: 999px;
  font-size: 0.68rem;
  padding: 1px 7px;
  min-width: 20px;
  text-align: center;
  flex-shrink: 0;
  margin-left: 6px;
  border: none;
}

/* ── Chat Main ───────────────────────────────────────────────────────────────── */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #fdf8f3;
}

/* ── Chat Header ─────────────────────────────────────────────────────────────── */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background: #fff8f1;
  border-bottom: 1.5px solid #f0dece;
  flex-shrink: 0;
}
.chat-header-info { display: flex; align-items: center; gap: 12px; }
.chat-avatar-wrap { position: relative; }
.chat-name { font-size: 1rem; font-weight: 700; color: #3d2c1e; }
.chat-status { font-size: 0.75rem; color: #84b87a; font-family: sans-serif; }
.chat-actions { display: flex; gap: 4px; color: #b87a5a; }

/* ── Messages ────────────────────────────────────────────────────────────────── */
.messages-scroll { flex: 1; overflow: hidden; }

.messages-area {
  padding: 20px 24px 8px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.date-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 16px 0 8px;
}
.date-divider span {
  font-size: 0.72rem;
  color: #b89878;
  background: #f5e8d8;
  border-radius: 999px;
  padding: 3px 12px;
  font-family: sans-serif;
}

.message-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}
.message-row--mine { flex-direction: row-reverse; }

.msg-avatar {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  margin-bottom: 18px;
}
.invisible { visibility: hidden; }

.bubble-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 65%;
}
.bubble-group--mine { align-items: flex-end; }

.bubble {
  padding: 10px 15px;
  border-radius: 18px;
  font-size: 0.9rem;
  line-height: 1.5;
  word-break: break-word;
  font-family: sans-serif;
}

.bubble--theirs {
  background: #fff0e4;
  color: #3d2c1e;
  border: 1px solid #f0dece;
  border-bottom-left-radius: 4px;
}
.bubble--mine {
  background: #e07840;
  color: #fff;
  border-bottom-right-radius: 4px;
}

/* Tail adjustments for grouped messages */
.bubble--tail-start.bubble--theirs { border-bottom-left-radius: 4px; border-top-left-radius: 18px; }
.bubble--tail-end.bubble--theirs { border-bottom-left-radius: 18px; border-top-left-radius: 4px; }
.bubble--tail-end-mine { border-bottom-right-radius: 18px; border-top-right-radius: 4px; }

.msg-time {
  font-size: 0.68rem;
  color: #b89878;
  margin-top: 3px;
  font-family: sans-serif;
  padding: 0 4px;
}

/* Typing indicator */
.typing-bubble {
  display: flex;
  align-items: center;
  gap: 5px;
  background: #fff0e4;
  border: 1px solid #f0dece;
  border-radius: 18px;
  border-bottom-left-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 18px;
}

.dot {
  width: 7px;
  height: 7px;
  background: #c4a48a;
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

/* ── Input Bar ───────────────────────────────────────────────────────────────── */
.input-bar {
  display: flex;
  align-items: flex-end;
  gap: 6px;
  padding: 12px 16px;
  background: #fff8f1;
  border-top: 1.5px solid #f0dece;
  flex-shrink: 0;
}

.attach-btn { color: #b87a5a; flex-shrink: 0; }

.input-wrap { flex: 1; }

.chat-textarea {
  resize: none;
  background: #fdf0e6;
  border: 1px solid #e8cdb0;
  border-radius: 18px;
  padding: 10px 16px;
  font-size: 0.9rem;
  font-family: sans-serif;
  color: #3d2c1e;
  line-height: 1.5;
  min-height: 42px;
  max-height: 120px;
  overflow-y: auto;
  width: 100%;
}
.chat-textarea::placeholder { color: #c4a48a; }
.chat-textarea:focus { outline: none; border-color: #e07840; box-shadow: 0 0 0 2px #f5c9a8; }

.send-btn {
  background: #e07840;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  transition: background 0.15s, transform 0.1s;
}
.send-btn:hover:not(:disabled) { background: #c8612a; transform: scale(1.05); }
.send-btn:disabled { background: #e8cdb0; }

/* ── Empty State ─────────────────────────────────────────────────────────────── */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #b89878;
}
.empty-icon { font-size: 3rem; }
.empty-title { font-size: 1.1rem; font-weight: 700; color: #3d2c1e; }
.empty-sub { font-size: 0.85rem; font-family: sans-serif; }
</style>