<script setup>
import { ref, reactive } from "vue";

const isEditing = ref(false);

const navLinks = [
    { name: "Home", icon: "HomeIcon", hasArrow: true },
    { name: "Personal Info", icon: "UserIcon", hasArrow: true },
    { name: "Security & sign-in", icon: "LockClosedIcon", hasArrow: true },
    { name: "Data & privacy", icon: "EyeIcon", hasArrow: true },
    { name: "Payment info", icon: "CreditCardIcon", hasArrow: true },
];

// FIX: Make personalData reactive using ref()
const personalData = ref([
    { label: "Name", value: "Joseph A." },
    { label: "Email", value: "Joseph.AAA@gmail.com" },
    { label: "Location", value: "1234 567th Street, City, State" },
]);

const editedData = reactive([]);

// Populate it safely when the component loads
const syncData = () => {
    editedData.length = 0; // Clear the array
    
    // FIX: Because personalData is now a ref, you must access it with .value
    personalData.value.forEach((item) => {
        editedData.push({ ...item }); // Shallow clone each object
    });
};

// Initial sync
syncData();

const saveChanges = () => {
    // FIX: Update personalData.value with the edited values
    personalData.value = editedData.map((item) => ({ ...item }));
    isEditing.value = false;

    console.log("Its working");
    syncData();
};

const cancelChanges = () => {
    syncData(); // Reset editedData to match original
    isEditing.value = false;
};
</script>

<template>
    <div
        class="min-h-screen bg-white font-poppins text-slate-900 py-12 px-10 w-full"
    >
        <div
            class="max-w-none w-full grid grid-cols-1 md:grid-cols-[280px_1fr] gap-16"
        >
            <aside class="space-y-8">
                <nav class="space-y-2">
                    <div
                        v-for="link in navLinks"
                        :key="link.name"
                        class="flex items-center justify-between py-2.5 px-3 cursor-pointer hover:bg-gray-50 rounded-lg group"
                    >
                        <div
                            class="flex items-center gap-3 text-sm font-medium text-gray-600 group-hover:text-black"
                        >
                            <div class="w-5 h-5 bg-gray-200 rounded-sm"></div>
                            {{ link.name }}
                        </div>
                        <span
                            v-if="link.hasArrow"
                            class="text-[10px] text-gray-400"
                            >▶</span
                        >
                    </div>
                </nav>

                <div class="space-y-3">
                    <button
                        class="w-full bg-orange-500 text-white py-3 px-4 rounded-md text-sm font-bold flex items-center justify-center gap-2 hover:bg-orange-600 transition-colors"
                    >
                        🔍 FIND WORK
                    </button>
                    <button
                        class="w-full border border-orange-500 text-orange-500 py-3 px-4 rounded-md text-sm font-bold flex items-center justify-center gap-2 hover:bg-orange-50 transition-colors"
                    >
                        ⊕ MAKE A JOB
                    </button>
                </div>
            </aside>

            <main class="space-y-10 w-full">
                <h1 class="text-5xl font-extrabold mb-10 tracking-tight">
                    Your Account
                </h1>

                <section
                    class="p-10 border border-gray-300 rounded-[2.5rem] shadow-sm w-full"
                >
                    <h2 class="text-2xl font-bold mb-4">Overview</h2>
                    <hr class="border-gray-200 mb-8" />
                    <div class="space-y-4">
                        <a
                            href="#"
                            class="block text-blue-500 font-medium hover:underline text-lg"
                            >Manage profile</a
                        >
                        <a
                            href="#"
                            class="block text-blue-500 font-medium hover:underline text-lg"
                            >Manage postings</a
                        >
                        <a
                            href="#"
                            class="block text-blue-500 font-medium hover:underline text-lg"
                            >View favorites</a
                        >
                    </div>
                </section>

                <section
                    class="p-10 border border-gray-300 rounded-[2.5rem] shadow-sm w-full bg-white"
                >
                    <div class="flex justify-between items-start">
                        <div>
                            <h2 class="text-2xl font-bold">
                                Personal Information
                            </h2>
                            <p class="text-gray-500 text-sm mt-1">
                                Manage your public and private details.
                            </p>
                        </div>
                        <div class="bg-gray-100 p-3 rounded-full">
                            <svg
                                class="w-10 h-10 text-gray-400"
                                fill="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                                />
                            </svg>
                        </div>
                    </div>

                    <hr class="border-gray-200 my-8" />

                    <div class="space-y-6">
                        <div
                            v-for="(row, index) in personalData"
                            :key="row.label"
                            class="flex justify-between items-center text-lg py-3 group border-b border-transparent hover:border-gray-100 transition-all"
                        >
                            <span
                                class="font-bold w-48 text-gray-900 shrink-0"
                                >{{ row.label }}</span
                            >

                            <div class="flex-1 pr-10 min-w-0">
                                <input
                                    v-if="isEditing"
                                    v-model="editedData[index].value"
                                    class="w-full bg-gray-50 border-b-2 border-primary/30 focus:border-primary outline-none py-1 px-2 rounded-t-md transition-all"
                                    type="text"
                                />
                                <span
                                    v-else
                                    @click="isEditing = true"
                                    class="block w-full truncate text-gray-600 cursor-pointer hover:text-gray-900 transition-colors"
                                >
                                    {{ row.value }}
                                </span>
                            </div>

                            <span
                                class="text-gray-300 group-hover:text-primary transition-colors shrink-0"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2.5"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="m9 18 6-6-6-6" />
                                </svg>
                            </span>
                        </div>
                    </div>

                    <div
                        v-if="isEditing"
                        class="mt-10 flex gap-4 animate-in fade-in slide-in-from-bottom-2"
                    >
                        <button
                            @click="saveChanges"
                            class="bg-[#FF7D1F] hover:bg-[#e66d1a] text-white font-bold py-3 px-8 rounded-2xl shadow-lg shadow-orange-200 transition-all active:scale-95"
                        >
                            Save Changes
                        </button>
                        <button
                            @click="cancelChanges"
                            class="bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold py-3 px-8 rounded-2xl transition-all"
                        >
                            Cancel
                        </button>
                    </div>
                </section>

                <section
                    class="p-10 border border-gray-300 rounded-[2.5rem] w-full shadow-sm w-full"
                >
                    <h2 class="text-2xl font-bold mb-4">Security & sign-in</h2>
                    <hr class="border-gray-200 mb-8" />
                    <div class="space-y-5">
                        <a
                            href="#"
                            class="block text-blue-500 font-medium hover:underline text-lg"
                            >Change Password</a
                        >
                        <a
                            href="#"
                            class="block text-blue-500 font-medium hover:underline text-lg"
                            >Enable two-factor authentication</a
                        >
                    </div>
                </section>

                <section
                    class="p-10 border border-gray-300 rounded-[2.5rem] w-full shadow-sm w-full"
                >
                    <h2 class="text-2xl font-bold mb-4">Data & Privacy</h2>
                    <hr class="border-gray-200 mb-8" />
                    <div class="space-y-8">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-lg"
                                >Use data to improve site</span
                            >
                            <input
                                type="checkbox"
                                checked
                                class="accent-orange-500 w-6 h-6 cursor-pointer"
                            />
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-lg"
                                >Use data to personalize experience</span
                            >
                            <input
                                type="checkbox"
                                checked
                                class="accent-orange-500 w-6 h-6 cursor-pointer"
                            />
                        </div>

                        <div class="flex justify-between items-center">
                            <span class="font-bold text-lg"
                                >Make Account Visible</span
                            >
                            <input
                                type="checkbox"
                                checked
                                class="accent-orange-500 w-6 h-6 cursor-pointer"
                            />
                        </div>
                    </div>
                </section>
            </main>
        </div>
    </div>
</template>
