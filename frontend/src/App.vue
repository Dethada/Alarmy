<template>
  <v-app>
    <v-content>
      <div v-if="loggedIn">
        <navigation @logout="loggedIn = false"></navigation>
        <router-view></router-view>
      </div>
      <div v-else>
        <login @loggedin="loggedIn = true" ></login>
      </div>
      <Snackbar></Snackbar>
    </v-content>
  </v-app>
</template>

<script>
import Navigation from '@/components/Navigation'
import Snackbar from '@/components/Snackbar'
import Login from '@/views/Login'

export default {
  name: "App",

  components: {
    Login,
    Navigation,
    Snackbar
  },

  data: () => ({
    loggedIn: localStorage.getItem('token')
  })
};
</script>
