<script setup>
import { onMounted, ref, reactive } from "vue";
import { createReview, loadProviders } from "../services/api";

// shadcn-vue component imports
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

// Form state matching the Review model
const form = reactive({
    service_provider: "",
    rating: "5", // Default to 5 stars
    comment: "",
    images: [],
});

const providers = ref([]);
const isFetchingProviders = ref(false);
const isSubmitting = ref(false);
const errorMessage = ref("");
const isSuccess = ref(false);

const fetchProviders = async () => {
    isFetchingProviders.value = true;
    try {
        const response = await loadProviders();
        providers.value = response.data;
    } catch (error) {
        console.error("Failed to load providers", error);
        errorMessage.value = "Failed to load service providers.";
    } finally {
        isFetchingProviders.value = false;
    }
};

onMounted(() => {
    fetchProviders();
});

// Capture uploaded files and store them in the reactive form state
const handleFileChange = (event) => {
    form.images = Array.from(event.target.files);
};

const submitReview = async () => {
    isSubmitting.value = true;
    errorMessage.value = "";
    isSuccess.value = false;

    // Use FormData because we are dealing with potential Image file uploads
    const formData = new FormData();
    formData.append("rating", form.rating);
    formData.append("comment", form.comment);
    
    // Append each image to the FormData array
    form.images.forEach((file) => {
        formData.append("images", file);
    });

    try {
        // Pass the provider ID in the URL path, and the formData in the body
        await createReview(form.service_provider, formData);

        isSuccess.value = true;
        form.service_provider = "";
        form.rating = "5";
        form.comment = "";
        form.images = [];
        
        // Reset the physical file input element
        const fileInput = document.getElementById("images");
        if (fileInput) fileInput.value = "";

    } catch (error) {
        console.error("Error submitting review:", error);
        if (error.response?.data?.error) {
            errorMessage.value = error.response.data.error; // Catches "Cannot review yourself"
        } else {
            errorMessage.value = "An error occurred while submitting your review.";
        }
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<template>
    <section class="max-w-md mx-auto p-6 border rounded-lg bg-card text-card-foreground shadow-sm">
        <form @submit.prevent="submitReview">
            <fieldset :disabled="isSubmitting" class="space-y-6">
                <legend class="text-xl font-semibold leading-none tracking-tight mb-4">
                    Review a Service Provider
                </legend>

                <p v-if="isSuccess" class="text-sm font-medium text-green-600 dark:text-green-500">
                    Review submitted successfully. Thank you for your feedback!
                </p>

                <p v-if="errorMessage" class="text-sm font-medium text-destructive bg-destructive/10 p-3 rounded-md">
                    {{ errorMessage }}
                </p>

                <article class="space-y-5 text-sm">
                    <p class="flex flex-col space-y-2">
                        <Label for="profile">Who are you reviewing?</Label>
                        <Select v-model="form.service_provider" required :disabled="isFetchingProviders">
                            <SelectTrigger id="profile">
                                <SelectValue :placeholder="isFetchingProviders ? 'Loading providers...' : 'Select a provider'" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="provider in providers" :key="provider.id" :value="String(provider.id)">
                                    {{ provider.name || `Provider #${provider.id}` }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </p>

                    <p class="flex flex-col space-y-2">
                        <Label for="rating">Rating</Label>
                        <Select v-model="form.rating" required>
                            <SelectTrigger id="rating">
                                <SelectValue placeholder="Select a rating" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="5">5 - Excellent</SelectItem>
                                <SelectItem value="4">4 - Very Good</SelectItem>
                                <SelectItem value="3">3 - Average</SelectItem>
                                <SelectItem value="2">2 - Poor</SelectItem>
                                <SelectItem value="1">1 - Terrible</SelectItem>
                            </SelectContent>
                        </Select>
                    </p>

                    <p class="flex flex-col space-y-2">
                        <Label for="comment">Review Comment</Label>
                        <Textarea
                            id="comment"
                            v-model="form.comment"
                            required
                            placeholder="Describe your experience with this provider..."
                            rows="4"
                            class="resize-none" />
                    </p>

                    <p class="flex flex-col space-y-2">
                        <Label for="images">Upload Photos (Optional)</Label>
                        <Input 
                            id="images" 
                            type="file" 
                            accept="image/*" 
                            multiple 
                            @change="handleFileChange" 
                        />
                    </p>
                </article>

                <menu class="flex justify-end p-0 m-0">
                    <Button type="submit" class="w-full sm:w-auto">
                        <span v-if="isSubmitting">Submitting...</span>
                        <span v-else>Submit Review</span>
                    </Button>
                </menu>
            </fieldset>
        </form>
    </section>
</template>