<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-success text-white text-center">
            <h4>Register</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" v-model="username" required minlength="3">
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email">
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required minlength="6">
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required>
              </div>
              <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                Register
              </button>
            </form>
            <p class="text-center mt-3">
              <router-link to="/login">Already have an account? Login</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match');
    return;
  }

  isLoading.value = true;
  try {
    const response = await fetch('/api/user/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        role: 'user'
      })
    });
    if (response.ok) {
      alert('Registration successful! Please login.');
      router.push('/login');
    } else {
      const error = await response.json();
      alert('Registration failed: ' + (error.detail || 'Unknown error'));
    }
  } catch (error) {
    alert('Registration failed');
  } finally {
    isLoading.value = false;
  }
};
</script>