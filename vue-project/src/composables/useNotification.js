import { ref } from 'vue'

const notification = ref({
  show: false,
  message: '',
  type: 'success', // success, error, warning, info
  timeout: 3000
})

export function useNotification() {
  const showNotification = (message, type = 'success', timeout = 3000) => {
    notification.value = {
      show: true,
      message,
      type,
      timeout
    }

    // Auto-hide notification
    setTimeout(() => {
      notification.value.show = false
    }, timeout)
  }

  const showSuccess = (message, timeout = 3000) => {
    showNotification(message, 'success', timeout)
  }

  const showError = (message, timeout = 5000) => {
    showNotification(message, 'error', timeout)
  }

  const showWarning = (message, timeout = 4000) => {
    showNotification(message, 'warning', timeout)
  }

  const showInfo = (message, timeout = 3000) => {
    showNotification(message, 'info', timeout)
  }

  const hideNotification = () => {
    notification.value.show = false
  }

  return {
    notification,
    showNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    hideNotification
  }
} 