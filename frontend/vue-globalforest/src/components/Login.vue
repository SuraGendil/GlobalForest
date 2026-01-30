<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white text-center">
            <h4>Login</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Username or Email</label>
                <input type="text" class="form-control" id="username" v-model="username" placeholder="Enter username or email" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
            <p class="text-center mt-3">
              <small>Demo: username "admin" or email (if registered), password "admin"</small><br>
              <router-link to="/register">Don't have an account? Register</router-link>
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
import { login } from '../composables/useAuth.js';

const router = useRouter();
const username = ref('');
const password = ref('');

const handleLogin = async () => {
  try {
    const response = await fetch('/api/user/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: username.value, password: password.value })
    });
    if (response.ok) {
      const data = await response.json();
      login(data.user);
      alert('Login successful!');
      router.push('/');
    } else {
      alert('Invalid credentials');
    }
  } catch (error) {
    alert('Login failed');
  }
};
</script>