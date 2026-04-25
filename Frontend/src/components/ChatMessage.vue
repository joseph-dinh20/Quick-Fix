<template>
  <div :class="messageClasses">
    <div class="flex items-start space-x-3">
      <div v-if="isSent" class="flex-shrink-0">
        <span class="block w-8 h-8 rounded-full bg-gray-300"></span>
      </div>
      
      <div class="flex-1 space-y-1">
        <p :class="messageTextClass">{{ message.content }}</p>
        <span class="text-xs text-gray-500">{{ timestamp }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: Object,
      required: true,
    },
    isSent: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    messageClasses() {
      return this.isSent
        ? "flex justify-end space-x-4 py-2"
        : "flex justify-start space-x-4 py-2";
    },
    messageTextClass() {
      return this.isSent
        ? "bg-blue-100 text-blue-800 p-3 rounded-lg"
        : "bg-gray-100 text-gray-800 p-3 rounded-lg";
    },
    timestamp() {
      return new Date(this.message.timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>

<style scoped>
/* You can add any scoped styles here if needed */
</style>