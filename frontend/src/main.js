import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { createProvider } from './vue-apollo'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'
// import VueSocketIO from 'vue-socket.io'
import VueSocketIOExt from 'vue-socket.io-extended';
import io from 'socket.io-client';


Vue.config.productionTip = false

Vue.use(Chartkick.use(Chart))

const baseURL = process.env.VUE_APP_BASE_URL || 'http://192.168.1.103:5000';

const token = localStorage.getItem('token')
const socket = io(baseURL + '/alert', {
  query: {token: token}
});

Vue.use(VueSocketIOExt, socket);

Vue.use(VueAxios, axios)
Vue.axios.defaults.baseURL = baseURL
Vue.axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;

new Vue({
  router,
  store,
  vuetify,
  apolloProvider: createProvider(),
  render: h => h(App)
}).$mount('#app')
