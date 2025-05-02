<template>
    <div class="container mt-4">
      <h2>Your Favourites</h2>
      <div v-if="loading">Loading favourites...</div>
      <div v-else>
        <div v-if="favourites.length" class="row">
          <div v-for="fav in favourites" :key="fav.id" class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ fav.name }}</h5>
                <p class="card-text">Username: {{ fav.username }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else>No favourites found.</div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  let favourites = ref([]);
  let loading = ref(true);
  
  onMounted(async () => {
    try {
      const response = await fetch(`/api/users/${sessionStorage.getItem('userId')}/favourites`);
      const data = await response.json();
      favourites.value = data;
    } catch (error) {
      console.error(error);
    } finally {
      loading.value = false;
    }
  });
  </script>