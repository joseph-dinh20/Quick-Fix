<script setup>
import { onMounted, ref, reactive } from "vue";
import { createReport, loadProviders } from "../services/api";

// shadcn-vue component imports
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

// We need the ID of the profile being reported passed in as a prop
const props = defineProps({
    reportedProfileId: {
        type: [String, Number],
        required: true,
    },
});

// Match the fields defined in ReportCreateSerializer
const form = reactive({
    reported_profile: "",
    reason: "",
    details: "",
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
        errorMessage.value = "Failed to load service providers to report.";
    } finally {
        isFetchingProviders.value = false;
    }
};

onMounted(() => {
    fetchProviders();
});

const submitReport = async () => {
    isSubmitting.value = true;
    errorMessage.value = "";
    isSuccess.value = false;

    const payload = {
        reported_profile: Number(form.reported_profile),
        reason: form.reason,
        details: form.details,
    };

    try {
        // Replace the URL with the actual path defined in your Django urls.py
        await createReport(payload);

        isSuccess.value = true;
        form.reported_profile = "";
        form.reason = "";
        form.details = "";
    } catch (error) {
        console.error("Full Error Response:", error.response?.data);

        // Detailed error parsing to catch specific 400 Bad Request messages
        if (error.response?.data) {
            const data = error.response.data;
            if (data.detail) {
                errorMessage.value = data.detail; // Catches "You cannot report yourself."
            } else if (data.reported_profile) {
                errorMessage.value = `Profile Error: ${data.reported_profile[0]}`;
            } else if (data.reason) {
                errorMessage.value = `Reason Error: ${data.reason[0]}`;
            } else {
                errorMessage.value =
                    "Please check your form inputs and try again.";
            }
        } else {
            errorMessage.value =
                "An unexpected error occurred communicating with the server.";
        }
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<template>
    <section
        class="max-w-md mx-auto p-6 border rounded-lg bg-card text-card-foreground shadow-sm">
        <form @submit.prevent="submitReport">
            <fieldset :disabled="isSubmitting" class="space-y-6">
                <legend
                    class="text-xl font-semibold leading-none tracking-tight mb-4">
                    Report a Service Provider
                </legend>

                <p
                    v-if="isSuccess"
                    class="text-sm font-medium text-green-600 dark:text-green-500">
                    Report submitted successfully. Thank you for keeping the
                    community safe.
                </p>

                <p
                    v-if="errorMessage"
                    class="text-sm font-medium text-destructive bg-destructive/10 p-3 rounded-md">
                    {{ errorMessage }}
                </p>

                <article class="space-y-5 text-sm">
                    <p class="flex flex-col space-y-2">
                        <Label for="profile">Who do you want to report?</Label>
                        <Select
                            v-model="form.reported_profile"
                            required
                            :disabled="isFetchingProviders">
                            <SelectTrigger id="profile">
                                <SelectValue
                                    :placeholder="
                                        isFetchingProviders
                                            ? 'Loading providers...'
                                            : 'Select a provider'
                                    " />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem
                                    v-for="provider in providers"
                                    :key="provider.id"
                                    :value="provider.id">
                                    {{
                                        provider.name ||
                                        `Provider #${provider.id}`
                                    }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </p>

                    <p class="flex flex-col space-y-2">
                        <Label for="reason">Reason for reporting</Label>
                        <Select v-model="form.reason" required>
                            <SelectTrigger id="reason">
                                <SelectValue placeholder="Select a reason" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="spam">Spam</SelectItem>
                                <SelectItem value="harassment"
                                    >Harassment</SelectItem
                                >
                                <SelectItem value="fake_profile"
                                    >Fake Profile</SelectItem
                                >
                                <SelectItem value="inappropriate_content"
                                    >Inappropriate Content</SelectItem
                                >
                                <SelectItem value="scam">Scam</SelectItem>
                                <SelectItem value="other">Other</SelectItem>
                            </SelectContent>
                        </Select>
                    </p>

                    <p class="flex flex-col space-y-2">
                        <Label for="details"
                            >Additional Details (Optional)</Label
                        >
                        <Textarea
                            id="details"
                            v-model="form.details"
                            placeholder="Please provide any context..."
                            rows="4"
                            class="resize-none" />
                    </p>
                </article>

                <menu class="flex justify-end p-0 m-0">
                    <Button type="submit" class="w-full sm:w-auto">
                        <span v-if="isSubmitting">Submitting...</span>
                        <span v-else>Submit Report</span>
                    </Button>
                </menu>
            </fieldset>
        </form>
    </section>
</template>
