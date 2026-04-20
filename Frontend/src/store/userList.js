import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { faker } from "@faker-js/faker";
import workPhoto1 from "@/assets/workPhotos/bathroom.jpg";
import workPhoto2 from "@/assets/workPhotos/garden.jpg";
import workPhoto3 from "@/assets/workPhotos/kitchen.jpg";
import profAvatar from "@/assets/avatars/avatar.png";
import defaultAvatar from "@/assets/avatars/defaultAvatar.png";
import starIcon from "@/assets/icons/star.png";
import checkMarkIcon from "@/assets/icons/checkMark.png";
import aboutMeIcon from "@/assets/icons/aboutMe.png";
import albumIcon from "@/assets/icons/album.png";
import reviewIcon from "@/assets/icons/review.png";
import spainFlag from "@/assets/flags/ES.svg";
import vietnamFlag from "@/assets/flags/VN.svg";
import arabicFlag from "@/assets/flags/SA.svg";
import chinaFlag from "@/assets/flags/CN.svg";
import usFlag from "@/assets/flags/US.svg";

// WARN: now directly using one time generated data stored in providers.json
import providersData from "@/store/data/providers.json";
export const userListStore = defineStore("users", () => {
  const providers = ref(providersData);
  return { providers };
});


// This is to store who is being reported, this is so userIDs do not get leaked into the URL
export const reportStore = defineStore("report", () => {
    const targetUser = ref({ id: null, username: "" });

    function setTargetUser(userData) {
        targetUser.value = userData;
    }

    return { targetUser, setTargetUser };
});

export const reviewStore = defineStore("review", () => {
    const targetUser = ref({ id: null, username: "" });

    function setTargetUser(userData) {
        targetUser.value = userData;
    }

    return { targetUser, setTargetUser };
});

// NOTE: generatesProvider() generates a list of providers with random data,
// calls it and return object list of providers
// export const userListStore = defineStore("users", () => {
//   const generateProvider = () => {
//     const randomNumber = faker.number.int(150);
//     return {
//       userID: faker.number.int(randomNumber * 100),
//       name: faker.person.fullName(),
//       avatar: faker.image.avatar(),
//       price: randomNumber,
//       workPhotos: Array.from(
//         { length: faker.number.int({ min: 7, max: 10 }) },
//         () => faker.image.urlPicsumPhotos({ width: 800, height: 800 }),
//       ),
//       aboutMe: faker.lorem.paragraph({ min: 1, max: randomNumber + 1 }),
//       averageRating: "4.9",
//       jobsCompleted: randomNumber,
//       datesBooked: [],
//       languages: [spainFlag, usFlag, chinaFlag, arabicFlag, vietnamFlag],
//       ratings: Array.from({ length: randomNumber }, (_, i) => ({
//         jobType: ["Gardening", "Plumbing", "Carpentry", "Electrical"][i % 4],
//         userName: faker.person.fullName(),
//         date: faker.date.anytime(),
//         userAvatar: defaultAvatar,
//         userRated: Math.floor(Math.random() * 5) + 1,
//         userComment: faker.lorem.paragraph(),
//       })),
//     };
//   };
//   const providers = ref(Array.from({ length: 15 }, generateProvider));
//   return { providers };
// });

export const favoriteListStore = defineStore("favoriteProviderStore", () => {
  const generateFavoriteList = () => {
    const randomNum = faker.number.int(100);
    return {
      userID: faker.number.int(randomNum * 100),
      name: faker.person.fullName(),
      avatar: faker.image.avatar(),
      hiredFor: ["Plumming", "Grass Cutting", "Pet Walking", "Face Painting"][
        faker.number.int({ min: 0, max: 3 })
      ],
      dateRecentlyHired: faker.date.anytime(),
      userRated: Math.floor(Math.random() * 5) + 1,
    };
  };
  const favoriteProviders = ref(
    Array.from({ length: 10 }, generateFavoriteList),
  );
  //WARN: the array name here MATTERS. favoriteProviders will be passed
  //down to be destructured.
  //example in FavoriteProvider.vue: const { favoriteProviders } = storeToRefs(store)
  return { favoriteProviders };
});
