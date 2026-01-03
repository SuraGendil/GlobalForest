<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">{{ title }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
                <router-link class="nav-link" to="/create-forest">Create Forest</router-link>
                <router-link class="nav-link" to="/forest">Forest</router-link>
                <a class="nav-link" href="#">Content 1</a>
                <a class="nav-link" href="#">Content 3</a>
                <a class="nav-link" href="#">Content 4</a>
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
</script>