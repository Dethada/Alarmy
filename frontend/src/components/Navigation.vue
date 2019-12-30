<template>
  <span>
    <v-toolbar color="black darken-4" dark>
      <!-- <v-toolbar-side-icon class="hidden-md-and-up" @click="drawer = !drawer"></v-toolbar-side-icon> -->
      <v-spacer class="hidden-md-and-up"></v-spacer>
      <v-toolbar-title>
        <v-btn text to="/">{{ appTitle }}</v-btn>
      </v-toolbar-title>
      <v-btn text class="hidden-sm-and-down" to="/profile">Profile</v-btn>
      <v-btn text class="hidden-sm-and-down" to="/alerts">Alerts</v-btn>
      <v-menu offset-y :open-on-hover="true">
        <template v-slot:activator="{ on }">
          <v-btn text class="hidden-sm-and-down" v-on="on">Manage</v-btn>
        </template>
        <v-list>
          <v-list-item @click="$router.push('/manage/device')">
            <v-list-item-title>Manage Device</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="userInfo.role === 'Admin'" @click="$router.push('/manage/user')">
            <v-list-item-title to="/manage">Manage Users</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <!-- <v-btn v-if="userInfo.role === 'Admin'" text class="hidden-sm-and-down" to="/manage">Manage</v-btn> -->
      <v-spacer class="hidden-sm-and-down"></v-spacer>
      <v-btn text class="hidden-sm-and-down" @click="logout">Log out</v-btn>
    </v-toolbar>
  </span>
</template>

<script>
import gql from "graphql-tag";

export default {
  name: "Navigation",
  apollo: {
    userInfo: gql`
      query {
        userInfo {
          role
        }
      }
    `
  },

  data() {
    return {
      appTitle: "Alarmy"
    };
  },
  methods: {
    logout() {
      console.log("logout");
      localStorage.removeItem("token");
      this.$emit("logout");
    }
  }
};
</script>