import { ref } from 'vue'

export function useLoading() {
  const isLoading = ref(false)
  const loadingText = ref('Carregando...')

  const startLoading = (text = 'Carregando...') => {
    isLoading.value = true
    loadingText.value = text
  }

  const stopLoading = () => {
    isLoading.value = false
  }

  const withLoading = async (asyncFunction, text = 'Carregando...') => {
    startLoading(text)
    try {
      const result = await asyncFunction()
      return result
    } finally {
      stopLoading()
    }
  }

  return {
    isLoading,
    loadingText,
    startLoading,
    stopLoading,
    withLoading
  }
} 