import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    snackbars: [],
    user: null,
    token: null,
  },
  getters: {
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
    SET_SNACKBAR(state, snackbar) {
      state.snackbars= state.snackbars.concat(snackbar)
    }
  },
  actions: {
    setSnackbar({commit}, snackbar) {
      snackbar.showing = true;
      snackbar.color = snackbar.color || 'primary';
      commit ('SET_SNACKBAR', snackbar);
    }
  },
  modules: {
  },
})
