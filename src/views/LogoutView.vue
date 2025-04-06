<template>
    <div class="container mt-5 text-center">
      <p>Logging you out...</p>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  onMounted(async () => {
    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST',
        });
        sessionStorage.removeItem('loggedIn');
        router.push('/login');
    } catch (err) {
      console.error('Logout error:', err);
    }
  });
  </script>
  
  <style scoped>
  .container {
    margin-top: 100px;
  }
  </style>
  