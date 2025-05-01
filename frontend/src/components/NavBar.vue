<template>
  <header v-if="isLoggedIn">
    <div class="px-3 py-2 text-bg-light border-bottom">
      <div class="container">
        <BNavbar toggleable="lg">
          <BNavbarBrand :to="{ name: 'home' }">
            <img alt="SOrCE Logo" src="../assets/sorce-logo.png" height="40" />
          </BNavbarBrand>
          <BNavbarToggle target="nav-collapse" href="/" />
          <BCollapse id="nav-collapse" is-nav>
            <BNavbarNav>
              <BNavItem :to="{ name: 'add' }" active-class="active"
                >Add Entry</BNavItem
              >
              <BNavItem :to="{ name: 'check' }" active-class="active"
                >Check Entry</BNavItem
              >
            </BNavbarNav>
            <BNavbarNav class="ms-auto mb-2 mb-lg-0">
              <div>
                <span class="me-3">Logged in as {{ getConferenceName }}</span>
                <a class="btn btn-outline-success" @click="logout">Logout</a>
              </div>
            </BNavbarNav>
          </BCollapse>
        </BNavbar>
      </div>
    </div>
  </header>
</template>

<script>
import {
  BNavbar,
  BNavbarBrand,
  BNavbarToggle,
  BCollapse,
  BNavbarNav,
  BNavItem,
} from 'bootstrap-vue-next';

export default {
  name: 'NavBar',
  components: {
    BNavbar,
    BNavbarBrand,
    BNavbarToggle,
    BCollapse,
    BNavbarNav,
    BNavItem,
  },
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    },
    getConferenceName: function () {
      return this.$store.getters.getConference;
    },
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logOut');
      this.$router.push('/login');
    },
  },
};
</script>
