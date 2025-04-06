<template>
    <div class="add-container">
      <h1>Login</h1>
      <LoginForm />
    </div>
</template>
  
<script>
    import LoginForm from '../components/LoginForm.vue';

    export default {
        name: 'LoginView',
        components: {
            LoginForm
        },
    };
</script>
  
<style scoped>
    .add-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    }
</style>