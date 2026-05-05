<template>
  <div class="flex h-screen bg-background font-sans text-foreground overflow-hidden">

    <!-- ─── Left sidebar: Conversation list ──────────────────────────────── -->
    <div class="w-full max-w-md border-r bg-card flex flex-col z-10">
      <div class="p-6">
        <h1 class="text-2xl font-semibold tracking-tight">Conversations</h1>
      </div>

      <Separator />

      <ScrollArea class="flex-1">
        <div class="flex flex-col">
          <template v-for="(chat, idx) in chats" :key="chat.id">
            <div
              @click="selectChat(chat.id)"
              :class="[
                'flex items-center gap-4 p-4 cursor-pointer transition-colors duration-200',
                selectedChatId === chat.id
                  ? 'bg-green-200 hover:bg-green-300 dark:bg-green-900/40 dark:hover:bg-green-900/60'
                  : chat.unread
                    ? 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700'
                    : 'hover:bg-accent/50',
              ]"
            >
              <Avatar class="w-12 h-12 border border-border shrink-0">
                <AvatarImage :src="chat.avatarUrl" :alt="chat.name" />
                <AvatarFallback class="bg-muted text-muted-foreground font-medium">
                  {{ chat.initials }}
                </AvatarFallback>
              </Avatar>

              <div class="flex-1 min-w-0">
                <h2 :class="['text-base truncate', chat.unread ? 'font-bold' : 'font-medium']">
                  {{ chat.name }}
                </h2>
                <p
                  :class="[
                    'text-sm truncate',
                    chat.unread ? 'text-foreground font-medium' : 'text-muted-foreground',
                  ]"
                >
                  {{ getLastMessage(chat) }}
                </p>
              </div>

              <div class="flex flex-col items-end gap-1 shrink-0">
                <div class="text-xs text-muted-foreground whitespace-nowrap font-medium">
                  {{ chat.lastMessageTime }}
                </div>
                <div v-if="chat.unread" class="w-2.5 h-2.5 bg-green-500 rounded-full"></div>
              </div>
            </div>
            <Separator v-if="idx < chats.length - 1" class="opacity-50" />
          </template>
        </div>
      </ScrollArea>
    </div>

    <!-- ─── Right: Active chat area ──────────────────────────────────────── -->
    <div class="flex-1 flex flex-col bg-background/95">

      <!-- Empty state -->
      <div
        v-if="!activeChat"
        class="flex-1 flex flex-col items-center justify-center text-muted-foreground"
      >
        <h2 class="text-xl font-semibold text-foreground mb-2">Nothing selected</h2>
        <p>Select a conversation to get started</p>
      </div>

      <div v-else class="flex-1 flex flex-col h-full overflow-hidden">

        <!-- ── Chat header ──────────────────────────────────────────────── -->
        <div class="flex items-center justify-between p-4 border-b bg-card">
          <div class="flex items-center gap-3">
            <Button variant="ghost" size="icon" class="text-muted-foreground md:hidden">
              <ChevronLeft class="w-5 h-5" />
            </Button>

            <!-- Clickable avatar → opens avatar popup -->
            <button
              class="rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              @click="avatarPopupOpen = true"
              :title="`View ${activeChat.name}'s photo`"
            >
              <Avatar class="w-10 h-10 border border-border hover:opacity-80 transition-opacity">
                <AvatarImage :src="activeChat.avatarUrl" :alt="activeChat.name" />
                <AvatarFallback class="bg-muted text-muted-foreground font-medium text-sm">
                  {{ activeChat.initials }}
                </AvatarFallback>
              </Avatar>
            </button>

            <h2 class="text-xl font-medium">{{ activeChat.name }}</h2>

            <!-- "View Provider" button — only shown when a provider snapshot exists -->
            <Button
              v-if="activeChat.providerId && activeProviderSnapshot"
              variant="outline"
              size="sm"
              class="ml-1 text-xs rounded-full border-green-400 text-green-700 hover:bg-green-50 dark:text-green-400 dark:border-green-700 dark:hover:bg-green-950"
              @click="viewProviderOpen = true"
            >
              View Provider
            </Button>
          </div>

          <div class="flex items-center gap-1">
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

        <!-- ── Message list ─────────────────────────────────────────────── -->
        <ScrollArea class="flex-1 p-6">
          <div class="space-y-6 flex flex-col pb-4">
            <div
              v-for="message in activeChat.messages"
              :key="message.id"
              :class="['flex w-full', message.sender === 'me' ? 'justify-end' : 'justify-start']"
            >
              <div
                class="flex gap-3 max-w-[70%]"
                :class="{ 'flex-row-reverse': message.sender === 'me' }"
              >
                <!-- Provider avatar beside their messages — clickable -->
                <button
                  v-if="message.sender === 'them'"
                  class="self-end rounded-full shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  @click="avatarPopupOpen = true"
                  :title="`View ${activeChat.name}'s photo`"
                >
                  <Avatar class="w-10 h-10 border border-border hover:opacity-80 transition-opacity">
                    <AvatarImage :src="activeChat.avatarUrl" :alt="activeChat.name" />
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
                    message.sender === 'me'
                      ? 'bg-green-300 text-gray-900 border-green-375 rounded-br-sm'
                      : 'bg-green-100 text-gray-900 border-green-175 rounded-bl-sm',
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

        <!-- ── Message input ────────────────────────────────────────────── -->
        <div class="p-4 bg-card border-t">
          <form
            @submit.prevent="sendMessage"
            class="flex items-center gap-3 bg-background border rounded-full px-2 py-2 focus-within:ring-2 focus-within:ring-green-300 focus-within:border-green-400 transition-all shadow-sm"
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger as-child>
                  <Button type="button" variant="ghost" size="icon" class="rounded-full shrink-0">
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
                :class="newMessage.trim() ? 'text-primary-foreground' : 'text-muted-foreground'"
              />
            </Button>
          </form>
        </div>

      </div>
    </div>
  </div>

  <!-- ─── Avatar Popup Dialog ───────────────────────────────────────────────── -->
  <Dialog v-model:open="avatarPopupOpen">
    <DialogContent class="max-w-xs flex flex-col items-center gap-5 py-10 px-8">
      <DialogHeader class="sr-only">
        <DialogTitle>Profile Picture</DialogTitle>
        <DialogDescription>
          Profile picture of {{ activeChat?.name }}
        </DialogDescription>
      </DialogHeader>

      <Avatar class="w-44 h-44 border-4 border-border shadow-xl">
        <AvatarImage :src="activeChat?.avatarUrl" :alt="activeChat?.name" />
        <AvatarFallback class="text-5xl font-semibold bg-muted text-muted-foreground">
          {{ activeChat?.initials }}
        </AvatarFallback>
      </Avatar>

      <p class="text-lg font-semibold text-center">{{ activeChat?.name }}</p>
    </DialogContent>
  </Dialog>

  <!-- ─── View Provider Dialog ──────────────────────────────────────────────── -->
  <Dialog v-model:open="viewProviderOpen">
    <DialogContent class="m-0 h-full max-h-[95vh] max-w-150 gap-0 p-0">
      <DialogHeader class="sr-only">
        <DialogTitle>Provider Profile</DialogTitle>
        <DialogDescription>
          Full profile for {{ activeChat?.name }}
        </DialogDescription>
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

  <!-- ─── Scheduler Dialog (opened via Provider's "Book Now" button) ───────── -->
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

// ─── shadcn-vue UI components ─────────────────────────────────────────────────
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

// ─── Lucide icons ─────────────────────────────────────────────────────────────
import { ChevronLeft, MoreVertical, Phone, Plus, ArrowRight, User } from 'lucide-vue-next'

// ─── Internal components ──────────────────────────────────────────────────────
import Provider from '@/components/Provider.vue'
import Scheduler from '@/components/Scheduler.vue'

// ─── Pinia store ──────────────────────────────────────────────────────────────
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/store/chatStore'

const chatStore = useChatStore()
const { chats } = storeToRefs(chatStore)

// ─── Local UI state ───────────────────────────────────────────────────────────
const selectedChatId = ref<number | null>(null)
const newMessage = ref('')
const bottomRef = ref<HTMLElement | null>(null)

// Dialog visibility flags
const avatarPopupOpen = ref(false)
const viewProviderOpen = ref(false)
const schedulerOpen = ref(false)
const schedulerProvider = ref<any>(null)

// ─── Derived state ────────────────────────────────────────────────────────────
const activeChat = computed<any | null>(() => {
  return chats.value.find((c: any) => c.id === selectedChatId.value) ?? null
})

// Provider snapshot for the active chat (null if this is a non-provider chat)
const activeProviderSnapshot = computed<any | null>(() => {
  if (!activeChat.value?.providerId) return null
  return chatStore.getProviderSnapshot(activeChat.value.providerId)
})

// ─── Cross-tab localStorage sync ─────────────────────────────────────────────
const onStorageChange = (event: StorageEvent) => {
  if (event.key !== 'quick-fix-chats-data' || !event.newValue) return
  try {
    const incoming: any[] = JSON.parse(event.newValue)
    // Mark newly-arrived messages as unread when the chat isn't active
    incoming.forEach((incomingChat) => {
      const local = chats.value.find((c: any) => c.id === incomingChat.id)
      if (local && incomingChat.messages.length > local.messages.length) {
        if (selectedChatId.value !== incomingChat.id) {
          incomingChat.unread = true
        }
      }
    })
    chats.value.splice(0, chats.value.length, ...incoming)
  } catch (e) {
    console.error('[ChatMessages] Failed to sync chats from storage event', e)
  }
}

onMounted(() => {
  window.addEventListener('storage', onStorageChange)

  // Auto-select the chat that was pending when navigating from ProviderList
  const pendingId = chatStore.consumePendingChat()
  if (pendingId) {
    selectedChatId.value = pendingId
    nextTick(() => scrollToBottom())
  }
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorageChange)
})

// Scroll to bottom whenever the active chat gains a new message
watch(
  () => activeChat.value?.messages?.length,
  () => scrollToBottom()
)

// ─── Methods ──────────────────────────────────────────────────────────────────
function selectChat(id: number) {
  selectedChatId.value = id
  const chat = chats.value.find((c: any) => c.id === id)
  if (chat?.unread) chat.unread = false
  scrollToBottom()
}

function getLastMessage(chat: any): string {
  if (!chat.messages?.length) return 'No messages yet'
  return chat.messages[chat.messages.length - 1].text
}

async function sendMessage() {
  if (!newMessage.value.trim() || !activeChat.value) return
  activeChat.value.messages.push({
    id: Date.now(),
    sender: 'me',
    text: newMessage.value.trim(),
  })
  activeChat.value.lastMessageTime = 'Just now'
  newMessage.value = ''
  scrollToBottom()
}

/**
 * Called when the Provider component emits @select (i.e., user clicks "Book Now").
 * Closes the provider profile dialog and opens the scheduler.
 */
function handleScheduleFromProvider(provider: any) {
  viewProviderOpen.value = false
  schedulerProvider.value = provider ?? activeProviderSnapshot.value
  schedulerOpen.value = true
}

async function scrollToBottom() {
  await nextTick()
  setTimeout(() => {
    if (!bottomRef.value) return

    // Try Radix scroll-area viewport first, then walk up the DOM
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