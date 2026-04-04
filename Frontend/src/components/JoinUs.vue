<script setup>
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from '@/components/ui/card'

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
    <div class="min-h-screen font-sans text-foreground bg-background">
        <header class="py-24 px-6 bg-muted/30 text-center border-b border-border">
            <h1 class="text-5xl md:text-6xl font-black mb-6 tracking-tight text-balance">
                Earn money your way
            </h1>
            <p class="max-w-2xl mx-auto text-muted-foreground text-lg mb-10 leading-relaxed">
                Be your own boss. Set your own rates. Help your community. Join
                the Quick Fix team today.
            </p>

            <div class="flex flex-col sm:flex-row justify-center items-center gap-4 max-w-lg mx-auto">
                <Input 
                    type="email" 
                    placeholder="Enter your email" 
                    class="h-14 px-6 rounded-xl border-input focus-visible:ring-orange-500 shadow-sm"
                />
                <Button 
                    class="w-full sm:w-auto h-14 bg-[#FF7D1F] hover:bg-orange-600 text-white font-bold px-8 rounded-xl transition-all"
                >
                    Get Started
                </Button>
            </div>
            <p class="mt-6 text-sm text-muted-foreground">
                Already have an account?
                <router-link to="/Signup" class="text-orange-500 font-bold hover:underline">
                    Sign In
                </router-link>
            </p>
        </header>

        <section class="py-24 px-6 max-w-7xl mx-auto">
            <h2 class="text-3xl font-extrabold text-center mb-16">
                Why join Quick Fix?
            </h2>
            <div class="grid md:grid-cols-3 gap-8">
                <Card 
                    v-for="item in features" 
                    :key="item.title"
                    class="border-border rounded-[2rem] hover:shadow-xl transition-all duration-300 group"
                >
                    <CardHeader class="p-10 pb-4">
                        <div class="text-4xl mb-6 group-hover:scale-110 transition-transform duration-300 origin-left">
                            {{ item.icon }}
                        </div>
                        <CardTitle class="text-xl font-bold">{{ item.title }}</CardTitle>
                    </CardHeader>
                    <CardContent class="px-10 pb-10">
                        <p class="text-muted-foreground leading-relaxed">{{ item.desc }}</p>
                    </CardContent>
                </Card>
            </div>
        </section>

        <section class="w-full py-24 px-6 bg-slate-950 text-white">
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
                        <div class="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center font-bold mb-6 text-lg ring-4 ring-orange-500/20">
                            {{ step.number }}
                        </div>
                        <h3 class="text-xl font-bold mb-4">{{ step.title }}</h3>
                        <p class="text-slate-400 text-sm leading-relaxed max-w-[250px]">
                            {{ step.desc }}
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-24 px-6">
            <div class="max-w-4xl mx-auto bg-orange-50 rounded-[2.5rem] p-12 md:p-20 text-center border border-orange-100/50">
                <h2 class="text-3xl font-extrabold mb-6">Ready to earn?</h2>
                <p class="text-muted-foreground mb-10 max-w-md mx-auto">
                    Join thousands of Fixers across the country helping people
                    get things done.
                </p>
                <Button 
                    size="lg"
                    class="bg-slate-900 hover:bg-black text-white font-bold h-14 px-12 rounded-xl transition-transform active:scale-95 shadow-lg"
                >
                    Apply Now
                </Button>
            </div>
        </section>

        <footer class="py-12 text-center text-xs text-muted-foreground border-t border-border/50">
            © 2026 Quick Fix Inc. All rights reserved.
        </footer>
    </div>
</template>