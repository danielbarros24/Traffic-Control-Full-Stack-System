import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router/index'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    snackbars: [],
  },
  mutations: {

    SET_SNACKBAR(state, snackbar) {
      state.snackbars= state.snackbars.concat(snackbar)
    },
  },
  actions: {
    setSnackbar({commit}, snackbar) {
      snackbar.showing = true;
      snackbar.color = snackbar.color || 'primary';
      commit ('SET_SNACKBAR', snackbar);
    },

    login: ({commit}, authData) => {
      const urlRasp = "192.168.1.216:5000"
      const urlDesktop = "127.0.0.1:5000"
      
      axios.post(`http://192.168.1.216:5000/login`, {
        username: authData.username,
        password: authData.password,
      }).then(response => {
        let success = response.data.success;
  
        if (success === true) {
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('username', authData.username);
          router.replace('dashboard');
        } 
        else {
          console.log('Login error');
        }
      }).catch(error => {
        console.log(error);
      })
    },
    logout: ({commit}) => {
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      router.replace('login');
    },
  },
  getters: {
    isAuthenticated(state) {
      return localStorage.getItem('token') !== null;
    },
  },
  modules: {
  },
})
