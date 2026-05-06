<template>
  <div class="flex h-screen bg-background font-sans text-foreground overflow-hidden">

    <!-- ─── Left sidebar: Conversation list ──────────────────────────────────── -->
    <div class="w-full max-w-md border-r bg-card flex flex-col z-10">
      <div class="p-6">
        <h1 class="text-2xl font-semibold tracking-tight">Conversations</h1>
      </div>

      <Separator />

      <!-- Not logged in -->
      <div
        v-if="!currentUser"
        class="flex-1 flex flex-col items-center justify-center gap-2 text-muted-foreground p-6 text-center"
      >
        <p class="font-medium text-foreground">You are not logged in</p>
        <p class="text-sm">Please log in to view your messages.</p>
      </div>

      <!-- No chats yet -->
      <div
        v-else-if="visibleChats.length === 0"
        class="flex-1 flex flex-col items-center justify-center gap-2 text-muted-foreground p-6 text-center"
      >
        <p class="text-sm">No conversations yet.</p>
        <p class="text-sm">Start one by messaging a provider or responding to a job.</p>
      </div>

      <ScrollArea v-else class="flex-1">
        <div class="flex flex-col">
          <template v-for="(chat, idx) in visibleChats" :key="chat.id">
            <div
              @click="selectChat(chat.id)"
              :class="[
                'flex items-center gap-4 p-4 cursor-pointer transition-colors duration-200',
                selectedChatId === chat.id
                  ? 'bg-green-200 hover:bg-green-300 dark:bg-green-900/40 dark:hover:bg-green-900/60'
                  : isChatUnread(chat)
                    ? 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700'
                    : 'hover:bg-accent/50',
              ]"
            >
              <Avatar class="w-12 h-12 border border-border shrink-0">
                <AvatarImage
                  :src="getOtherParticipant(chat).avatarUrl"
                  :alt="getOtherParticipant(chat).name"
                />
                <AvatarFallback class="bg-muted text-muted-foreground font-medium">
                  {{ getOtherParticipant(chat).initials }}
                </AvatarFallback>
              </Avatar>

              <div class="flex-1 min-w-0">
                <h2
                  :class="[
                    'text-base truncate',
                    isChatUnread(chat) ? 'font-bold' : 'font-medium',
                  ]"
                >
                  {{ getOtherParticipant(chat).name }}
                </h2>
                <p
                  :class="[
                    'text-sm truncate',
                    isChatUnread(chat)
                      ? 'text-foreground font-medium'
                      : 'text-muted-foreground',
                  ]"
                >
                  {{ getLastMessage(chat) }}
                </p>
              </div>

              <div class="flex flex-col items-end gap-1 shrink-0">
                <div class="text-xs text-muted-foreground whitespace-nowrap font-medium">
                  {{ chat.lastMessageTime }}
                </div>
                <div
                  v-if="isChatUnread(chat)"
                  class="w-2.5 h-2.5 bg-green-500 rounded-full"
                ></div>
              </div>
            </div>
            <Separator v-if="idx < visibleChats.length - 1" class="opacity-50" />
          </template>
        </div>
      </ScrollArea>
    </div>

    <!-- ─── Right: Active chat area ───────────────────────────────────────────── -->
    <div class="flex-1 flex flex-col bg-background/95">

      <!-- Empty / no selection -->
      <div
        v-if="!activeChat"
        class="flex-1 flex flex-col items-center justify-center text-muted-foreground"
      >
        <h2 class="text-xl font-semibold text-foreground mb-2">Nothing selected</h2>
        <p>Select a conversation to get started</p>
      </div>

      <div v-else class="flex-1 flex flex-col h-full overflow-hidden">

        <!-- ── Chat header ────────────────────────────────────────────────────── -->
        <div class="flex items-center justify-between p-4 border-b bg-card">
          <div class="flex items-center gap-3 min-w-0">
            <Button variant="ghost" size="icon" class="text-muted-foreground md:hidden shrink-0">
              <ChevronLeft class="w-5 h-5" />
            </Button>

            <!-- Clickable avatar → avatar popup -->
            <button
              class="rounded-full shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              @click="avatarPopupOpen = true"
              :title="`View ${otherParticipant?.name}'s photo`"
            >
              <Avatar
                class="w-10 h-10 border border-border hover:opacity-80 transition-opacity"
              >
                <AvatarImage
                  :src="otherParticipant?.avatarUrl"
                  :alt="otherParticipant?.name"
                />
                <AvatarFallback
                  class="bg-muted text-muted-foreground font-medium text-sm"
                >
                  {{ otherParticipant?.initials }}
                </AvatarFallback>
              </Avatar>
            </button>

            <h2 class="text-xl font-medium truncate">{{ otherParticipant?.name }}</h2>

            <!-- "View Provider" — shown only to customers when a provider snapshot is available -->
            <Button
              v-if="activeChat.linkedProviderId && activeProviderSnapshot && userStore.isCustomer"
              variant="outline"
              size="sm"
              class="ml-1 shrink-0 text-xs rounded-full border-green-400 text-green-700 hover:bg-green-50 dark:text-green-400 dark:border-green-700 dark:hover:bg-green-950"
              @click="viewProviderOpen = true"
            >
              View Provider
            </Button>

            <!-- "View Job Listing" — shown only to providers when a job snapshot is available -->
            <Button
              v-if="activeChat.linkedJobId && activeJobSnapshot && userStore.isProvider"
              variant="outline"
              size="sm"
              class="ml-1 shrink-0 text-xs rounded-full border-blue-400 text-blue-700 hover:bg-blue-50 dark:text-blue-400 dark:border-blue-700 dark:hover:bg-blue-950"
              @click="viewJobOpen = true"
            >
              View Job Listing
            </Button>
          </div>

          <div class="flex items-center gap-1 shrink-0">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger as-child>
                  <Button variant="ghost" size="icon" class="rounded-full">
                    <Phone class="w-5 h-5 text-muted-foreground" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Call</TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger as-child>
                  <Button variant="ghost" size="icon" class="rounded-full">
                    <MoreVertical class="w-5 h-5 text-muted-foreground" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>More Options</TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </div>

        <!-- ── Message list ───────────────────────────────────────────────────── -->
        <ScrollArea class="flex-1 p-6">
          <div class="space-y-6 flex flex-col pb-4">
            <div
              v-for="message in activeChat.messages"
              :key="message.id"
              :class="[
                'flex w-full',
                isMe(message) ? 'justify-end' : 'justify-start',
              ]"
            >
              <div
                class="flex gap-3 max-w-[70%]"
                :class="{ 'flex-row-reverse': isMe(message) }"
              >
                <!-- Other person's avatar beside their messages — clickable -->
                <button
                  v-if="!isMe(message)"
                  class="self-end rounded-full shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  @click="avatarPopupOpen = true"
                  :title="`View ${otherParticipant?.name}'s photo`"
                >
                  <Avatar
                    class="w-10 h-10 border border-border hover:opacity-80 transition-opacity"
                  >
                    <AvatarImage
                      :src="otherParticipant?.avatarUrl"
                      :alt="otherParticipant?.name"
                    />
                    <AvatarFallback
                      class="bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400"
                    >
                      <User class="w-5 h-5" />
                    </AvatarFallback>
                  </Avatar>
                </button>

                <div
                  :class="[
                    'px-5 py-3 rounded-3xl shadow-sm text-sm border',
                    isMe(message)
                      ? 'bg-green-300 text-gray-900 border-green-400 rounded-br-sm'
                      : 'bg-green-100 text-gray-900 border-green-200 rounded-bl-sm',
                  ]"
                >
                  {{ message.text }}
                </div>
              </div>
            </div>

            <!-- Scroll anchor -->
            <div ref="bottomRef" class="h-px w-full"></div>
          </div>
        </ScrollArea>

        <!-- ── Message input ──────────────────────────────────────────────────── -->
        <div class="p-4 bg-card border-t">
          <form
            @submit.prevent="sendMessage"
            class="flex items-center gap-3 bg-background border rounded-full px-2 py-2 focus-within:ring-2 focus-within:ring-green-300 focus-within:border-green-400 transition-all shadow-sm"
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger as-child>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    class="rounded-full shrink-0"
                  >
                    <Plus class="w-5 h-5 text-muted-foreground" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Add Attachment</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <Input
              v-model="newMessage"
              type="text"
              placeholder="Type a message..."
              class="flex-1 bg-transparent border-none focus-visible:ring-0 focus-visible:ring-offset-0 px-2 py-1 shadow-none h-auto text-base"
            />

            <Button
              type="submit"
              size="icon"
              :disabled="!newMessage.trim()"
              class="rounded-full shrink-0 transition-all"
              :variant="newMessage.trim() ? 'default' : 'ghost'"
            >
              <ArrowRight
                class="w-5 h-5"
                :class="
                  newMessage.trim() ? 'text-primary-foreground' : 'text-muted-foreground'
                "
              />
            </Button>
          </form>
        </div>

      </div>
    </div>
  </div>

  <!-- ─── Avatar Popup Dialog ────────────────────────────────────────────────── -->
  <Dialog v-model:open="avatarPopupOpen">
    <DialogContent class="max-w-xs flex flex-col items-center gap-5 py-10 px-8">
      <DialogHeader class="sr-only">
        <DialogTitle>Profile Picture</DialogTitle>
        <DialogDescription>Profile picture of {{ otherParticipant?.name }}</DialogDescription>
      </DialogHeader>

      <Avatar class="w-44 h-44 border-4 border-border shadow-xl">
        <AvatarImage :src="otherParticipant?.avatarUrl" :alt="otherParticipant?.name" />
        <AvatarFallback class="text-5xl font-semibold bg-muted text-muted-foreground">
          {{ otherParticipant?.initials }}
        </AvatarFallback>
      </Avatar>

      <p class="text-lg font-semibold text-center">{{ otherParticipant?.name }}</p>
    </DialogContent>
  </Dialog>

  <!-- ─── View Provider Dialog ───────────────────────────────────────────────── -->
  <Dialog v-model:open="viewProviderOpen">
    <DialogContent class="m-0 h-full max-h-[95vh] max-w-150 gap-0 p-0">
      <DialogHeader class="sr-only">
        <DialogTitle>Provider Profile</DialogTitle>
        <DialogDescription>Full profile for {{ otherParticipant?.name }}</DialogDescription>
      </DialogHeader>
      <ScrollArea class="h-full max-h-full">
        <div class="p-4">
          <Provider
            v-if="activeProviderSnapshot"
            :provider="activeProviderSnapshot"
            @select="handleScheduleFromProvider"
          />
        </div>
      </ScrollArea>
    </DialogContent>
  </Dialog>

  <!-- ─── View Job Listing Dialog ────────────────────────────────────────────── -->
  <Dialog v-model:open="viewJobOpen">
    <DialogContent class="max-w-2xl p-0 bg-white border-0 shadow-2xl overflow-hidden rounded-xl">
      <DialogHeader class="sr-only">
        <DialogTitle>Job Listing</DialogTitle>
        <DialogDescription>Details for the job listing</DialogDescription>
      </DialogHeader>

      <div v-if="activeJobSnapshot" class="p-8 max-h-[85vh] overflow-y-auto">

        <!-- Title row -->
        <div class="flex justify-between items-start mb-6 gap-4">
          <h2 class="text-2xl md:text-3xl font-extrabold text-slate-900 leading-tight">
            {{ activeJobSnapshot.title || 'Job Listing' }}
          </h2>
          <!-- Job type badge -->
          <span
            class="shrink-0 text-xs font-semibold uppercase tracking-wide px-3 py-1 rounded-full bg-green-100 text-green-700"
          >
            {{ activeJobSnapshot.request_type || 'quote' }}
          </span>
        </div>

        <hr class="border-slate-100 mb-8" />

        <!-- Quick Details grid -->
        <div class="mb-8">
          <h3 class="font-bold text-slate-900 text-lg mb-6">Quick Details</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-4">

            <!-- Customer name -->
            <div class="flex items-center text-slate-600 font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 shrink-0"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              {{ activeJobSnapshot.customer?.name || activeJobSnapshot.user_name || 'Unknown customer' }}
            </div>

            <!-- Language -->
            <div class="flex items-center text-slate-600 font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 shrink-0"><circle cx="12" cy="12" r="10"></circle><line x1="2" x2="22" y1="12" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
              {{ activeJobSnapshot.languages || activeJobSnapshot.language || 'English' }}
            </div>

            <!-- Location -->
            <div class="flex items-center text-slate-600 font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 shrink-0"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              {{ activeJobSnapshot.city }}{{ activeJobSnapshot.state ? ', ' + activeJobSnapshot.state : ', California' }}
            </div>

            <!-- Urgency -->
            <div class="flex items-center text-slate-600 font-medium capitalize">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 shrink-0"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              {{ activeJobSnapshot.urgency || 'Not specified' }}
            </div>

            <!-- Date -->
            <div class="flex items-center text-slate-600 font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 shrink-0"><path d="M8 2v4"></path><path d="M16 2v4"></path><rect width="18" height="18" x="3" y="4" rx="2"></rect><path d="M3 10h18"></path></svg>
              {{ formatDate(activeJobSnapshot.deadline || activeJobSnapshot.date) }}
            </div>

            <!-- Service / category -->
            <div class="flex items-center text-slate-600 font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 shrink-0"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
              <!-- services is an array in fallback shape; service is a string in raw shape -->
              <span v-if="Array.isArray(activeJobSnapshot.services)">
                {{ activeJobSnapshot.services.map((s) => s.name || s).join(', ') }}
              </span>
              <span v-else>{{ activeJobSnapshot.service || 'General' }}</span>
            </div>

          </div>

          <!-- Budget line -->
          <div class="mt-6 pt-2 flex items-center gap-3 flex-wrap">
            <span class="text-lg font-bold text-slate-900">
              {{ activeJobSnapshot.budget != null ? `$${activeJobSnapshot.budget}` : activeJobSnapshot.price != null ? `$${activeJobSnapshot.price}` : '$0' }}
            </span>
            <span class="text-base text-slate-500 font-medium">/ hr</span>
          </div>
        </div>

        <hr class="border-slate-100 mb-8" />

        <!-- Description -->
        <div>
          <h3 class="font-bold text-slate-900 text-lg mb-4">About the Job</h3>
          <p class="text-slate-600 leading-relaxed whitespace-pre-wrap">
            {{ activeJobSnapshot.description || 'No description provided.' }}
          </p>
        </div>

      </div>
    </DialogContent>
  </Dialog>

  <!-- ─── Scheduler Dialog (opened via Provider's "Book Now") ───────────────── -->
  <Dialog v-model:open="schedulerOpen">
    <DialogContent class="max-w-md border-0 p-0">
      <DialogHeader class="sr-only">
        <DialogTitle>Schedule</DialogTitle>
        <DialogDescription>Select a date and time</DialogDescription>
      </DialogHeader>
      <Scheduler v-if="schedulerProvider" :provider="schedulerProvider" />
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'

// ─── shadcn-vue UI ────────────────────────────────────────────────────────────
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import {
  Tooltip, TooltipContent, TooltipProvider, TooltipTrigger,
} from '@/components/ui/tooltip'
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
} from '@/components/ui/dialog'

// ─── Lucide icons ─────────────────────────────────────────────────────────────
import { ChevronLeft, MoreVertical, Phone, Plus, ArrowRight, User } from 'lucide-vue-next'

// ─── Internal components ──────────────────────────────────────────────────────
import Provider from '@/components/Provider.vue'
import Scheduler from '@/components/Scheduler.vue'

// ─── Stores ───────────────────────────────────────────────────────────────────
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/store/chatStore'
import { useUserStore } from '@/store/userStore'

const chatStore = useChatStore()
const userStore = useUserStore()
const { chats } = storeToRefs(chatStore)

// ─── Current user (reactive) ──────────────────────────────────────────────────
const currentUser = computed(() => userStore.currentUser)

// ─── Local UI state ───────────────────────────────────────────────────────────
const selectedChatId   = ref<number | null>(null)
const newMessage       = ref('')
const bottomRef        = ref<HTMLElement | null>(null)

const avatarPopupOpen  = ref(false)
const viewProviderOpen = ref(false)
const viewJobOpen      = ref(false)
const schedulerOpen    = ref(false)
const schedulerProvider = ref<any>(null)

// ─── Derived: chats scoped to the logged-in user ──────────────────────────────
const visibleChats = computed<any[]>(() => {
  const uid = currentUser.value?.id
  if (!uid) return []
  return chatStore.getChatsForUser(uid)
})

// ─── Derived: the active chat object ──────────────────────────────────────────
const activeChat = computed<any | null>(() => {
  return visibleChats.value.find((c: any) => c.id === selectedChatId.value) ?? null
})

// ─── Derived: the OTHER participant's info for the active chat ─────────────────
// This is what we display in the header, avatar popup, and beside messages.
const otherParticipant = computed<any | null>(() => {
  if (!activeChat.value?.participants) return null
  const uid = currentUser.value?.id
  const others = Object.values(activeChat.value.participants as Record<string, any>).filter(
    (p: any) => p.userId !== uid
  )
  return others[0] ?? null
})

// ─── Derived: snapshots for the active chat ───────────────────────────────────
const activeProviderSnapshot = computed<any | null>(() => {
  if (!activeChat.value?.linkedProviderId) return null
  return chatStore.getProviderSnapshot(activeChat.value.linkedProviderId)
})

const activeJobSnapshot = computed<any | null>(() => {
  if (!activeChat.value?.linkedJobId) return null
  return chatStore.getJobSnapshot(activeChat.value.linkedJobId)
})

// ─── Helper: is this message sent by the current user? ────────────────────────
// Supports both the new { senderId } format and the legacy { sender: 'me'/'them' } format.
function isMe(message: any): boolean {
  if (message.senderId !== undefined) {
    return message.senderId === currentUser.value?.id
  }
  // Legacy seed data fallback
  return message.sender === 'me'
}

// ─── Helper: get the other participant for a sidebar chat row ─────────────────
function getOtherParticipant(chat: any): { name: string; initials: string; avatarUrl: string } {
  const uid = currentUser.value?.id
  if (chat.participants && uid) {
    const others = Object.values(chat.participants as Record<string, any>).filter(
      (p: any) => p.userId !== uid
    )
    if (others.length > 0) return others[0] as any
  }
  // Legacy fallback for chats without a participants map
  return { name: chat.name ?? '?', initials: chat.initials ?? '?', avatarUrl: chat.avatarUrl ?? '' }
}

// ─── Helper: is this chat unread for the current user? ────────────────────────
function isChatUnread(chat: any): boolean {
  const uid = currentUser.value?.id
  if (uid && Array.isArray(chat.unreadFor)) return chat.unreadFor.includes(uid)
  // Legacy boolean fallback
  return chat.unread ?? false
}

// ─── Helper: format a date string for display ─────────────────────────────────
function formatDate(dateStr: string | undefined): string {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

// ─── Cross-tab localStorage sync ─────────────────────────────────────────────
// The storage event fires in OTHER tabs when this tab writes. We update the
// store's chats ref so the sidebar reflects new messages instantly.
const onStorageChange = (event: StorageEvent) => {
  if (event.key !== 'quick-fix-chats-v2' || !event.newValue) return
  try {
    const incoming: any[] = JSON.parse(event.newValue)
    const uid = currentUser.value?.id

    // Mark as unread for current user if new messages arrived in a non-active chat
    if (uid) {
      incoming.forEach((incomingChat: any) => {
        const local = chats.value.find((c: any) => c.id === incomingChat.id)
        if (local && incomingChat.messages.length > local.messages.length) {
          if (selectedChatId.value !== incomingChat.id) {
            if (!Array.isArray(incomingChat.unreadFor)) incomingChat.unreadFor = []
            if (!incomingChat.unreadFor.includes(uid)) {
              incomingChat.unreadFor.push(uid)
            }
          }
        }
      })
    }

    // Replace store chats; the watch in chatStore will re-persist
    chats.value = incoming
  } catch (e) {
    console.error('[ChatMessages] Failed to sync from storage event', e)
  }
}

onMounted(() => {
  window.addEventListener('storage', onStorageChange)

  // Auto-select the chat that was pending when navigating from another page
  const pendingId = chatStore.consumePendingChat()
  if (pendingId) {
    selectedChatId.value = pendingId
    nextTick(() => scrollToBottom())
  }
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorageChange)
})

// Scroll to bottom whenever the active chat's message count increases
watch(
  () => activeChat.value?.messages?.length,
  () => scrollToBottom()
)

// ─── Methods ──────────────────────────────────────────────────────────────────
function selectChat(id: number) {
  selectedChatId.value = id

  const chat = chats.value.find((c: any) => c.id === id)
  if (!chat) return

  // Clear the unread indicator for the current user
  const uid = currentUser.value?.id
  if (uid && Array.isArray(chat.unreadFor)) {
    const idx = chat.unreadFor.indexOf(uid)
    if (idx > -1) chat.unreadFor.splice(idx, 1)
  } else if (chat.unread) {
    // Legacy boolean cleanup
    chat.unread = false
  }

  scrollToBottom()
}

function getLastMessage(chat: any): string {
  if (!chat.messages?.length) return 'No messages yet'
  return chat.messages[chat.messages.length - 1].text
}

async function sendMessage() {
  if (!newMessage.value.trim() || !activeChat.value || !currentUser.value) return

  activeChat.value.messages.push({
    id: Date.now(),
    senderId: currentUser.value.id,   // new format — used by isMe()
    text: newMessage.value.trim(),
  })
  activeChat.value.lastMessageTime = 'Just now'

  // Mark the OTHER participant as having an unread message
  const uid = currentUser.value.id
  const otherIds = Object.keys(activeChat.value.participants || {}).filter(
    (k: string) => k !== uid
  )
  if (!Array.isArray(activeChat.value.unreadFor)) activeChat.value.unreadFor = []
  otherIds.forEach((otherId: string) => {
    if (!activeChat.value.unreadFor.includes(otherId)) {
      activeChat.value.unreadFor.push(otherId)
    }
  })

  newMessage.value = ''
  scrollToBottom()
}

/** Called when the Provider component emits @select ("Book Now"). */
function handleScheduleFromProvider(provider: any) {
  viewProviderOpen.value = false
  schedulerProvider.value = provider ?? activeProviderSnapshot.value
  schedulerOpen.value = true
}

async function scrollToBottom() {
  await nextTick()
  setTimeout(() => {
    if (!bottomRef.value) return

    let scrollContainer: Element | null = bottomRef.value.closest(
      '[data-radix-scroll-area-viewport]'
    )

    if (!scrollContainer) {
      let parent = bottomRef.value.parentElement
      while (parent) {
        const style = window.getComputedStyle(parent)
        if (style.overflowY === 'auto' || style.overflowY === 'scroll') {
          scrollContainer = parent
          break
        }
        parent = parent.parentElement
      }
    }

    if (scrollContainer) {
      scrollContainer.scrollTo({ top: scrollContainer.scrollHeight, behavior: 'smooth' })
    } else {
      bottomRef.value.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }, 50)
}
</script>