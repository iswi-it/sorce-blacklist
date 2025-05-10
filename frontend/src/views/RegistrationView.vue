<template>
  <div class="row justify-content-center align-items-center">
    <div class="col-md-4 col-sm-8">
      <BAlert v-model="error.countdown" variant="danger" dismissible fade>
        {{ error.message }}
      </BAlert>

      <BAlert v-model="success.countdown" variant="success" dismissible fade>
        {{ success.message }}
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
            id="registration_secret"
            type="password"
            name="registration_secret"
            v-model="form.registration_secret"
            placeholder="registration secret"
            class="form-control"
            required="true"
          />
          <label for="registration_secret">Registration Secret</label>
        </div>
        <div class="form-floating mb-3">
          <input
            id="username"
            type="text"
            name="username"
            v-model="form.username"
            placeholder="username"
            class="form-control"
            required="true"
          />
          <label for="username">Username</label>
        </div>
        <div class="form-floating mb-3">
          <input
            id="conference"
            type="text"
            name="conference"
            v-model="form.conference"
            placeholder="conference"
            class="form-control"
            required="true"
          />
          <label for="conference">Conference</label>
        </div>
        <div class="form-floating mb-3">
          <input
            id="password"
            type="password"
            name="password"
            v-model="form.password"
            placeholder="password"
            class="form-control"
            required="true"
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
import axios from 'axios';

export default defineComponent({
  name: 'LoginView',
  components: {
    BAlert,
  },
  data() {
    return {
      form: {
        registration_secret: '',
        username: '',
        conference: '',
        password: '',
      },
      error: {
        message: '',
        countdown: 0,
      },
      success: {
        message: '',
        countdown: 0,
      },
    };
  },
  methods: {
    submit() {
      const request = this.form;
      axios
        .post('users', request)
        .then((response) => {
          if (response.status === 200) {
            this.success.countdown = 30 * 1000;
            this.success.message = `User with username "${response.data.username}" for the conference "${response.data.conference}" was successfully created!`;
            this.form = {
              registration_secret: '',
              username: '',
              conference: '',
              password: '',
            };
          } else {
            this.error.countdown = 10 * 1000;
            this.error.message = 'Something went wrong!';
          }
        })
        .catch((error) => {
          // user login failed -> show error
          this.error.countdown = 10 * 1000;
          if (error.response.data.detail)
            this.error.message = error.response.data.detail;
          else this.error.message = 'Something went wrong!';
        });
    },
  },
});
</script>
