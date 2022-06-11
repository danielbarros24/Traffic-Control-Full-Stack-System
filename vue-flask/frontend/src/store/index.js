import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    snackbars: []
  },
  getters: {
  },
  mutations: {
    SET_SNACKBAR(state, snackbar) {
      state.snackbars= state.snackbars.concat(snackbar)
    }
  },
  actions: {
    setSnackbar({commit}, snackbar) {
      snackbar.showing = true;
      snackbar.color = snackbar.color || 'red darken-3';
      commit ('SET_SNACKBAR', snackbar);
    }
  },
  modules: {
  }
})
