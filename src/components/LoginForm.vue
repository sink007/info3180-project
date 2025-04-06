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
    import { useRouter } from 'vue-router';  // This is for navigation after login.

    const username = ref('');
    const password = ref('');
    let csrf_token = ref('');
    const router = useRouter(); // For page redirection after login.

    // Fetch the CSRF token (if needed, can remove if not required)
    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        });
    }

    // Fetch CSRF token when component mounts
    onMounted(() => {
        getCsrfToken();
    });

    // Handle user login
    const loginUser = async () => {
        let loginForm = document.getElementById('loginForm');
        let form_data = new FormData(loginForm);
        form_data.append('username', username.value);
        form_data.append('password', password.value);

        try {
            let response = await fetch('/api/auth/login', {
                method: 'POST',
                body: form_data,
                headers: {
                'X-CSRFToken': csrf_token.value,
                },
            });

            if (response.ok) {
                let data = await response.json();
                router.push('/');
                console.log("Login successful");
            } else {
                let errorData = await response.json();
                console.error("Login failed:", errorData);
            }
        }
        catch (error) {
            console.error('Error:', error);
        }
    };
</script>

<style scoped>
    .container {
        max-width: 600px;
        margin: auto;
    }
</style>
