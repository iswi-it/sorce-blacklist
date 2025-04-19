<template>
  <section>
    <BFormFile
      v-model="file"
      label="Please provide a csv file!"
      accept=".csv"
      required
      @update:model-value="handleFileUpload"
    />
    <div v-if="csvData.length">
      <h4>Parsed CSV:</h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th v-for="(header, index) in csvData[0]" :key="index">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in csvData.slice(1)" :key="rowIndex">
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
import { BFormFile } from 'bootstrap-vue-next';
import Papa from 'papaparse';

export default defineComponent({
  name: 'CheckEntriesView',
  components: {
    BFormFile,
  },
  data() {
    return {
      file: null,
      csvData: [],
      entries_output: [],
    };
  },
  methods: {
    handleFileUpload() {
      if (this.file && this.file.type == 'text/csv') {
        // @TODO: check header of csv file

        Papa.parse(this.file, {
          complete: (results) => {
            this.csvData = results.data;
            console.log(results.data);
            results.data.forEach((value, index) => {});
          },
          header: true,
        });
      } else {
        alert('Please upload correct file type!');
      }
    },
  },
});
</script>
