<template>
  <div class="flex h-screen bg-background font-sans text-foreground overflow-hidden">
    
    <div class="w-full max-w-md border-r bg-card flex flex-col z-10">
      <div class="p-6">
        <h1 class="text-2xl font-semibold tracking-tight">Conversations</h1>
      </div>
      
      <Separator />

      <ScrollArea class="flex-1">
        <div class="flex flex-col">
          <div 
            v-for="chat in chats" 
            :key="chat.id"
            @click="selectChat(chat.id)"
            :class="[
              'flex items-center gap-4 p-4 cursor-pointer transition-colors duration-200',
              selectedChatId === chat.id 
                ? 'bg-green-200 hover:bg-green-300 dark:bg-green-900/40 dark:hover:bg-green-900/60' 
                : chat.unread
                  ? 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700'
                  : 'hover:bg-accent/50'
            ]"
          >
            <Avatar class="w-12 h-12 border border-border">
              <AvatarImage :src="chat.avatarUrl" :alt="chat.name" />
              <AvatarFallback class="bg-muted text-muted-foreground font-medium">
                {{ chat.initials }}
              </AvatarFallback>
            </Avatar>
            
            <div class="flex-1 min-w-0">
              <h2 :class="['text-base truncate', chat.unread ? 'font-bold' : 'font-medium']">
                {{ chat.name }}
              </h2>
              <p :class="['text-sm truncate', chat.unread ? 'text-foreground font-medium' : 'text-muted-foreground']">
                {{ getLastMessage(chat) }}
              </p>
            </div>
            
            <div class="flex flex-col items-end gap-1">
              <div class="text-xs text-muted-foreground whitespace-nowrap font-medium">
                {{ chat.lastMessageTime }}
              </div>
              <div v-if="chat.unread" class="w-2.5 h-2.5 bg-green-500 rounded-full"></div>
            </div>
          </div>
          <Separator v-for="n in chats.length - 1" :key="'sep-'+n" class="opacity-50" />
        </div>
      </ScrollArea>
    </div>

    <div class="flex-1 flex flex-col bg-background/95">
      
      <div v-if="!activeChat" class="flex-1 flex flex-col items-center justify-center text-muted-foreground">
        <h2 class="text-xl font-semibold text-foreground mb-2">Nothing selected</h2>
        <p>Select a conversation to get started</p>
      </div>

      <div v-else class="flex-1 flex flex-col h-full overflow-hidden">
        
        <div class="flex items-center justify-between p-4 border-b bg-card">
          <div class="flex items-center gap-4">
            <Button variant="ghost" size="icon" class="text-muted-foreground md:hidden">
              <ChevronLeft class="w-5 h-5" />
            </Button>
            <h2 class="text-xl font-medium">{{ activeChat.name }}</h2>
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

        <ScrollArea class="flex-1 p-6">
          <div class="space-y-6 flex flex-col pb-4">
            <div 
              v-for="message in activeChat.messages" 
              :key="message.id"
              :class="['flex w-full', message.sender === 'me' ? 'justify-end' : 'justify-start']"
            >
              <div class="flex gap-3 max-w-[70%]" :class="{'flex-row-reverse': message.sender === 'me'}">
                
                <Avatar v-if="message.sender === 'them'" class="w-10 h-10 border border-border">
                  <AvatarFallback class="bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400">
                    <User class="w-5 h-5" />
                  </AvatarFallback>
                </Avatar>
                
                <div 
                  :class="[
                    'px-5 py-3 rounded-3xl shadow-sm text-sm border',
                    message.sender === 'me' 
                      ? 'bg-green-300 text-gray-900 border-green-375 rounded-br-sm' 
                      : 'bg-green-100 text-gray-900 border-green-175 rounded-bl-sm'
                  ]"
                >
                  {{ message.text }}
                </div>
              </div>
            </div>
            <!-- Invisible element to anchor the scroll to -->
            <div ref="bottomRef" class="h-px w-full"></div>
          </div>
        </ScrollArea>

        <div class="p-4 bg-card border-t">
          <form @submit.prevent="sendMessage" class="flex items-center gap-3 bg-background border rounded-full px-2 py-2 focus-within:ring-2 focus-within:ring-green-300 focus-within:border-green-400 transition-all shadow-sm">
            
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
              <ArrowRight class="w-5 h-5" :class="newMessage.trim() ? 'text-primary-foreground' : 'text-muted-foreground'" />
            </Button>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'

// --- shadcn-vue Components ---
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'

// --- Lucide Icons ---
import { ChevronLeft, MoreVertical, Phone, Plus, ArrowRight, User } from 'lucide-vue-next'

// --- Storage Key ---
const STORAGE_KEY = 'quick-fix-chats-data'

// --- State ---
const selectedChatId = ref<number | null>(null)
const newMessage = ref('')
const bottomRef = ref<HTMLElement | null>(null) // Anchor ref for scrolling

// --- Default Mock Data ---
const defaultChats = [
  {
    id: 1,
    name: 'Joseph D.',
    initials: 'JD',
    avatarUrl: '',
    lastMessageTime: '10 min',
    unread: false,
    messages: [
      { id: 1, sender: 'me', text: 'Lorem Ipsum' },
      { id: 2, sender: 'them', text: 'Lorem Ipsum' },
      { id: 3, sender: 'me', text: '1010100001101001001010100' },
      { id: 4, sender: 'them', text: '48 31 C0 48 89 C7' },
    ]
  },
  {
    id: 2,
    name: 'Sarah Jenkins',
    initials: 'SJ',
    avatarUrl: '',
    lastMessageTime: '2 hrs',
    unread: true, 
    messages: [
      { id: 1, sender: 'them', text: 'Are we still meeting to discuss the database schema?' },
      { id: 2, sender: 'me', text: 'Yes, let\'s sync at 2 PM. I have the Entity Framework models ready.' },
      { id: 3, sender: 'them', text: 'Perfect, see you then.' }
    ]
  },
  {
    id: 3,
    name: 'System Alerts',
    initials: 'SA',
    avatarUrl: '',
    lastMessageTime: '1 day',
    unread: false,
    messages: [
      { id: 1, sender: 'them', text: 'Docker container "p2p_node_42" has restarted unexpectedly.' },
      { id: 2, sender: 'me', text: 'Acknowledge. Checking the logs now.' }
    ]
  }
]


const loadChats = () => {
  const savedData = localStorage.getItem(STORAGE_KEY)
  if (savedData) {
    try {
      return JSON.parse(savedData)
    } catch (e) {
      console.error('Failed to parse chat data from local storage', e)
      return defaultChats
    }
  }
  return defaultChats
}

const chats = ref(loadChats())


const activeChat = computed(() => {
  return chats.value.find((c: any) => c.id === selectedChatId.value) || null
})


const onStorageChange = (event: StorageEvent) => {
  if (event.key === STORAGE_KEY && event.newValue) {
    const newChats = JSON.parse(event.newValue)
    
    newChats.forEach((newChat: any) => {
      const oldChat = chats.value.find((c: any) => c.id === newChat.id)
      if (oldChat && newChat.messages.length > oldChat.messages.length) {
         if (selectedChatId.value !== newChat.id) {
            newChat.unread = true 
         }
      }
    })
    
    chats.value = newChats
  }
}

onMounted(() => {
  window.addEventListener('storage', onStorageChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorageChange)
})

watch(chats, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

watch(
  () => activeChat.value?.messages?.length,
  () => {
    scrollToBottom()
  }
)

const selectChat = (id: number) => {
  selectedChatId.value = id
  
  const chat = chats.value.find((c: any) => c.id === id)
  if (chat && chat.unread) {
    chat.unread = false
  }

  scrollToBottom()
}

const getLastMessage = (chat: any) => {
  if (!chat.messages || chat.messages.length === 0) return 'No messages yet'
  return chat.messages[chat.messages.length - 1].text
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !activeChat.value) return

  const newMsg = {
    id: Date.now(),
    sender: 'me',
    text: newMessage.value.trim()
  }

  activeChat.value.messages.push(newMsg)
  activeChat.value.lastMessageTime = 'Just now'
  newMessage.value = ''

  scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  setTimeout(() => {
    if (bottomRef.value) {
      let scrollContainer = bottomRef.value.closest('[data-radix-scroll-area-viewport]')
      
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
        scrollContainer.scrollTo({
          top: scrollContainer.scrollHeight,
          behavior: 'smooth'
        })
      } else {
        bottomRef.value.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
      }
    }
  }, 50)
}
</script>