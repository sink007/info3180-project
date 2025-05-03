<template>
  <div class="container mt-5">
    <div class="text-center mb-5">
      <img :src="userPhoto" class="profile-pic mb-3" alt="Profile Picture" />
      <h2>{{ username }}'s Profiles</h2>
    </div>

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

      <div v-if="profiles.length < 3" class="col-md-4 mb-4">
        <div class="card h-100 d-flex align-items-center justify-content-center text-center">
          <button @click="router.push('/profiles/new')" class="square-add-btn">+</button>
        </div>
      </div>
    </div>

    <div class="mt-5" v-if="favourites.length">
      <h3 class="text-center mb-4 text-danger">Profiles You Have Favourited</h3>
      <div class="row justify-content-center">
        <div v-for="profile in favourites" :key="'fav-' + profile.id" class="col-md-4 mb-4">
          <div class="card fav-card h-100 text-center p-3">
          <img 
            :src="`/uploads/${profile.photo}`" 
            alt="Profile Photo" 
            class="fav-profile-pic mx-auto mb-3"
          />
          <h5 class="fw-bold">{{ profile.name }}</h5>
          <RouterLink :to="`/profiles/${profile.id}`" class="btn btn-outline-danger mt-2">View Profile</RouterLink>
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

onMounted(async () => {
  const userId = sessionStorage.getItem("userId");
  if (!userId) return router.push('/login');

  try {
    const userRes = await fetch(`/api/users/${userId}`);
    const user = await userRes.json();
    username.value = user.name;
    userPhoto.value = `/uploads/${user.photo}`;

    const res = await fetch(`/api/profiles`, {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem("token")}`
      }
    });
    const data = await res.json();
    profiles.value = Array.isArray(data)
      ? data.filter(p => p.user_id === parseInt(userId))
      : [];

    const favRes = await fetch(`/api/users/${userId}/favourites`);
    const favData = await favRes.json();
    favourites.value = Array.isArray(favData) ? favData : [];
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

.fav-card {
  border: 2px dashed #dc3545;
  background-color: #fff0f3;
  border-radius: 10px;
  transition: transform 0.2s ease-in-out;
}

.fav-card:hover {
  transform: scale(1.02);
  background-color: #ffe6ea;
}

.fav-card .card-body {
  padding: 1.5rem;
}

.fav-card .btn {
  border-color: #dc3545;
  color: #dc3545;
}

.fav-card .btn:hover {
  background-color: #dc3545;
  color: white;
}

.fav-profile-pic {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #dc3545;
  box-shadow: 0 0 10px rgba(220, 53, 69, 0.3);
}
</style>
