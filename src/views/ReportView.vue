<template>
  <div class="container mt-4" style="max-width: 900px;">
    <h3 class="mb-4 text-center">Top Favourited Profiles</h3>

    <div class="mb-4 text-center">
      <label for="topNInput" class="form-label">Enter number of top profiles to fetch:</label>
      <input 
        id="topNInput"
        v-model.number="topN"
        type="number" 
        min="1" 
        class="form-control d-inline-block w-auto mx-2" 
      />
      <button class="btn btn-success" @click="fetchTopProfiles">Search</button>
    </div>

    <div v-if="loading" class="text-center">Loading top profiles...</div>

    <div v-else-if="profiles.length > 0" class="row">
      <div 
        v-for="(profile, index) in profiles" 
        :key="profile.id" 
        class="col-md-6 mb-4 d-flex align-items-stretch"
      >
        <div class="card shadow-sm profile-card w-100">
          <div class="card-body text-center">
            <div :class="['rank-label', getRankClass(index)]" class="mb-3">#{{ index + 1 }}</div>
            <img 
              :src="`/uploads/${profile.photo}`" 
              alt="Profile Photo" 
              class="profile-pic mb-3" 
            />
            <h5 class="card-title">{{ profile.name }}</h5>
            <p class="mb-1"><strong>Parish:</strong> {{ profile.parish }}</p>
            <p class="mb-2"><strong>Favourited:</strong> {{ profile.fav_count }} time(s)</p>
            <div class="text-center">
              <router-link :to="`/profiles/${profile.id}`" class="btn btn-outline-primary">Show More Details</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <p class="text-center">No top profiles found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const topN = ref("");
const loading = ref(false);
const profiles = ref([]);

async function fetchTopProfiles() {
  if (topN.value < 1) {
    alert("Please enter a number greater than 0.");
    return;
  }

  loading.value = true;
  try {
    const response = await fetch(`/api/users/favourites/${topN.value}`);
    profiles.value = await response.json();
  } catch (error) {
    console.error("Failed to load top favourites:", error);
  } finally {
    loading.value = false;
  }
}

function getRankClass(index) {
  if (index === 0) return 'gold';
  if (index === 1) return 'silver';
  if (index === 2) return 'bronze';
  return 'gray';
}
</script>

<style scoped>
.profile-card {
  border-radius: 15px;
  padding: 1.5rem;
  transition: transform 0.2s ease;
}

.profile-card:hover {
  transform: scale(1.02);
}

.profile-pic {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  object-fit: cover;
  border: 5px solid #007bff;
}

.rank-label {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  display: inline-block;
  margin-right: 20px; 
}

.rank-label.gold {
  background-color: #ffd700; 
}

.rank-label.silver {
  background-color: #c0c0c0; 
}

.rank-label.bronze {
  background-color: #cd7f32; 
}

.rank-label.gray {
  background-color: #808080;
}

.square-add-btn {
  width: 60px;
  height: 60px;
  font-size: 2rem;
  border: 2px solid #007bff;
  border-radius: 12px;
  background-color: transparent;
  color: #007bff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.square-add-btn:hover {
  background-color: #007bff;
  color: white;
}
</style>
