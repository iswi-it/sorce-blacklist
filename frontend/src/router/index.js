import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import AddEntryView from '../views/AddEntryView.vue';
import CheckEntriesView from '../views/CheckEntriesView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/check',
    name: 'check',
    component: CheckEntriesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/add',
    name: 'add',
    component: AddEntryView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
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
