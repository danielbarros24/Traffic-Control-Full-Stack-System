import Vue from 'vue'
import Vuex from 'vuex'

// imports of AJAX functions will go here
import { authenticate } from '@/api'  
import { isValidJwt, EventBus } from '@/utils'


Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    snackbars: [],
    surveys: [],
    currentSurvey: {},
    user: {},
    jwt: ''
  },
  mutations: {

    SET_SNACKBAR(state, snackbar) {
      state.snackbars= state.snackbars.concat(snackbar)
    },
    setUserData (state, payload) {
      console.log('setUserData payload = ', payload)
      state.userData = payload.userData
    },
    setJwtToken (state, payload) {
      console.log('setJwtToken payload = ', payload)
      localStorage.token = payload.jwt.token
      state.jwt = payload.jwt
    }
  },
  actions: {
    setSnackbar({commit}, snackbar) {
      snackbar.showing = true;
      snackbar.color = snackbar.color || 'primary';
      commit ('SET_SNACKBAR', snackbar);
    },
    login (context, userData) {
      context.commit('setUserData', { userData })
      return authenticate(userData)
        .then(response => context.commit('setJwtToken', { jwt: response.data }))
        .catch(error => {
          console.log('Error Authenticating: ', error)
          EventBus.emit('failedAuthentication', error)
        })
    }
  },
  getters: {
    // reusable data accessors
    isAuthenticated (state) {
      return isValidJwt(state.jwt.token)
    }
  },
  modules: {
  },
})
