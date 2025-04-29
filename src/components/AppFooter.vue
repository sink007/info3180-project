<template>
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; {{ year }} Jam-Date. Made with love for the realest Jamaicans 🇯🇲</p>
      </div>
    </footer>
  </template>
  
  <script setup>
  const year = new Date().getFullYear();
  </script>
  
  <style scoped>
  .footer {
    background-color: #111827;
    color: white;
    font-size: 0.85rem;
    text-align: center;
    padding: 12px 0;
    margin: 0;
    width: 100%;
  }
  
  .footer-content {
    width: 100%;
  }
  </style>