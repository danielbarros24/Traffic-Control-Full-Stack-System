import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router/index'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    snackbars: [],
    username: null,
	  token: null,
  },
  mutations: {

    SET_SNACKBAR(state, snackbar) {
      state.snackbars= state.snackbars.concat(snackbar)
    },

    authUser(state, userData) {
      state.username = userData.username;
      state.token = userData.token;
    },
    clearAuthData(state) {
      state.username = null;
      state.token = null;
    },
    
  },
  actions: {
    setSnackbar({commit}, snackbar) {
      snackbar.showing = true;
      snackbar.color = snackbar.color || 'primary';
      commit ('SET_SNACKBAR', snackbar);
    },

    login: ({commit}, authData) => {
      axios.post(':5000/login', {
        username: authData.username,
        password: authData.password,
      }).then(response => {
        let success = response.data.success;
  
        if (success === true) {
          commit('authUser', { username: authData.username, token: response.data.token });
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
    autoLogin({commit}) {
      let token = localStorage.getItem('token');
      let username = localStorage.getItem('username');
  
      if (!token || !username) {
        return;
      }
  
      commit('authUser', { username: username, token: token });
    },
    logout: ({commit}) => {
      commit('clearAuthData');
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      router.replace('login');
    },
  },
  getters: {
    isAuthenticated(state) {
      return state.token !== null;
    },
  },
  modules: {
  },
})
