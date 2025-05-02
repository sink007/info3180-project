<template>
  <header>
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    <nav class="navbar">
      <div class="container-fluid d-flex justify-content-between align-items-center w-100">
        
        <!-- Left: Jam Date logo -->
        <a class="navbar-brand handwritten" href="/">Jam Date</a>

        <!-- Right: Show Report + Logout if logged in -->
        <div class="d-flex align-items-center gap-3">
          <RouterLink v-if="isLoggedIn" to="/my-profile" class="nav-link">My Profile</RouterLink>
          <RouterLink to="/report" class="nav-link report-link">View Report</RouterLink>
          <button v-if="isLoggedIn" class="btn btn-link logout-btn" @click="logoutUser">Logout</button>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const isLoggedIn = ref(false);
const router = useRouter();

onMounted(() => {
  isLoggedIn.value = sessionStorage.getItem("loggedIn") === "true";
});

const logoutUser = async () => {
  try {
    const response = await fetch("/api/auth/logout", {
      method: "POST",
      credentials: "include" // Session-based auth remains intact
    });

    if (response.ok) {
      isLoggedIn.value = false;
      sessionStorage.removeItem("loggedIn");
      router.push("/login");
    } else {
      alert("Logout failed.");
    }
  } catch (error) {
    console.error("Logout error:", error);
  }
};
</script>

<style scoped>
.navbar {
  background-color: #111827; /* solid dark navy (tailwind vibes) */
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
