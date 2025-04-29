<template>
    <div class="container mt-4">
      <h2>Matches</h2>
      <div v-if="loading">Loading matches...</div>
      <div v-else>
        <div v-if="matches.length" class="row">
          <div v-for="match in matches" :key="match.id" class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Match: {{ match.user_id }}</h5>
                <p class="card-text">Birth Year: {{ match.birth_year }}</p>
                <p class="card-text">Height: {{ match.height }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else>No matches found.</div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  let matches = ref([]);
  let loading = ref(true);
  
  onMounted(async () => {
    try {
      const response = await fetch(`/api/profiles/matches/${sessionStorage.getItem('profileId')}`);
      const data = await response.json();
      matches.value = data;
    } catch (error) {
      console.error(error);
    } finally {
      loading.value = false;
    }
  });
  </script>