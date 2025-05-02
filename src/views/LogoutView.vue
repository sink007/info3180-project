<template>
  <div class="container mt-5 text-center">
    <p>Logging you out...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

async function logout() {
  try {
    const response = await fetch('/api/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      credentials: 'include'
    });

    if (response.ok) {
      localStorage.removeItem('token');
      sessionStorage.removeItem('loggedIn');
      sessionStorage.removeItem('userId');
      alert('Logout successful!');
      router.push('/login');
    } else {
      alert('Logout failed.');
    }
  } catch (error) {
    console.error(error);
    alert('Logout failed.');
  }
}

onMounted(() => {
  logout();
});
</script>

<style scoped>
.container {
  margin-top: 100px;
}
</style>

  
