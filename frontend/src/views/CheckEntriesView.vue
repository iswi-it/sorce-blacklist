<template>
  <section>
    <BFormFile
      v-model="file"
      label="Please provide a csv file!"
      accept=".csv"
      required
      @update:model-value="handleFileUpload"
    />
    <div v-if="entries_output.length > 0 && entries_input.length > 0">
      <h4>Blacklist Results:</h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th v-for="(header, index) in header" :key="index">
              {{ header }}
            </th>
            <th>comment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in entries_input" :key="rowIndex">
            <td v-for="(cell, cellIndex) in row" :key="cellIndex">
              {{ cell }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="entries_input.length">
      <h4>Parsed CSV:</h4>
      <BButton @click="checkBlacklist">Check Blacklist!</BButton>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th v-for="(header, index) in header" :key="index">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in entries_input" :key="rowIndex">
            <td v-for="(cell, cellIndex) in row" :key="cellIndex">
              {{ cell }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { BFormFile, BButton } from 'bootstrap-vue-next';
import Papa from 'papaparse';
import { normalizeText, normalizeDiacritics } from 'normalize-text';
import Hashes from 'jshashes';
import axios from 'axios';

export default defineComponent({
  name: 'CheckEntriesView',
  components: {
    BFormFile,
    BButton,
  },
  data() {
    return {
      file: null,
      header: [],
      entries_input: [],
      entries_output: [],
      entries_found: [],
    };
  },
  methods: {
    handleFileUpload() {
      if (this.file && this.file.type == 'text/csv') {
        // @TODO: check header of csv file

        const results = Papa.parse(this.file, {
          skipEmptyLines: true,
          complete: (results) => {
            this.entries_input = results.data;
            this.header = results.meta.fields;
          },
          header: true,
        });
      } else {
        alert('Please upload correct file type!');
      }
    },
    checkBlacklist() {
      const plain_entries = this.entries_input;
      const hashed_entries = this.hashEntries(plain_entries);
      axios.post('entries/check', hashed_entries).then((response) => {
        if (response.status == 200) {
          this.entries_output = response.data;
          this.entries_output.forEach((value, index) => {
            if (value.name_hash || value.email_hash || value.birthdate_hash) {
              var score = 0;
              if (value.name_hash) score += 1;
              if (value.email_hash) score += 1;
              if (value.birthdate_hash) score += 0.5;
              if (value.nationality_hash) score += 0.5;

              this.entries_found.push({
                index: index,
                score: score,
              });
              console.log(this.entries_found);
            }
          });
        }
      });
    },
    hashEntries(entries) {
      var SHA256 = new Hashes.SHA256();

      const hashed_entries = entries.map((value, index) => {
        console.log(value);
        return {
          name_hash: SHA256.hex(this.normalize(value.name)),
          email_hash: SHA256.hex(this.normalize(value.email)),
          nationality_hash: SHA256.hex(this.normalize(value.nationality)),
          birthdate_hash: SHA256.hex(this.normalize(value.birthdate)),
        };
      });
      return hashed_entries;
    },
    normalize(text) {
      return normalizeText(normalizeDiacritics(text));
    },
  },
});
</script>
