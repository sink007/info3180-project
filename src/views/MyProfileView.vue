<template>
  <div class="container mt-5">
    <!-- Header -->
    <div class="text-center mb-5">
      <img :src="userPhoto" class="profile-pic mb-3" alt="Profile Picture" />
      <h2>{{ username }}'s Profiles</h2>
    </div>

    <!-- Profile Cards -->
    <div class="row justify-content-center">
      <div v-for="profile in profiles" :key="profile.id" class="col-md-4 mb-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body text-center">
            <h5 class="card-title">{{ profile.description }}</h5>
            <p><strong>Parish:</strong> {{ profile.parish }}</p>
            <p><strong>Race:</strong> {{ profile.race }}</p>
            <div class="d-flex justify-content-center gap-2 mt-2">
              <RouterLink :to="`/profiles/${profile.id}`" class="btn btn-outline-primary">Show More Details</RouterLink>
              <RouterLink :to="`/profiles/matches/${profile.id}`" class="btn btn-outline-success">Match Me</RouterLink>

            </div>
          </div>
        </div>
      </div>

      <!-- Add New Profile Cards -->
      <div v-for="n in 3 - profiles.length" :key="'create-' + n" class="col-md-4 mb-4">
        <div class="card h-100 d-flex align-items-center justify-content-center text-center">
          <button @click="router.push('/profiles/new')" class="square-add-btn">+</button>
        </div>
      </div>
    </div>
    <!-- Favourited Profiles Section -->
    <div class="mt-5" v-if="favourites.length">
      <h3 class="text-center mb-4">Profiles You Have Favourited</h3>
      <div class="row justify-content-center">
        <div v-for="profile in favourites" :key="profile.id" class="col-md-4 mb-4">
          <div class="card h-100 shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">{{ profile.description }}</h5>
              <p><strong>Parish:</strong> {{ profile.parish }}</p>
              <p><strong>Race:</strong> {{ profile.race }}</p>
              <RouterLink :to="`/profiles/${profile.id}`" class="btn btn-outline-primary">Show More Details</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const profiles = ref([]);
const username = ref('');
const userPhoto = ref('');
const router = useRouter();
const favourites = ref([]);

const goToMatches = (profileId) => {
  router.push('/matches');
};

onMounted(async () => {
  const userId = sessionStorage.getItem("userId");
  if (!userId) return router.push('/login');

  try {
    const userRes = await fetch(`/api/users/${userId}`);
    const user = await userRes.json();
    username.value = user.name;
    userPhoto.value = `/uploads/${user.photo}`;

    const response = await fetch(`/api/profiles`);
    const data = await response.json();
    profiles.value = data.filter(p => p.user_id === parseInt(userId));

    // Fetch favourited profiles
    const favRes = await fetch(`/api/users/${userId}/favourites`);
    const favData = await favRes.json();
    if (Array.isArray(favData)) {
      favourites.value = favData;
      console.log(favourites.value[0])
    }
  } catch (err) {
    console.error("Failed to load profiles or user info:", err);
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
