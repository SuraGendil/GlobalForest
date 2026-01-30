import { ref, computed } from 'vue';

const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
const isLoggedIn = computed(() => !!user.value);
const isAdmin = computed(() => user.value?.role === 'admin');

const login = (userData) => {
  user.value = userData;
  localStorage.setItem('user', JSON.stringify(userData));
};

const logout = () => {
  user.value = null;
  localStorage.removeItem('user');
};

export { user, isLoggedIn, isAdmin, login, logout };