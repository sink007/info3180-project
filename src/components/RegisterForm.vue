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
import { ref } from 'vue';
import { useRouter } from 'vue-router'; 

const username = ref('');
const password = ref('');
const name = ref('');
const email = ref('');
const photo = ref(null);
const router = useRouter();

const handleFileUpload = (event) => {
    photo.value = event.target.files[0];
};

const registerUser = async () => {
    let form_data = new FormData();
    form_data.append('username', username.value);
    form_data.append('password', password.value);
    form_data.append('name', name.value);
    form_data.append('email', email.value);
    if (photo.value) {
    form_data.append('photo', photo.value);
    }

    console.log("Username:", username.value);
    console.log("Password:", password.value);
    console.log("Name:", name.value);
    console.log("Email:", email.value);
    console.log("Photo:", photo.value);

    try {
        let response = await fetch('/api/register', {
            method: 'POST',
            body: form_data,
        });

        let data = await response.json();
        if (response.ok) {
            alert(data.message);
            router.push({ name: 'home' });
        } else {
            alert("Registration failed.");
            console.log(data);
        }
    } catch (error) {
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
