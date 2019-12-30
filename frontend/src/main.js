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

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  apolloProvider: createProvider(),
  render: h => h(App)
}).$mount('#app')

// const baseURL = 'http://192.168.14.131:5000';
// axios.defaults.baseURL = baseURL;
// if (typeof baseURL !== 'undefined') {
//   Vue.axios.defaults.baseURL = baseURL;
// }

Vue.use(Chartkick.use(Chart))
Vue.use(VueAxios, axios)
Vue.axios.defaults.baseURL = 'http://192.168.14.131:5000'
Vue.axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('token');

// Vue.use(require('@websanova/vue-auth'), {
//   auth: require('@websanova/vue-auth/drivers/auth/bearer.js'),
//   http: require('@websanova/vue-auth/drivers/http/axios.1.x.js'),
//   router: require('@websanova/vue-auth/drivers/router/vue-router.2.x.js')
// })
