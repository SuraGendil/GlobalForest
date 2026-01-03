import { createRouter, createWebHistory } from 'vue-router';
import ForestList from './components/ForestList.vue';
import AddForest from './components/AddForest.vue';
import EditForest from './components/EditForest.vue';

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
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;