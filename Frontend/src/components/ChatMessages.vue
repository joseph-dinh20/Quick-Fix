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
                ? 'bg-orange-200 hover:bg-orange-300 dark:bg-orange-900/40 dark:hover:bg-orange-900/60' 
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
              <h2 class="text-base font-medium truncate">{{ chat.name }}</h2>
              <p class="text-sm text-muted-foreground truncate">{{ getLastMessage(chat) }}</p>
            </div>
            
            <div class="text-xs text-muted-foreground whitespace-nowrap font-medium">
              {{ chat.lastMessageTime }}
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

        <ScrollArea class="flex-1 p-6" ref="messagesScrollArea">
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
                      ? 'bg-[#fb923c] text-gray-900 border-[#ea580c] rounded-br-sm' 
                      : 'bg-[#fed7aa] text-gray-900 border-[#fdba74] rounded-bl-sm'
                  ]"
                >
                  {{ message.text }}
                </div>
              </div>
            </div>
          </div>
        </ScrollArea>

        <div class="p-4 bg-card border-t">
          <form @submit.prevent="sendMessage" class="flex items-center gap-3 bg-background border rounded-full px-2 py-2 focus-within:ring-2 focus-within:ring-orange-300 focus-within:border-orange-400 transition-all shadow-sm">
            
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
const messagesScrollArea = ref<InstanceType<typeof ScrollArea> | null>(null)

// --- Default Mock Data ---
const defaultChats = [
  {
    id: 1,
    name: 'Joseph D.',
    initials: 'JD',
    avatarUrl: '',
    lastMessageTime: '10 min',
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
    messages: [
      { id: 1, sender: 'them', text: 'Docker container "p2p_node_42" has restarted unexpectedly.' },
      { id: 2, sender: 'me', text: 'Acknowledge. Checking the logs now.' }
    ]
  }
]

// --- Initialization Logic ---
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

// Reactive chats array loaded synchronously
const chats = ref(loadChats())

// --- Persistence Logic ---
// Watch for deep changes in the chats array and save to local storage automatically
const onStorageChange = (event: StorageEvent) => {
  if (event.key === STORAGE_KEY && event.newValue) {
    chats.value = JSON.parse(event.newValue)
  }
}

onMounted(() => {
  window.addEventListener('storage', onStorageChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorageChange)
})

// Auto-save whenever chats change
watch(chats, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

// --- Computed ---
const activeChat = computed(() => {
  return chats.value.find((c: any) => c.id === selectedChatId.value) || null
})

// --- Methods ---
const selectChat = (id: number) => {
  selectedChatId.value = id
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

  // Update active chat's message array and time
  activeChat.value.messages.push(newMsg)
  activeChat.value.lastMessageTime = 'Just now'
  
  // Clear input
  newMessage.value = ''

  // Scroll down to see the new message
  await scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  // With shadcn-vue's ScrollArea, we need to target the viewport element inside it
  if (messagesScrollArea.value?.$el) {
    const viewport = messagesScrollArea.value.$el.querySelector('[data-radix-scroll-area-viewport]')
    if (viewport) {
      viewport.scrollTop = viewport.scrollHeight
    }
  }
}
</script>