<template>
  <div class="container mt-4">
    <!-- SEARCH AND FILTER AREA -->
    <div class="search-filters mb-4">
      <input
        type="text"
        class="form-control mb-2"
        placeholder="Search profiles..."
        v-model="searchTerm"
      />
      <div class="filter-buttons mb-2">
        <button
          v-for="filter in ['Name', 'Birth', 'Sex', 'Race']"
          :key="filter"
          @click="selectedFilter = filter"
          :class="['filter-btn', { active: selectedFilter === filter }]"
        >
          {{ filter }}
        </button>
        <button v-if="searchTerm" class="clear-btn" @click="clearSearch">Clear</button>
      </div>
    </div>

    <!-- LATEST PROFILES AREA -->
    <h2 class="mt-5">Latest Profiles</h2>

    <div v-if="loading">Loading profiles...</div>
    <div v-else>
      <div v-if="profiles.length" class="row">
        <div v-for="profile in filteredProfiles" :key="profile.id" class="col-md-4 mb-4">
          <div class="profile-card">
            <img :src="profile.photo" alt="Profile Image" />

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
import { useRouter } from 'vue-router';

const profiles = ref([]);
const loading = ref(true);
const searchTerm = ref(sessionStorage.getItem("lastSearch") || '');
const selectedFilter = ref(null);
const router = useRouter();

onMounted(async () => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    const response = await fetch('/api/profiles', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      profiles.value = data;
    } else {
      console.error("Unauthorized or error fetching profiles");
      router.push("/login");
    }
  } catch (error) {
    console.error("Error fetching profiles:", error);
    router.push("/login");
  } finally {
    loading.value = false;
  }
});

const clearSearch = () => {
  searchTerm.value = '';
  sessionStorage.removeItem("lastSearch");
};

const filteredProfiles = computed(() => {
  const term = searchTerm.value.toLowerCase().trim();

  if (term) {
    sessionStorage.setItem("lastSearch", term);
  }

  const filtered = profiles.value.filter(profile => {
    if (!term) return true;

    switch (selectedFilter.value) {
      case 'Name':
        return profile.name.toLowerCase().includes(term);
      case 'Sex':
        return profile.sex?.trim().toLowerCase() === term;
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

  return term ? filtered : filtered.slice(0, 4);
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

.clear-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.clear-btn:hover {
  background-color: #495057;
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

.profile-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
