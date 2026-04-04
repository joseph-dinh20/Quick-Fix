<script setup>
const features = [
    {
        icon: "📅",
        title: "Flexible Schedule",
        desc: "You're in control. Work when you want, where you want, and only on the tasks you choose.",
    },
    {
        icon: "＄",
        title: "Great Earnings",
        desc: "Set your own hourly rates and keep 100% of your tips. Get paid directly to your bank account.",
    },
    {
        icon: "🔧",
        title: "Build Your Business",
        desc: "Focus on what you’re good at, from furniture assembly to home repairs. We handle the marketing.",
    },
];

const steps = [
    {
        number: 1,
        title: "Sign Up",
        desc: "Create your account and tell us which services you want to offer.",
    },
    {
        number: 2,
        title: "Get Verified",
        desc: "Submit your ID through our secure verification portal.",
    },
    {
        number: 3,
        title: "Start Fixing",
        desc: "Set your availability and start receiving task requests in your area.",
    },
];
</script>

<template>
    <div class="min-h-screen font-sans text-[#1a202c] bg-white">
        <header class="py-20 px-6 bg-[#f9fafb] text-center">
            <h1 class="text-5xl md:text-6xl font-black mb-6 tracking-tight">
                Earn money your way
            </h1>
            <p
                class="max-w-2xl mx-auto text-gray-500 text-lg mb-10 leading-relaxed"
            >
                Be your own boss. Set your own rates. Help your community. Join
                the Quick Fix team today.
            </p>

            <div
                class="flex flex-col sm:flex-row justify-center items-center gap-4 max-w-lg mx-auto"
            >
                <input
                    type="email"
                    placeholder="Enter your email"
                    class="w-full px-6 py-4 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-500 shadow-sm"
                />
                <button
                    class="w-full sm:w-auto bg-[#FF7D1F] hover:bg-orange-600 text-white font-bold px-8 py-4 rounded-xl transition-all whitespace-nowrap"
                >
                    Get Started
                </button>
            </div>
            <p class="mt-6 text-sm text-gray-400">
                Already have an account?
                <a href="#/Signup" class="text-orange-500 font-bold hover:underline"
                    >Sign In</a
                >
            </p>
        </header>

        <section class="py-24 px-6 max-w-7xl mx-auto">
            <h2 class="text-3xl font-extrabold text-center mb-16">
                Why join Quick Fix?
            </h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div
                    v-for="item in features"
                    :key="item.title"
                    class="p-10 border border-gray-400 rounded-[2rem] hover:shadow-2xl transition-shadow duration-300"
                >
                    <div class="text-3xl mb-6">{{ item.icon }}</div>
                    <h3 class="text-xl font-bold mb-4">{{ item.title }}</h3>
                    <p class="text-gray-500 leading-relaxed">{{ item.desc }}</p>
                </div>
            </div>
        </section>

        <section class="relative left-[50%] right-[50%] ml-[-50vw] mr-[-50vw] w-[99vw] py-24 px-6 bg-[#0f172a] text-white overflow-hidden">
            <div class="max-w-7xl mx-auto">
                <h2 class="text-3xl font-extrabold text-center mb-20">
                    How to get started
                </h2>
                <div class="grid md:grid-cols-3 gap-16 text-center">
                    <div
                        v-for="step in steps"
                        :key="step.number"
                        class="flex flex-col items-center"
                    >
                        <div
                            class="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center font-bold mb-6 text-lg"
                        >
                            {{ step.number }}
                        </div>
                        <h3 class="text-xl font-bold mb-4">{{ step.title }}</h3>
                        <p class="text-gray-400 text-sm leading-relaxed">
                            {{ step.desc }}
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-24 px-6">
            <div
                class="max-w-4xl mx-auto bg-[#fff0e5] rounded-[2.5rem] p-12 md:p-20 text-center"
            >
                <h2 class="text-3xl font-extrabold mb-6">Ready to earn?</h2>
                <p class="text-gray-600 mb-10 max-w-md mx-auto">
                    Join thousands of Fixers across the country helping people
                    get things done.
                </p>
                <button
                    class="bg-[#1a1a1a] hover:bg-black text-white font-bold px-12 py-4 rounded-xl transition-transform active:scale-95 shadow-lg hover:shadow-xl"
                >
                    Apply Now
                </button>
            </div>
        </section>

        <footer
            class="py-12 text-center text-xs text-gray-400 border-t border-gray-100"
        >
            © 2026 Quick Fix Inc. All rights reserved.
        </footer>
    </div>
</template>
