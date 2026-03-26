import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { faker } from '@faker-js/faker';
import workPhoto1 from '@/assets/workPhotos/bathroom.jpg'
import workPhoto2 from '@/assets/workPhotos/garden.jpg'
import workPhoto3 from '@/assets/workPhotos/kitchen.jpg'
import profAvatar from '@/assets/avatars/avatar.png'
import defaultAvatar from '@/assets/avatars/defaultAvatar.png'
import starIcon from '@/assets/icons/star.png'
import checkMarkIcon from '@/assets/icons/checkMark.png'
import aboutMeIcon from '@/assets/icons/aboutMe.png'
import albumIcon from '@/assets/icons/album.png'
import reviewIcon from '@/assets/icons/review.png'
import spainFlag from '@/assets/flags/ES.svg'
import vietnamFlag from '@/assets/flags/VN.svg'
import arabicFlag from '@/assets/flags/SA.svg'
import chinaFlag from '@/assets/flags/CN.svg'
import usFlag from '@/assets/flags/US.svg'
// export const useAlertsStore = defineStore('alerts', {
//
// })

// export const useCounterStore = defineStore('counter', () => {
//   const count = ref(0)
//   const name = ref('Eduardo')
//   const doubleCount = computed(() => count.value * 2)
//   function increment() {
//     count.value++
//   }
//
//   return { count, name, doubleCount, increment }
// })

// NOTE: generatesProvider() generates a list of providers with random data,
// calls it and return object list of providers
export const userList = defineStore('users', () => {
  const generateProvider = () => {
    const randomNumber = faker.number.int(150)
    return {
      name: faker.person.fullName(),
      avatar: faker.image.avatar(),
      price: randomNumber,
      workPhotos: [workPhoto1, workPhoto2, workPhoto3, workPhoto1, workPhoto2, workPhoto3],
      aboutMe: faker.lorem.paragraph({ min: 1, max: randomNumber }),
      averageRating: '4.9',
      jobsCompleted: randomNumber,
      datesBooked: [],
      languages: [spainFlag, usFlag, chinaFlag, arabicFlag, vietnamFlag],
      ratings: Array.from({ length: randomNumber }, (_, i) => ({
        jobType: ['Gardening', 'Plumbing', 'Carpentry', 'Electrical'][i % 4],
        userName: faker.person.fullName(),
        date: faker.date.anytime(),
        userAvatar: defaultAvatar,
        userRated: Math.floor(Math.random() * 5) + 1,
        userComment: faker.lorem.paragraph(),
      })),
    }
  }
  const providers = ref(Array.from({ length: 15 }, generateProvider))
  return { providers }
})
