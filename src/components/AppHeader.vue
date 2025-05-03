<template>
  <header>
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    <nav class="navbar">
      <div class="container-fluid d-flex justify-content-between align-items-center w-100">

        <RouterLink class="navbar-brand handwritten" to="/">Jam Date</RouterLink>

        <div class="d-flex align-items-center gap-3">
          <RouterLink v-if="loggedIn" to="/my-profile" class="nav-link">My Profile</RouterLink>
          <RouterLink to="/report" class="nav-link report-link">View Report</RouterLink>
          <button v-if="loggedIn" class="btn btn-link logout-btn" @click="logoutUser">Logout</button>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter, useRoute } from "vue-router";
import { ref, onMounted, onUnmounted, watch } from "vue";

const loggedIn = ref(false);
const router = useRouter();
const route = useRoute();

function checkAuth() {
  loggedIn.value = sessionStorage.getItem("token") !== null;
}

onMounted(() => {
  checkAuth();
  window.addEventListener("storage", checkAuth);
});

watch(route, () => {
  checkAuth();
});

onUnmounted(() => {
  window.removeEventListener("storage", checkAuth);
});

const logoutUser = () => {
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("userId");
  loggedIn.value = false;
  router.push("/login");
};
</script>


<style scoped>
.navbar {
  background-color: #111827;
  color: white;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  padding: 12px 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.navbar-brand {
  font-size: 1.75rem;
  font-weight: 500;
  color: white;
  text-decoration: none;
}

.handwritten {
  font-family: 'Pacifico', cursive;
}

.nav-link {
  color: white;
  font-weight: 500;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.2s ease;
}

.report-link:hover {
  color: #00ffc8;
  text-decoration: underline;
}

.logout-btn {
  background: none;
  border: none;
  color: #ddd;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.95rem;
}
</style>
