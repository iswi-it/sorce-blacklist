<template>
  <div id="app">
    <NavBar />
    <div class="main container">
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  components: {
    NavBar,
  },
  beforeCreate() {
    // always get current user when a token exists
    if (localStorage.getItem('token')) {
      this.$store.dispatch('viewMe');
    }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.main {
  padding-top: 4em;
}
</style>
