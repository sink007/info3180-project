<template>
    <div class="add-container">
      <h1>Register Account</h1>
      <RegisterForm />
    </div>
</template>
  
<script>
    import RegisterForm from '../components/RegisterForm.vue';

    export default {
    name: 'RegisterView',
    components: {
        RegisterForm
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