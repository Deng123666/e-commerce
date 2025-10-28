<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  // Check if user is logged in on app mount
  authStore.checkAuth()
})
</script>

<style scoped>
#app {
  width: 100%;
  min-height: 100vh;
}
</style>

