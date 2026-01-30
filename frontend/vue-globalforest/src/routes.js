import { createRouter, createWebHistory } from 'vue-router';
import ForestList from './components/ForestList.vue';
import AddForest from './components/AddForest.vue';
import EditForest from './components/EditForest.vue';
import Admin from './components/Admin.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import { isLoggedIn, isAdmin } from './composables/useAuth.js';

const routes = [
    {
        name: 'ForestList',
        path: '/',
        component: ForestList
    },
    {
        name: 'AddForest',
        path: '/create-forest',
        component: AddForest
    },
    {
        name: 'EditForest',
        path: '/edit-forest/:id',
        component: EditForest
    },
    {
        name: 'Admin',
        path: '/admin',
        component: Admin,
        beforeEnter: (to, from, next) => {
            if (isLoggedIn.value && isAdmin.value) {
                next();
            } else {
                next('/');
            }
        }
    },
    {
        name: 'Login',
        path: '/login',
        component: Login
    },
    {
        name: 'Register',
        path: '/register',
        component: Register
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;