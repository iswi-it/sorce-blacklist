import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import AddEntryView from '../views/AddEntryView.vue';
import CheckEntriesView from '../views/CheckEntriesView.vue';
import RegistrationView from '../views/RegistrationView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      requiresAuth: true,
      title: 'Home',
    },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      title: 'Login',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: RegistrationView,
    meta: {
      title: 'Register',
    },
  },
  {
    path: '/check',
    name: 'check',
    component: CheckEntriesView,
    meta: {
      requiresAuth: true,
      title: 'Check Entries',
    },
  },
  {
    path: '/add',
    name: 'add',
    component: AddEntryView,
    meta: {
      requiresAuth: true,
      title: 'Add Entry',
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
  document.title = 'SOrCE-Blacklist - ' + to.meta.title;
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (localStorage.getItem('token')) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router;
