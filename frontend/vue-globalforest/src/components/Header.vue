<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">{{ title }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav me-auto">
                <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
                <!-- <router-link class="nav-link" to="/create-forest">Create Forest</router-link>
                <router-link class="nav-link" to="/cases">Forest</router-link> -->
                <router-link v-if="isAdmin" class="nav-link" to="/admin">Admin</router-link>
            </div>
            <div class="navbar-nav">
                <button v-if="isLoggedIn" @click="handleLogout" class="btn btn-outline-light me-2">Logout</button>
                <router-link v-if="!isLoggedIn" class="nav-link" to="/register">Register</router-link>
                <router-link v-if="!isLoggedIn" class="nav-link" to="/login">Login</router-link>
            </div>
        </div>
        </div>
    </nav>
</template>

<script setup>
    const props = defineProps({   
        title: {
            type: String,
            required: true
        }
    });

    import { isLoggedIn, isAdmin, logout } from '../composables/useAuth.js';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    const handleLogout = () => {
      logout();
      router.push('/');
    };
</script>