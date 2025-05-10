<template>
  <section>
    <BAlert
      v-if="error.countdown"
      v-model="error.countdown"
      variant="danger"
      dismissible
      fade
    >
      {{ error.message }}
    </BAlert>
    <h3>Check Blacklist</h3>
    <p>
      This form will let you upload a csv file with data of participants, which
      will be checked against the hashes in the blacklist. Each field will be
      hashed locally and then uploaded to the server. Please use the csv format
      as provided in the <a href="/example.csv">example list</a> or listed below:
      <ul>
        <li>name: Full name of participant (case insensitive)</li>
        <li>email: E-Mail address of participant (case insensitive)</li>
        <li>nationality: Nationality of participant in english (full name) as mentioned in           <a
            href="https://github.com/Imagin-io/country-nationality-list/blob/master/countries.csv"
            target="_blank"
            >this list</a
          > (case insensitive)</li>
        <li>birthdate: Date of bith in format DD/MM/YYYY</li>
      </ul>

      After uploading your list, you will see the imported data and you can start the checking process. You will get back only the rows that have been found in the blacklist with comments that have been provided by the person enlisting the participant. The score shows which details of the participant have been found in the blacklist (also marked with red="not found" or green="found").
    </p>
    <BFormFile
      v-if="!file_correct"
      v-model="file"
      label="Please provide a csv file in the expected format!"
      accept=".csv"
      required
      @update:model-value="handleFileUpload"
    />
    <div v-if="entries_output.length > 0 && entries_input.length > 0">
      <BButton @click="clearResult" class="mb-3 " variant="primary">Make another scan</BButton>

      <h4>Blacklist Results</h4>
      <p>
        The search found {{ entries_found.length }} entries from your list in
        the blacklist.
      </p>

      <table class="table table-bordered">
        <thead>
          <tr>
            <th>#</th>
            <th>Full Name</th>
            <th>E-Mail</th>
            <th>Nationality</th>
            <th>Date of Birth</th>
            <th>Comment</th>
            <th>Score</th>
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
      <BButton @click="checkBlacklist" class="mb-3 " variant="primary">Check Blacklist!</BButton>

      <h4>Content of uploaded list</h4>

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
import { BFormFile, BButton, BAlert } from 'bootstrap-vue-next';
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
    BAlert,
  },
  data() {
    return {
      file: null,
      file_correct: false,
      header: [],
      entries_input: [],
      entries_output: [],
      entries_found: [],
      error: {
        countdown: 0,
        message: null
      }
    };
  },
  methods: {
    handleFileUpload() {
      if (this.file && this.file.type == 'text/csv') {
        const expectedHeader = ['name', 'email', 'nationality', 'birthdate'];

        Papa.parse(this.file, {
          skipEmptyLines: true,
          complete: (results) => {
            const actualHeader = results.meta.fields;

            const isHeaderValid = expectedHeader.length === actualHeader.length &&
                          expectedHeader.every((field, index) => field === actualHeader[index]);

            if (isHeaderValid) {
              this.entries_input = results.data;
              this.header = results.meta.fields;
              this.file_correct = true;
            } else {
              this.error.message = 'Please upload a csv file with header (name, email, nationality, birthdate)!'
              this.error.countdown = 60 * 1000;
            }
          },
          header: true,
        });
      } else {
        this.error.message = 'Please upload correct file type!'
        this.error.countdown = 60 * 1000;
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
    clearResult() {
      this.file = null;
      this.header = [];
      this.entries_input = [];
      this.entries_output = [];
      this.entries_found = [];
    }
  },
});
</script>
