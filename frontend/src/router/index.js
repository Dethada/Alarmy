import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/profile',
    name: 'Profile',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/manage/user',
    name: 'ManageUser',
    component: () => import('../views/ManageUser.vue')
  },
  {
    path: '/manage/device',
    name: 'ManageDevice',
    component: () => import('../views/ManageDevice.vue')
  },
  {
    path: '/alerts/detail',
    name: 'AlertDetail',
    component: () => import('../views/AlertDetail.vue')
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../views/Alerts.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
