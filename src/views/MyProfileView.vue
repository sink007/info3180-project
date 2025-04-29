<template>
    <div class="container mt-5">
      <!-- Header: Profile Picture + Username -->
      <div class="text-center mb-5">
        <img :src="userPhoto" class="profile-pic mb-3" alt="Profile Picture" />
        <h2>{{ username }}'s Profiles</h2>
    </div>
  
      <!-- Profile Cards -->
      <div class="row justify-content-center">
        <!-- Existing Profiles -->
        <div v-for="profile in profiles" :key="profile.id" class="col-md-4 mb-4">
          <div class="card h-100 shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">{{ profile.description }}</h5>
              <p><strong>Parish:</strong> {{ profile.parish }}</p>
              <p><strong>Race:</strong> {{ profile.race }}</p>
              <RouterLink :to="`/profiles/${profile.id}`" class="btn btn-outline-primary mt-2">Show More Details</RouterLink>
            </div>
          </div>
        </div>
  
        <!-- Blank Create Profile Cards -->
        <div
          v-for="n in 3 - profiles.length"
          :key="'create-' + n"
          class="col-md-4 mb-4"
        >
        <div class="card h-100 d-flex align-items-center justify-content-center text-center">
            <button @click="router.push('/profiles/new')" class="square-add-btn">+</button>
        </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const profiles = ref([]);
  const loading = ref(true);
  const username = ref('');
  const userPhoto = ref('');
  const router = useRouter();
  
  onMounted(async () => {
    const userId = sessionStorage.getItem("userId");
  
    if (!userId) {
      router.push('/login');
      return;
    }
  
    try {
      // 🔥 1. Fetch user details
      const userRes = await fetch(`/api/users/${userId}`);
      const user = await userRes.json();
      username.value = user.name;
      userPhoto.value = `/uploads/${user.photo}`;
  
      // 🔥 2. Fetch user profiles
      const response = await fetch(`/api/profiles`);
      const data = await response.json();
      profiles.value = data.filter(p => p.user_id === parseInt(userId));
  
    } catch (err) {
      console.error("Failed to load profile or user info:", err);
    } finally {
      loading.value = false;
    }
  });
  </script>
  
  <style scoped>
    .profile-pic {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    object-fit: cover;
    border: 5px solid #007bff;
    }
  
    .square-add-btn {
  width: 60px;
  height: 60px;
  font-size: 2rem;
  border: 2px solid #007bff;
  border-radius: 12px;
  background-color: transparent; /* Cleaner than 'none' */
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