<template>
  <div class="row justify-content-center align-items-center">
    <div class="col-md-4 col-sm-8">
      <BAlert v-model="error.countdown" variant="danger" dismissible fade>
        {{ error.message }}
      </BAlert>

      <img
        alt="SOrCE Logo"
        src="../assets/sorce-logo.png"
        height="100"
        class="mb-4"
      />
      <form @submit.prevent="submit">
        <div class="form-floating mb-3">
          <input
            id="username"
            type="text"
            name="username"
            v-model="form.username"
            placeholder="username"
            class="form-control"
          />
          <label for="username">Username</label>
        </div>
        <div class="form-floating mb-3">
          <input
            id="password"
            type="password"
            name="password"
            v-model="form.password"
            placeholder="password"
            class="form-control"
          />
          <label for="password">Password</label>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { BAlert } from 'bootstrap-vue-next';
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'LoginView',
  components: {
    BAlert,
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      error: {
        message: '',
        countdown: 0,
      },
    };
  },
  methods: {
    ...mapActions(['logIn']),
    async submit() {
      const User = new FormData();
      User.append('username', this.form.username);
      User.append('password', this.form.password);
      this.logIn(User)
        .then(() => {
          this.$router.push('/');
        })
        .catch((error) => {
          this.error.countdown = 10 * 1000;
          this.error.message = error;
        });
    },
  },
});
</script>
