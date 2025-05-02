<script setup>
import { RouterLink, useRouter } from "vue-router";
import { ref, onMounted, onBeforeUnmount } from "vue";

const isLoggedIn = ref(false);
const router = useRouter();

const checkLoginStatus = () => {
  isLoggedIn.value = sessionStorage.getItem("token") !== null;
};

onMounted(() => {
  checkLoginStatus();
  window.addEventListener("storage", checkLoginStatus);
});

onBeforeUnmount(() => {
  window.removeEventListener("storage", checkLoginStatus);
});

const logoutUser = async () => {
  try {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("userId");
    isLoggedIn.value = false;
    router.push("/login");
  } catch (error) {
    console.error("Logout error:", error);
  }
};
</script>

<style scoped>
.navbar {
  background-color: #111827; /* dark navy */
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
  transition: color 0.2s ease;
}

.navbar-brand:hover {
  color: #00ffc8;
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

.nav-link:hover {
  color: #00ffc8;
  text-decoration: underline;
}

.report-link {
  margin-right: 10px;
}

.logout-btn {
  background: none;
  border: none;
  color: #ddd;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.logout-btn:hover {
  color: #ff5e5e;
  text-decoration: underline;
}
</style>
