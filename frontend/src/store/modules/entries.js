import axios from 'axios';
import { entries } from 'core-js/core/array';

const state = {
  entries_input: null,
  entries_hashed: null,
  entries_output: null,
};

const getters = {
  areEntriesLoaded: (state) => !!state.entries_input,
  areEntriesHashed: (state) => !!state.entries_hashed,
  areEntriesProcessed: (state) => !!state.entries_output,
  entriesLength: (state) => state.entries_input.length,
  getEntryByPos: (state) => (i) => entries_input.at(i),
  getHashByPos: (state) => (i) => entries_hashed.at(i),
  getOutputByPos: (state) => (i) => entries_output.at(i),
};
