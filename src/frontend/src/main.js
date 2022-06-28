import 'regenerator-runtime'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import {Chart} from 'chart.js'
import Chartkick from 'vue-chartkick'

import '@/plugins/Dayjs';
import store from './store'


Vue.config.productionTip = false

Vue.use(Chartkick.use(Chart));
new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
