<script setup>
import NavBar from './components/NavBar.vue'
import GlobalNotification from './components/GlobalNotification.vue'
</script>

<template>
  <div class="app">
    <!-- Navbar Component -->
    <NavBar />

    <!-- Router View - Dynamic Content Based on Route -->
    <router-view />
    
    <!-- Global Notification Component -->
    <GlobalNotification />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: #E8E7E7;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}
</style>
