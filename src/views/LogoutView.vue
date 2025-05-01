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
    const response = await fetch('https://info3180-project-lof1.onrender.com/api/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`
      }
    });
    if (response.ok) {
      sessionStorage.removeItem('token');
      alert('Logout successful!');
      router.push('/login');
    } else {
      alert('Logout failed.');
    }
  } catch (error) {
    console.error(error);
    console.log('Token:', sessionStorage.getItem('token'));
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

  