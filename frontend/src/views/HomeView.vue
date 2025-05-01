<template>
  <div class="row align-items-start">
    <div class="col">
      <div class="card">
        <div class="card-body" v-if="entries">
          There are <b>{{ entries }}</b> entries in the blacklist!
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <div class="card-body" v-if="entries">Column 2 (TODO)</div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <div class="card-body" v-if="entries">Column 3 (TODO)</div>
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
    const entries = ref(null);

    axios.get('entries/statistics').then((response) => {
      if (response.data.num) {
        entries.value = response.data.num;
      }
    });

    return {
      entries,
    };
  },
};
</script>
