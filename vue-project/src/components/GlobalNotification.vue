<template>
  <v-snackbar
    v-model="notification.show"
    :color="getColor(notification.type)"
    :timeout="notification.timeout"
    location="top right"
    class="global-notification"
  >
    <div class="notification-content">
      <v-icon class="notification-icon">
        {{ getIcon(notification.type) }}
      </v-icon>
      <span class="notification-message">
        {{ notification.message }}
      </span>
    </div>

    <template v-slot:actions>
      <v-btn
        color="white"
        variant="text"
        @click="hideNotification"
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { useNotification } from '@/composables/useNotification'

const { notification, hideNotification } = useNotification()

const getColor = (type) => {
  const colors = {
    success: 'success',
    error: 'error',
    warning: 'warning',
    info: 'info'
  }
  return colors[type] || 'info'
}

const getIcon = (type) => {
  const icons = {
    success: 'mdi-check-circle',
    error: 'mdi-alert-circle',
    warning: 'mdi-alert',
    info: 'mdi-information'
  }
  return icons[type] || 'mdi-information'
}
</script>

<style scoped>
.notification-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.notification-icon {
  font-size: 1.25rem;
}

.notification-message {
  font-weight: 500;
}

:deep(.v-snackbar__wrapper) {
  min-width: 300px;
  max-width: 500px;
}
</style> 