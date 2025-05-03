<template>
    <div class="overlay" v-if="show">
      <div class="overlay-content">
        <h3>You need to create an account or log in to access profiles.</h3>
        <p>
          <RouterLink to="/register">Register</RouterLink> or 
          <RouterLink to="/login">Login</RouterLink> to continue.
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps(['show']);
  </script>
  
  <style scoped>
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    backdrop-filter: blur(5px);
    background-color: rgba(0, 0, 0, 0.6);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .overlay-content {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  }
  
  .overlay-content a {
    color: #0d6efd;
    text-decoration: underline;
    font-weight: bold;
  }
  </style>