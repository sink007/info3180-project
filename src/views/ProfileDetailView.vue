<template>
  <div class="container mt-4" style="max-width: 800px;">
    <div v-if="loading">Loading profile...</div>

    <div v-else-if="profile" class="card shadow p-4" style="border-radius: 15px;">
      <div class="text-center mb-3">
        <img 
          :src="`/uploads/${profile.photo}`" 
          alt="Profile Photo" 
          class="img-fluid mb-3" 
          style="max-width: 150px; border-radius: 25%;" 
        />
        <h4 class="mt-2">{{ profile.name }}</h4>
      </div>

      <p class="lead text-center" style="font-size: 1rem;">{{ profile.biography }}</p>

      <div class="row text-center mt-4">
        <div class="col-md-6">
          <p><strong>Sex:</strong> {{ profile.sex }}</p>
          <p><strong>Race:</strong> {{ profile.race }}</p>
          <p><strong>Height:</strong> {{ profile.height }} inches</p>
        </div>
        <div class="col-md-6">
          <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
          <p><strong>Parish:</strong> {{ profile.parish }}</p>
          <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
        </div>
      </div>

      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-primary" @click="emailUser">Email User</button>
        <button 
          class="btn" 
          :class="isFavourited ? 'btn-warning' : 'btn-success'" 
          @click="addToFavourites"
        >
          {{ isFavourited ? 'Favourited' : 'Favourite' }}
        </button>
      </div>
    </div>

    <div v-else>
      <p>Profile not found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
let profile = ref(null);
let loading = ref(true);
let isFavourited = ref(false);  // new

onMounted(async () => {
  try {
    const response = await fetch(`/api/profiles/${route.params.id}`);
    profile.value = await response.json();
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
});

async function addToFavourites() {
  try {
    const response = await fetch(`/api/profiles/${route.params.id}/favourite`, {
      method: 'POST'
    });
    const data = await response.json();
    alert(data.message);
    isFavourited.value = true; // button changes color after click
  } catch (error) {
    console.error(error);
  }
}

function emailUser() {
  if (profile.value && profile.value.email) {
    window.location.href = `mailto:${profile.value.email}`;
  } else {
    alert("Email not available for this user.");
  }
}
</script>