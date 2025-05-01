<template>
    <div class="container mt-4">
        <form id="loginForm" @submit.prevent="loginUser">
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input v-model="username" type="text" name="username" class="form-control" required />
            </div>

            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input v-model="password" type="password" name="password" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const csrf_token = ref('');
const router = useRouter();

// Fetch CSRF token
function getCsrfToken() {
    fetch('https://info3180-project-lof1.onrender.com/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        });
}

// 🚀 CHECK LOGIN STATUS ON PAGE LOAD
onMounted(() => {
    getCsrfToken();
    
    // If already logged in, redirect to profiles
    const loggedIn = sessionStorage.getItem("loggedIn") === "true";
    if (loggedIn) {
        router.push('/profiles');
    }
});

// Handle login
const loginUser = async () => {
    try {
        const response = await fetch('https://info3180-project-lof1.onrender.com/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token.value,
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
            }),
        });

        if (response.ok) {
            const data = await response.json();

            sessionStorage.setItem("loggedIn", "true");
            sessionStorage.setItem("userId", data.id);

            window.location.href = "/profiles"; 
        } else {
            const errorData = await response.json();
            console.error("Login failed:", errorData);
            alert("Login failed. Please try again.");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred during login.");
    }
};

</script>

<style scoped>
.container {
    max-width: 600px;
    margin: auto;
}
</style>
