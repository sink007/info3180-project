<template>
  <div class="home-hero" :style="{ backgroundImage: `url(${backgroundImage})` }">
    <div class="overlay">
      <div class="glass-card">
        <h1 class="logo">Jam-Date</h1>
        <p class="tagline">Jamaica’s #1 place to meet real people. Safe. Simple. Vibes.</p>
        <div class="btn-row">
          <RouterLink to="/register" class="btn btn-primary">
            <i class="fas fa-user-plus"></i> Register
          </RouterLink>
          <RouterLink to="/login" class="btn btn-outline">
            <i class="fas fa-sign-in-alt"></i> Login
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import backgroundImage from '@/assets/site-background.jpg'
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}

.home-hero {
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.55);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  max-width: 500px;
  text-align: center;
  color: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(10px);
}

.logo {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 15px;
}

.tagline {
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.btn-row {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
}

.btn-primary {
  background-color: #00b894;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #019875;
}

.btn-outline {
  border: 2px solid #00b894;
  color: #00b894;
  background: transparent;
}

.btn-outline:hover {
  background: #00b894;
  color: white;
}
</style>


