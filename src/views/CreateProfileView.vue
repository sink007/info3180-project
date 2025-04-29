<template>
    <div class="container mt-4">
      <h2>Create Your Profile</h2>
      <form @submit.prevent="submitProfile" class="mb-4">
        <div class="form-group mb-3">
          <textarea v-model="description" class="form-control" placeholder="Short Description" required></textarea>
        </div>
        <div class="form-group mb-3">
          <input v-model="parish" class="form-control" placeholder="Parish" required />
        </div>
        <div class="form-group mb-3">
          <textarea v-model="biography" class="form-control" placeholder="Biography" required></textarea>
        </div>
        <div class="form-group mb-3">
          <select v-model="sex" class="form-control" required>
            <option value="">Select Sex</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>
        <div class="form-group mb-3">
          <input v-model="race" class="form-control" placeholder="Race" required />
        </div>
        <div class="form-group mb-3">
          <input v-model="birth_year" type="number" class="form-control" placeholder="Birth Year" required />
        </div>
        <div class="form-group mb-3">
          <input v-model="height" type="number" step="0.1" class="form-control" placeholder="Height (inches)" required />
        </div>
        <div class="form-group mb-3">
          <input v-model="fav_cuisine" class="form-control" placeholder="Favorite Cuisine" required />
        </div>
        <div class="form-group mb-3">
          <input v-model="fav_colour" class="form-control" placeholder="Favorite Colour" required />
        </div>
        <div class="form-group mb-3">
          <input v-model="fav_school_subject" class="form-control" placeholder="Favorite School Subject" required />
        </div>
        <div class="form-check mb-2">
          <input type="checkbox" v-model="political" class="form-check-input" />
          <label class="form-check-label">Political</label>
        </div>
        <div class="form-check mb-2">
          <input type="checkbox" v-model="religious" class="form-check-input" />
          <label class="form-check-label">Religious</label>
        </div>
        <div class="form-check mb-2">
          <input type="checkbox" v-model="family_oriented" class="form-check-input" />
          <label class="form-check-label">Family Oriented</label>
        </div>
  
        <button type="submit" class="btn btn-primary mt-3">Create Profile</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const description = ref('');
  const parish = ref('');
  const biography = ref('');
  const sex = ref('');
  const race = ref('');
  const birth_year = ref('');
  const height = ref('');
  const fav_cuisine = ref('');
  const fav_colour = ref('');
  const fav_school_subject = ref('');
  const political = ref(false);
  const religious = ref(false);
  const family_oriented = ref(false);
  const router = useRouter();
  
  async function submitProfile() {
  try {
    const csrfToken = await fetch('/api/v1/csrf-token')
      .then(response => response.json())
      .then(data => data.csrf_token);

    const response = await fetch('/api/profiles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        description: description.value,
        parish: parish.value,
        biography: biography.value,
        sex: sex.value,
        race: race.value,
        birth_year: birth_year.value,
        height: height.value,
        fav_cuisine: fav_cuisine.value,
        fav_colour: fav_colour.value,
        fav_school_subject: fav_school_subject.value,
        political: political.value,
        religious: religious.value,
        family_oriented: family_oriented.value
      })
    });

    const data = await response.json();
    if (response.ok) {
      alert(data.message);
      router.push('/profiles'); 
    } else {
      console.error('Error creating profile:', data);
      alert('Failed to create profile.');
    }
  } catch (error) {
    console.error('Error creating profile:', error);
  }
}
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: auto;
  }
  </style>