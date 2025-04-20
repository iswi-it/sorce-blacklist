<template>
  <section>
    <BAlert v-model="success_countdown" variant="success" dismissible fade>
      Entry was successfully added to SOrCE-Blacklist!
    </BAlert>
    <BAlert v-model="error_countdown" variant="danger" dismissible fade>
      Entry was successfully added to SOrCE-Blacklist!
    </BAlert>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="name" class="form-label">Name:</label>
        <input
          type="text"
          name="name"
          v-model="form.name"
          class="form-control"
          required="true"
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">E-Mail:</label>
        <input
          type="text"
          name="email"
          v-model="form.email"
          class="form-control"
          required="true"
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Nationality:</label>
        <input
          type="text"
          name="email"
          v-model="form.nationality"
          class="form-control"
          required="true"
        />
      </div>
      <div class="mb-3">
        <label for="birtdate" class="form-label">Birthdate:</label>
        <VueDatePicker
          v-model="form.birthdate"
          name="birthdate"
          :enable-time-picker="false"
          model-type="dd/MM/yyyy"
          format="dd/MM/yyyy"
        />
      </div>
      <div class="mb-3">
        <label for="comment" class="form-label">Comment:</label>
        <input
          type="textarea"
          name="comment"
          v-model="form.comment"
          class="form-control"
          required="true"
        />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import { defineComponent } from 'vue';
import { normalizeText, normalizeDiacritics } from 'normalize-text';
import axios from 'axios';
import { BAlert } from 'bootstrap-vue-next';

import Hashes from 'jshashes';

export default defineComponent({
  name: 'AddEntryView',
  components: {
    VueDatePicker,
    BAlert,
  },
  data() {
    return {
      form: {
        name: null,
        email: null,
        nationality: null,
        birthdate: null,
        comment: null,
        origin: null,
      },
      success_countdown: 0,
      error_countdown: 0,
    };
  },
  methods: {
    submit() {
      var SHA256 = new Hashes.SHA256();

      const request = {
        name_hash: SHA256.hex(normalize(this.form.name)),
        email_hash: SHA256.hex(normalize(this.form.email)),
        birthdate_hash: SHA256.hex(normalize(this.form.birthdate)),
        origin: this.$store.getters.getConference,
        comment: this.form.comment,
      };

      axios
        .post('entries', request)
        .then((response) => {
          if (response.status == 200) {
            this.success_countdown = 1000 * 10;
            this.resetForm();
          } else {
            this.error_countdown = 1000 * 10;
          }
        })
        .catch((error) => {
          this.error_countdown = 1000 * 10;
        });

      console.log(this.form);
    },
    resetForm() {
      Object.keys(this.form).forEach((key) => {
        this.form[key] = null;
      });
    },
  },
});

function normalize(text) {
  return normalizeText(normalizeDiacritics(text));
}
</script>
