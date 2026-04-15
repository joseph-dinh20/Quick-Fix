<script setup>
import { ref, reactive } from 'vue'
import { createReport } from '../services/api'

// shadcn-vue component imports
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

// We need the ID of the profile being reported passed in as a prop
const props = defineProps({
  reportedProfileId: {
    type: [String, Number],
    required: true
  }
})

// Match the fields defined in ReportCreateSerializer
const form = reactive({
  reason: '',
  details: ''
})

const isSubmitting = ref(false)
const errorMessage = ref('')
const isSuccess = ref(false)

const submitReport = async () => {
  isSubmitting.value = true
  errorMessage.value = ''
  isSuccess.value = false

  const payload = {
    reported_profile: props.reportedProfileId,
    reason: form.reason,
    details: form.details,
  }

  try {
    // Replace the URL with the actual path defined in your Django urls.py
    await createReport(payload)
    
    isSuccess.value = true
    form.reason = ''
    form.details = ''
  } catch (error) {
    // The Django view returns {"detail": "You cannot report yourself."} on a 400 error
    // It also returns serializer errors which we can parse here.
    errorMessage.value = 
      error.response?.data?.detail || 
      error.response?.data?.reason?.[0] || 
      'An unexpected error occurred while submitting your report.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="max-w-md mx-auto p-4 border rounded-lg bg-card text-card-foreground shadow-sm">
    <form @submit.prevent="submitReport">
      <fieldset :disabled="isSubmitting" class="space-y-6">
        <legend class="text-xl font-semibold leading-none tracking-tight mb-4">
          Report Profile
        </legend>

        <p v-if="isSuccess" class="text-sm font-medium text-green-600 dark:text-green-500">
          Report submitted successfully. Thank you for keeping the community safe.
        </p>
        
        <p v-if="errorMessage" class="text-sm font-medium text-destructive">
          {{ errorMessage }}
        </p>

        <article class="space-y-4 text-sm">
          <p class="flex flex-col space-y-2">
            <Label for="reason">Reason for reporting</Label>
            <Select v-model="form.reason" required>
              <SelectTrigger id="reason">
                <SelectValue placeholder="Select a reason" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="spam">Spam</SelectItem>
                <SelectItem value="harassment">Harassment</SelectItem>
                <SelectItem value="fake_profile">Fake Profile</SelectItem>
                <SelectItem value="inappropriate_content">Inappropriate Content</SelectItem>
                <SelectItem value="scam">Scam</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectContent>
            </Select>
          </p>

          <p class="flex flex-col space-y-2">
            <Label for="details">Additional Details (Optional)</Label>
            <Textarea
              id="details"
              v-model="form.details"
              placeholder="Please provide any additional context..."
              rows="4"
              class="resize-none"
            />
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