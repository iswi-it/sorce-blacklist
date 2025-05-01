import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from 'vue';
import { createBootstrap } from 'bootstrap-vue-next';
import axios from 'axios';

import App from './App.vue';
import router from './router';
import store from './store';

// default axios settings
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';

// Automatically add Authorization header if token exists
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// automatically logout when token expired
axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    console.log(originalRequest);
    if (
      error.response.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url != 'token'
    ) {
      originalRequest._retry = true;
      store.dispatch('logOut');
      router.push('/login');
    }
    return Promise.reject(error);
  }
});

// setup vue app
const app = createApp(App);
app.use(router);
app.use(store);
app.use(createBootstrap());
app.mount('#app');
