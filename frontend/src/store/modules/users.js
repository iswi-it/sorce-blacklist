import axios from 'axios';

const state = {
  user: null,
  conference: null,
};

const getters = {
  isAuthenticated: (state) => !!state.user,
  getUser: (state) => state.user,
  getConference: (state) => state.conference,
};

const actions = {
  async logIn({ dispatch }, user) {
    const response = await axios.post('token', user);
    const token = response.data.access_token;
    localStorage.setItem('token', token);
    await dispatch('viewMe');
  },
  async viewMe({ commit }) {
    let { data } = await axios.get('users/me');
    await commit('setUser', data);
  },
  async logOut({ commit }) {
    localStorage.removeItem('token');
    await commit('logout');
  },
};

const mutations = {
  setUser(state, data) {
    state.user = data.username;
    state.conference = data.conference;
  },
  logout(state) {
    state.conference = null;
    state.user = null;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
