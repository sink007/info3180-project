<template>
  <div class="container mt-5">
    <!-- Header -->
    <div class="text-center mb-5">
      <h2>Matched Profiles</h2>
    </div>

    <!-- Match Cards -->
    <div v-if="loading" class="text-center">Loading matches...</div>

    <div v-else-if="matches.length > 0" class="row justify-content-center">
      <div
        class="col-md-4 mb-4"
        v-for="match in matches"
        :key="match.id"
      >
        <div class="card h-100 shadow-sm">
          <div class="card-body text-center">
            <h5 class="card-title">Potential Match</h5>
            <p class="mb-1"><strong>Birth Year:</strong> {{ match.birth_year }}</p>
            <p class="mb-1"><strong>Height:</strong> {{ match.height }} in</p>
            <p class="mb-1"><strong>Sex:</strong> {{ match.sex }}</p>
            <div class="d-flex justify-content-center gap-2 mt-2">
              <RouterLink :to="`/profiles/${match.id}`" class="btn btn-outline-primary">
                Show More Details
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Matches -->
    <div v-else class="text-center mt-5">
      <h5>No matches found for this profile.</h5>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const matches = ref([]);
const loading = ref(true);
const csrf_token = ref('');

function getCsrfToken() {
  fetch('https://info3180-project-lof1.onrender.com/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
}

async function loadMatches() {
  const profileId = route.params.id;

  try {
    const response = await fetch(`https://info3180-project-lof1.onrender.com/api/profiles/matches/${profileId}`, {
      method: 'GET',
      headers: {
        'X-CSRFToken': csrf_token.value
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (data) {
      matches.value = data;
    } else {
      console.warn("No matches:", data.message);
    }
  } catch (err) {
    console.error("Error fetching matched profiles:", err);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  getCsrfToken();
  loadMatches();
});
</script>

<style scoped>
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
  transform: scale(1.05);
}
</style>
