<template>
    <div class="container mt-4">
        <form id="registerForm" @submit.prevent="registerUser">
        <div class="form-group mb-3">
            <label for="username" class="form-label">Username</label>
            <input v-model="username" type="text" name="username" class="form-control" required />
        </div>

        <div class="form-group mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="password" type="password" name="password" class="form-control" required />
        </div>

        <div class="form-group mb-3">
            <label for="name" class="form-label">Full Name</label>
            <input v-model="name" type="text" name="name" class="form-control" required />
        </div>

        <div class="form-group mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="email" type="email" name="email" class="form-control" required />
        </div>

        <div class="form-group mb-3">
            <label for="photo" class="form-label">Profile Photo</label>
            <input type="file" @change="handleFileUpload" class="form-control" />
        </div>

        <button type="submit" class="btn btn-primary">Register</button>
        </form>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router'; 
    const username = ref('');
    const password = ref('');
    const name = ref('');
    const email = ref('');
    const photo = ref(null);
    let csrf_token = ref('');
    const router = useRouter();

    function getCsrfToken() {
        fetch('https://info3180-project-lof1.onrender.com/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            console.log("csrf work");
            csrf_token.value = data.csrf_token;
        });
    }

    onMounted(() => {
        getCsrfToken();
    });

    const handleFileUpload = (event) => {
        photo.value = event.target.files[0];
    };

    const registerUser = async () => {
    let registerForm = document.getElementById('registerForm');
    let form_data = new FormData(registerForm);
    form_data.append('username', username.value);
    form_data.append('password', password.value);
    form_data.append('name', name.value);
    form_data.append('email', email.value);
    form_data.append('photo', photo.value);

    try {
        const response = await fetch('https://info3180-project-lof1.onrender.com/api/register', {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value,
            },
            credentials: 'include' // <-- This is crucial
        });

        const text = await response.text();  // Don't try to parse as JSON yet
        console.log("Raw server response:", text);

        if (response.ok) {
            const data = JSON.parse(text);  // Now parse JSON safely
            alert(data.message);
            router.push({ name: 'home' });
        } else {
            console.error("Server returned an error:", text);
            alert("Registration failed. See console for details.");
        }
    } catch (error) {
        console.log("Request failed:");
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
