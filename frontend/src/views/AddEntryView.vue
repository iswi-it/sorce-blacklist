<template>
  <section>
    <BAlert v-model="success_countdown" variant="success" dismissible fade>
      Entry was successfully added to SOrCE-Blacklist!
    </BAlert>
    <BAlert v-model="error_countdown" variant="danger" dismissible fade>
      Entry was successfully added to SOrCE-Blacklist!
    </BAlert>
    <h3>Add Participant to Blacklist</h3>
    <p>
      This form will let you add a participant to the SOrCE-Blacklist. All data
      you enter will be first hashed locally and the send to the server to be
      stored in a central database. Please make sure to follow the instructions
      of each form entry, so entries can be matched later. Hashed Data will be
      normalized, so the blacklist and matching are insensitive towards capital
      letters.
    </p>
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
        <div class="form-text">
          Full name of the participant that should be put on the blacklist. Data
          will be hashed!
        </div>
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
        <div class="form-text">
          E-Mail of the participant that should be put on the blacklist. Data
          will be hashed!
        </div>
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
        <div class="form-text">
          Please use the full english name of the participants nationality, e.g
          as written in
          <a
            href="https://github.com/Imagin-io/country-nationality-list/blob/master/countries.csv"
            target="_blank"
            >this list</a
          >
          in the column nationality.
        </div>
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
        <div class="form-text">
          Please choose the birthdate of participant that will be put on the
          blacklist. Data will be hashed!
        </div>
      </div>
      <div class="mb-3">
        <label for="comment" class="form-label">Comment:</label>
        <textarea
          type="textarea"
          name="comment"
          v-model="form.comment"
          class="form-control"
          required="true"
        />
        <div class="form-text">
          Field for a general comment, e.g. why the person was put on the
          blacklist. Don't put privat data like names or emails in this field as
          it won't be hashed!
        </div>
      </div>
      <button type="submit" class="btn btn-primary">
        Blacklist Participant
      </button>
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
