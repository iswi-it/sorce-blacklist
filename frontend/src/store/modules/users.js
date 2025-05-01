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
    return new Promise(async (resolve, reject) => {
      axios
        .post('token', user)
        .then(async (response) => {
          // save token and get user data
          const token = response.data.access_token;
          localStorage.setItem('token', token);
          await dispatch('viewMe');
          resolve();
        })
        .catch((error) => {
          // authentication failed / wrong password or username
          if (error.response.status == 401) {
            reject(error.response.data.detail);
          }
        });
    });
  },
  async viewMe({ commit, dispatch }) {
    axios
      .get('users/me')
      .then(async (response) => {
        // save user data
        await commit('setUser', response.data);
      })
      .catch(async () => {
        // authentication failed
        await dispatch('logOut');
      });
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
