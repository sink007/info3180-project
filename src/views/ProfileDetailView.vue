<template>
  <div class="container mt-4" style="max-width: 800px;">
    <div v-if="loading">Loading profile...</div>

    <div v-else-if="profile" class="card shadow p-4" style="border-radius: 15px;">
      <div class="text-center mb-3">
        <img
          :src="getProfilePhoto(profile?.photo)"
          @error="onImageError"
          class="profile-pic mb-3"
          alt="Profile Photo"
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

      <div class="row text-center mt-3">
        <div class="col-md-6">
          <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
          <p><strong>Favourite School Subject:</strong> {{ profile.fav_school_subject }}</p>
        </div>
        <div class="col-md-6">
          <p><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
          <p><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
          <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
        </div>
      </div>

      <p class="text-center mt-3">
        <strong>Favourited:</strong> {{ profile.fav_count }} time(s) 
      </p>

      <div class="d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-primary" @click="emailUser">Email User</button>
        <button 
          class="btn" 
          :class="isFavourited ? 'text-danger' : 'text-muted'" 
          @click="addToFavourites"
          style="font-size: 2rem;"
        >
          <i class="fa" :class="isFavourited ? 'fa-heart' : 'fa-heart'"></i>
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
let isFavourited = ref(false);

onMounted(async () => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("You need to log in to view this profile.");
    return;
  }

  try {
    const response = await fetch(`/api/profiles/${route.params.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Profile fetch failed.");
    }

    profile.value = await response.json();

    const favResponse = await fetch(`/api/profiles/${profile.value.id}/is-favourited`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const favData = await favResponse.json();
    isFavourited.value = favData.isFavourited === true;

  } catch (error) {
    console.error("Error loading profile:", error);
    alert("Failed to load profile. Try logging in again.");
  } finally {
    loading.value = false;
  }
});

async function addToFavourites() {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Token is missing!");
    return;
  }

  try {
    const response = await fetch(`/api/profiles/${profile.value.id}/favourite`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
    });
    const data = await response.json();
    alert(data.message);
    if (data.message === "User added to favourites.") {
      isFavourited.value = true;
      profile.value.fav_count += 1;
    }
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


function getProfilePhoto(filename) {
  if (!filename) return '/uploads/default-user.png';
  return `/uploads/${filename}`;
}


function onImageError(e) {
  e.target.src = '/uploads/default-user.png';
}

</script>


<style scoped>

img.profile-pic {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ccc;
}

  @import url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css);
</style>
