<template>
  <div class="container mt-4">
    <!-- SEARCH AND FILTER AREA -->
    <div class="search-filters mb-4">
      <input type="text" class="form-control mb-3" placeholder="Search profiles..." v-model="searchTerm" />
      <div class="filter-buttons">
        <button
          v-for="filter in ['Name', 'Birth', 'Sex', 'Race']"
          :key="filter"
          @click="selectedFilter = filter"
          :class="['filter-btn', { active: selectedFilter === filter }]"
        >
          {{ filter }}
        </button>
      </div>
    </div>

    <!-- LATEST PROFILES AREA -->
    <h2 class="mt-5">Latest Profiles</h2>

    <div v-if="loading">Loading profiles...</div>
    <div v-else>
      <div v-if="profiles.length" class="row">
        <div v-for="profile in filteredProfiles" :key="profile.id" class="col-md-4 mb-4">
          <div class="profile-card">
            <img :src="profile.photo" alt="Profile Image" class="bg-img" />

            <div class="overlay">
              <div class="text-block">
                <p class="name">{{ profile.name }}</p>
                <p class="parish">{{ profile.parish }}</p>
                <router-link :to="`/profiles/${profile.id}`" class="btn btn-light">View Profile</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>No profiles found.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const profiles = ref([]);
const loading = ref(true);
const searchTerm = ref('');
const selectedFilter = ref(null);
const csrfToken = ref('');

// Fetch CSRF token from the backend
const getCsrfToken = async () => {
  try {
    const response = await fetch('https://info3180-project-lof1.onrender.com/api/v1/csrf-token', { credentials: 'include' });
    const data = await response.json();
    csrfToken.value = data.csrf_token;
  } catch (error) {
    console.error('Failed to fetch CSRF token:', error);
  }
};

onMounted(async () => {
  await getCsrfToken();  // Fetch the CSRF token when the component is mounted
  await fetchProfiles();  // Fetch profiles after getting the CSRF token
});

// Fetch profiles with CSRF token included in the request headers
const fetchProfiles = async () => {
  try {
    const response = await fetch('https://info3180-project-lof1.onrender.com/api/profiles', {
      method: 'GET',
      headers: {
        'X-CSRFToken': csrfToken.value,  // Include CSRF token in the request headers
      },
      credentials: 'include',  // Include credentials (cookies) with the request
    });
    const data = await response.json();
    profiles.value = data;
  } catch (error) {
    console.error('Failed to fetch profiles:', error);
  } finally {
    loading.value = false;
  }
};

const filteredProfiles = computed(() => {
  const term = searchTerm.value.toLowerCase();

  const filtered = profiles.value.filter(profile => {
    if (!term) return true;

    switch (selectedFilter.value) {
      case 'Name':
        return profile.name.toLowerCase().includes(term);
      case 'Sex':
        return profile.sex?.trim().toLowerCase() === term.trim().toLowerCase();
      case 'Race':
        return profile.race && profile.race.toLowerCase().includes(term);
      case 'Birth':
        return profile.birth_year && profile.birth_year.toString().includes(term);
      default:
        return (
          profile.name.toLowerCase().includes(term) ||
          profile.parish.toLowerCase().includes(term)
        );
    }
  });

  // Limit to the 4 most recent profiles
  return filtered.slice(0, 4);
});
</script>

<style scoped>
.filter-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-right: 10px;
}

.filter-btn:hover {
  background-color: #0056b3;
}

.filter-btn.active {
  background-color: #333;
  color: #fff;
}

.card-img-top {
  object-fit: cover;
  height: 200px;
}

.profile-card {
  position: relative;
  width: 100%;
  height: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.55);
  padding: 12px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 100px;
}

.text-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.name {
  font-weight: 600;
  font-size: 1rem;
  margin: 0;
}

.parish {
  font-size: 0.85rem;
  margin: 0;
  color: #ccc;
}

.overlay .btn {
  padding: 5px 12px;
  font-size: 0.85rem;
  margin-top: 6px;
}
</style>
