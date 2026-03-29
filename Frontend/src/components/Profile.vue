<script setup>
import {
  Card, CardContent, CardDescription,
  CardFooter, CardHeader, CardTitle,
} from '@/components/ui/card'

import {
  Avatar, AvatarFallback, AvatarImage,
} from '@/components/ui/avatar'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { AspectRatio } from '@/components/ui/aspect-ratio'
import { Label } from '@/components/ui/label'

import {
  Popover, PopoverContent, PopoverTrigger,
} from '@/components/ui/popover'

import {
  HoverCard, HoverCardContent, HoverCardTrigger,
} from '@/components/ui/hover-card'

import {
  Dialog, DialogClose, DialogContent,
  DialogDescription, DialogFooter, DialogHeader,
  DialogTitle, DialogTrigger,
} from '@/components/ui/dialog'

import {
  Carousel, CarouselContent, CarouselItem,
  CarouselNext, CarouselPrevious
} from '@/components/ui/carousel'

import { Badge } from '@/components/ui/badge'
import { ref, computed, watch } from 'vue'
import deleteIcon from '@/assets/icons/delete.png'

//WARN: ideally, with a fully integrated backend we would try to grab data based on current user.
//1. if user is logged in, if user is a provider, pull provider data based on current user ID.
//2. set defined descriptions/rates/images/avatar left by the user of previous saves.

//NOTE: Variables
const avatar = ref('')
const name = ref('Josh')
const rates = ref('$' + '500')
const userMsg = ref('some random user message')

//NOTE: language search bar
const showScroll = ref(false)
const languageChoice = ref('')
const languageList = ['english', 'chinese', 'spanish', 'arabic', 'vietnamese']
languageList.sort()

function showScrollState() {
  showScroll.value = !showScroll.value
}


//NOTE: This is for image upload, image display
const photoList = ref([])
// const photoList = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) //BUG: for debugging
const selectedImage = ref()
const displayedPhotos = computed(() => photoList.value.slice(0, 4))

function removePhoto(photo) {
  console.log('remove photo -> ' + photo)
  photoList.value = photoList.value.filter((p) => p !== photo)
}


function handleDebug() {
  console.log('userMsg = ' + userMsg.value)
  console.log('rates = ' + rates.value)
  console.log('images = ' + photoList.value)
}

function handleFileChange(event) {
  const file = event.target.files[0] //use this for backend at some point
  if (!file) return
  selectedImage.value = file
  console.log("file = " + file)
  handleFileSubmit()
}

function handleFileSubmit() {
  if (!selectedImage.value) return
  //WARN: URL.createObjectURL creates a fake URL that points to a file/blob
  //so that it can be displayed on the browser with <img src="someBlobs...">
  //since HTML elements expect URLs and not file objects.
  const fileUrl = URL.createObjectURL(selectedImage.value)
  photoList.value.push(fileUrl)
  console.log("fileUrl = " + fileUrl)
  selectedImage.value = null
  forceReRender()
}

//NOTE: Temporary copy pasta for avatar upload and display
function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  selectedImage.value = file
  console.log(file)
  handleAvatarSubmit()
}

function handleAvatarSubmit() {
  if (!selectedImage.value) return
  const fileUrl = URL.createObjectURL(selectedImage.value)
  avatar.value = fileUrl
  console.log(avatar.value)
  selectedImage.value = null
}

//NOTE: Force Re-Render Section
// every time forceReRender is called, this updates
// the component value (componentKey) by 1.
// Making vue to aware an update the component is needed because a value has @change
const componentKey = ref(0)
const forceReRender = () => { componentKey.value++ }

//NOTE: all this to get photo Carousel number update ex. 4th out of 6 photos (4/6)
const api = ref()
const totalCount = computed(() => photoList.value.length)
const current = ref(0)

const showReadMoreButton = computed(() => {
  return provider.aboutMe.split(' ').length > 80
})

function setApi(val) {
  api.value = val
}

watch(api, (api) => {
  if (!api)
    return
  // totalCount.value = api.scrollSnapList().length
  current.value = api.selectedScrollSnap() + 1
  api.on('select', () => {
    current.value = api.selectedScrollSnap() + 1
  })
})

</script>

<template>
  <div>
    <Card class="min-h-200 min-w-150">

      <CardTitle class="text-2xl flex justify-center">Profile Setup</CardTitle>
      <CardHeader class="flex flex-row">
        <div class="flex flex-row gap-5">
          <Label for="avatar" class="cursor-pointer">
            <Input id="avatar" type="file" accept="image/png, image/jpeg" @change="handleAvatarUpload" class="hidden" />
            <Avatar class="scale-[2] m-4">
              <AvatarImage :src="avatar" alt="@shadcn" />
              <AvatarFallback>Avatar</AvatarFallback>
            </Avatar>
          </Label>
          <CardTitle>
            Full Name
            <Input type="text" v-model="name" class="max-w-50"></Input>
          </CardTitle>
        </div>
        <div>
          <CardTitle>
            Rates
            <Input placeholder="$00.00/hr" v-model="rates"> </Input>
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <Label class="p-2">Profile Description</Label>
        <Textarea v-model="userMsg" id="description" class="min-h-50 min-w-full text-pretty" placeholder="Write a concise but detailed description on how you can help the customers.
          Detailing on your experiences, what you may have done before, or who you are.">
        </Textarea>

        <!-- BUG: Disabled until fully implemented -->
        <!-- NOTE: Language Selection Area -->
        <!-- <Label class="mt-5">Language Selection</Label> -->
        <!-- <div class="w-full max-w-sm relative"> -->
        <!--   <div class="flex items-center gap-2"> -->
        <!--     <Input type="text" v-model="languageChoice" @focus="showScrollState" @blur="showScrollState" -->
        <!--       placeholder="test" /> -->
        <!--     <Button type="submit"> add </Button> -->
        <!--   </div> -->
        <!---->
        <!-- NOTE: Floating Dropdown Wrapper -->
        <!--   <div v-if="showScroll" class="absolute mt-1 w-full z-1"> -->
        <!--     <ScrollArea class="h-50 w-full rounded-md"> -->
        <!--       <div class="p-6 space-y-3"> -->
        <!--         <div v-for="language in languageList" @mousedown="selectjob(job)" -->
        <!--           class="cursor-pointer rounded px-2 py-1 hover:bg-muted transition"> -->
        <!--           {{ language }} -->
        <!--         </div> -->
        <!--       </div> -->
        <!--     </ScrollArea> -->
        <!--   </div> -->
        <!-- </div> -->

        <!-- NOTE: Work Photo Section -->
        <Label v-if="photoList.length > 0" for="workPhotos" class="mt-5 mb-2">Work Photos</Label>
        <div id="workPhotos" class="flex">
          <div v-for="photo in displayedPhotos">
            <HoverCard :open-delay="50" :close-delay="0">
              <div class="flex flex-col w-25">
                <HoverCardTrigger>
                  <div class="flex flex-col">
                    <AspectRatio :ratio="1 / 1">
                      <!-- <span class="text-4xl font-semibold"> {{ photo }}</span> -->
                      <img :src="photo" class="object-cover h-full rounded-lg p-0.5" />
                    </AspectRatio>
                  </div>
                </HoverCardTrigger>
                <Button class="hover:bg-destructive hover:text-white self-center" @click="removePhoto(photo)"
                  variant="outline" size="sm">
                  X
                  <!-- <img :src="deleteIcon"> -->
                </Button>
              </div>
              <HoverCardContent class="w-130 border-0">
                <AspectRatio :ratio="3 / 2">
                  <img :src="photo" class="w-full h-full rounded-lg" />
                </AspectRatio>
              </HoverCardContent>
            </HoverCard>
          </div>

          <!-- NOTE: If provider has more than 4 images, condense it. -->
          <div v-if="photoList.length > 4">
            <Dialog>
              <DialogTrigger as-child>
                <button class="w-25 h-full flex flex-col">
                  <AspectRatio :ratio="1 / 1">
                    <div class="relative h-full w-full">
                      <img :src="photoList[4]" class="object-cover h-full rounded-lg p-0.5">
                      <div class="rounded-lg absolute inset-0.5 bg-black/50 flex items-center justify-center">
                        <span class="text-xl font-bold text-white">{{ photoList.length - 4 }}+</span>
                      </div>
                    </div>
                  </AspectRatio>
                </button>
              </DialogTrigger>
              <DialogContent class="min-w-100 max-w-170 flex justify-center">
                <DialogHeader>
                  <DialogTitle></DialogTitle>
                  <DialogDescription></DialogDescription>

                  <!-- BUG: why tf does this cause an error???? -->
                  <!-- <Carousel class="flex flex-col items-center" :opts="{ startIndex: 4, loop: true, duration: 10 }" -->

                  <Carousel class="flex flex-col items-center" :opts="{ startIndex: 4, loop: true, duration: 10 }"
                    @init-api="setApi">
                    <CarouselContent>
                      <CarouselItem v-for="photo in photoList" :key="photo">
                        <div class="flex flex-col items-center aspect-square">
                          <!-- <div> -->
                          <!-- <span class="text-4xl font-semibold"> {{ photo }}</span> -->
                          <img :src="photo" class="w-full h-full object-cover rounded-lg" />
                          <!-- </div> -->
                          <Button class="mt-2 mb-5 w-20 hover:bg-destructive hover:text-white"
                            @click="removePhoto(photo)" variant="outline">Remove</Button>
                        </div>
                      </CarouselItem>
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                    <Badge class="mt-2 text-sm bg-blue-500 text-white" variant="outline">
                      {{ current }} of {{ totalCount }} photos
                    </Badge>
                  </Carousel>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <Label for="picture" class="mt-5">Photo Upload</Label>
        <Input id="picture" :key="componentKey" type="file" accept="image/png, image/jpeg" @change="handleFileChange"
          class="w-50 cursor-pointer" />
      </CardContent>
      <CardFooter>
        <Button :onclick="handleDebug">Save Profile</Button>
      </CardFooter>
    </Card>
  </div>
</template>
