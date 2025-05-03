<template>
  <div class="container mt-5">
    <!-- Header -->
    <div class="text-center mb-5">
      <h2>Matched Profiles</h2>
    </div>

    <!-- Match Cards -->
    <div v-if="loading" class="text-center">Loading matches...</div>

    <div v-else-if="matches.length > 0" class="row justify-content-center">
      <div class="col-md-4 mb-4" v-for="match in matches" :key="match.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body text-center">
            <div class="badge-match mb-2">💘 Matched</div>
            <h5 class="card-title">Potential Match</h5>
            <p><strong>Birth Year:</strong> {{ match.birth_year }}</p>
            <p><strong>Height:</strong> {{ match.height }} in</p>
            <p><strong>Sex:</strong> {{ match.sex }}</p>
            <p><strong>Match Score:</strong> {{ match.match_count }}/6</p>
            <RouterLink :to="`/profiles/${match.id}`" class="btn btn-outline-primary mt-2">
              Show More Details
            </RouterLink>
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

async function loadMatches() {
  const profileId = route.params.id;
  const token = sessionStorage.getItem("token");

  try {
    const response = await fetch(`/api/profiles/matches/${profileId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    if (Array.isArray(data)) {
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

.card {
  border: 2px solid #ffccd5;
  border-radius: 12px;
  background-color: #fff5f7;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}

.card:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 20px rgba(255, 192, 203, 0.4);
}

.card-title {
  font-weight: bold;
  color: #d6336c;
  font-size: 1.2rem;
}

.card-body p {
  margin: 0.3rem 0;
}

.btn-outline-primary {
  border-color: #d6336c;
  color: #d6336c;
}

.btn-outline-primary:hover {
  background-color: #d6336c;
  color: white;
}

.badge-match {
  background-color: #ffccd5;
  color: #b02a37;
  font-weight: 600;
  border-radius: 50px;
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
}
</style>
