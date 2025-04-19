<template>
    <header>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">SOrCE-Blacklist</a>
            </div>
            <div v-if="isLoggedIn">
                Logged in as {{ getConferenceName }}
                <a class="btn btn-outline-success" @click="logout">Logout</a>
            </div>
            
        </nav>
    </header>
</template>

<script>

export default {
    name: 'NavBar',
    computed: {
        isLoggedIn: function () {
            return this.$store.getters.isAuthenticated;
        },
        getConferenceName: function() {
            return this.$store.getters.getConference;
        }
    },
    methods: {
        async logout () {
            await this.$store.dispatch('logOut');
            this.$router.push('/login');
        }
  },
}

</script>