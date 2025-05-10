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
      <p>
        The search found {{ entries_found.length }} entries from your list in
        the blacklist.
      </p>

      <table class="table table-bordered">
        <thead>
          <tr>
            <th>#</th>
            <th v-for="(header, index) in header" :key="index">
              {{ header }}
            </th>
            <th>comment</th>
            <th>score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, found_index) in entries_found" :key="found_index">
            <td>{{ entry.index }}</td>
            <ResultCell
              :entry_input="entries_input[entry.index]"
              :entry_output="entries_output[entry.index]"
              field="name"
            />
            <ResultCell
              :entry_input="entries_input[entry.index]"
              :entry_output="entries_output[entry.index]"
              field="email"
            />
            <ResultCell
              :entry_input="entries_input[entry.index]"
              :entry_output="entries_output[entry.index]"
              field="nationality"
            />
            <ResultCell
              :entry_input="entries_input[entry.index]"
              :entry_output="entries_output[entry.index]"
              field="birthdate"
            />

            <td>
              <div
                v-for="(comment, commentIndex) in entries_output[entry.index]
                  .comments"
                :key="commentIndex"
              >
                <span>{{ comment.origin }}:</span>
                <span>{{ comment.text }}</span>
              </div>
            </td>
            <td>{{ entry.score }}</td>
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
            <th>#</th>
            <th v-for="(header, index) in header" :key="index">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in entries_input" :key="rowIndex">
            <td>{{ rowIndex }}</td>
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
import ResultCell from '@/components/ResultCell.vue';

export default defineComponent({
  name: 'CheckEntriesView',
  components: {
    BFormFile,
    BButton,
    ResultCell,
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

        Papa.parse(this.file, {
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
    async checkBlacklist() {
      const plain_entries = this.entries_input;
      const hashed_entries = this.hashEntries(plain_entries);
      await axios
        .post('entries/check', hashed_entries)
        .then(async (response) => {
          if (response.status == 200) {
            this.entries_output = response.data;
            await this.entries_output.forEach((value, index) => {
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
              }
            });

            await this.entries_found.sort((a, b) => b.score - a.score);
            console.log(this.entries_found);
          }
        });
    },
    hashEntries(entries) {
      var SHA256 = new Hashes.SHA256();

      const hashed_entries = entries.map((value) => {
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
