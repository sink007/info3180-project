<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">VueJS with Flask</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button class="nav-link btn btn-link text-white" @click="logoutUser">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { ref, onMounted } from "vue";

// Global login state (you might want to use a proper store like Pinia for larger apps)
const isLoggedIn = ref(false);
const router = useRouter();

// Check if user is logged in on mount (basic check)
onMounted(() => {
  isLoggedIn.value = sessionStorage.getItem("loggedIn") === "true";
});

// Handle logout
const logoutUser = async () => {
  try {
    const response = await fetch("/api/auth/logout", {
      method: "POST",
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
.navbar .btn-link {
  padding: 0;
  border: none;
  cursor: pointer;
}
</style>
