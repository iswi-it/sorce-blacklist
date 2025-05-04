<template>
  <h1 class="text-center mb-5">Welcome to the SOrCE-Blacklist!</h1>
  <div class="row align-items-start">
    <div class="col">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Entries</h5>
          <p class="card-text">
            There are <b>{{ entries }}</b> entries in the blacklist!
          </p>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Possible Actions</h5>
          <p class="card-text">
            You can add new entries to the blacklist or check a list of participant data in comparison with the save hashes in the blacklist.
          </p>
          <a href="#" class="card-link">Add Entry</a>
          <a href="#" class="card-link">Check Entries</a>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Registered Conferences</h5>
          <p class="card-text">
          <ul v-if="conferences">
            <li v-for="conference in conferences">{{ conference }}</li>
          </ul>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  name: 'HomeView',
  setup() {
    const entries = ref(0);
    const conferences = ref(null);

    axios.get('statistics').then((response) => {
      if (response.data.num) {
        entries.value = response.data.num;
      }
      if (response.data.conferences) {
        conferences.value = response.data.conferences;
      }
    });

    return {
      entries,
      conferences,
    };
  },
};
</script>
