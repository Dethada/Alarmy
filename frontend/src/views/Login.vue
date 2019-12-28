<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>Alarmy Login</v-toolbar-title>
                <v-spacer />
              </v-toolbar>
              <v-card-text>
                <v-form action="#" @submit.prevent="login">
                  <v-text-field
                    v-model="email"
                    label="Email"
                    name="email"
                    prepend-icon="person"
                    type="email"
                  />

                  <v-text-field
                    v-model="password"
                    id="password"
                    label="Password"
                    name="pass"
                    prepend-icon="lock"
                    type="password"
                  />
                  <v-card-actions>
                    <v-spacer />
                    <v-btn type="submit" color="primary">Login</v-btn>
                  </v-card-actions>
                </v-form>
              </v-card-text>
              <v-btn @click="test" color="primary">Test</v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <v-snackbar
        v-model="snackbar"
        :bottom="snackbar_bottom"
        :right="snackbar_bottom"
        :timeout="snackbar_timeout"
      >
        {{ snackbar_text }}
        <v-btn :color="snackbar_color" text @click="snackbar = false">Close</v-btn>
      </v-snackbar>
    </v-content>
  </v-app>
</template>

<script>
import axios from "axios";
import { mapActions } from 'vuex'

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      snackbar: false,
      snackbar_color: "pink",
      snackbar_text: "",
      snackbar_timeout: 5000,
      snackbar_right: true,
      snackbar_bottom: true
    };
  },
  methods: {
    ...mapActions(['sendError', 'sendSuccess']),
    login() {
      let params = {
        email: this.email,
        pass: this.password
      };
      axios
        .post("/token/auth", params)
        .then(resp => {
          localStorage.setItem("token", resp.data.access_token);
          axios.defaults.headers.common["Authorization"] =
            "Bearer " + resp.data.access_token;
          this.sendSuccess('Login Success!')
          this.$emit("loggedin");
        })
        .catch(err => {
          this.sendError('Login Failed!')
        });
    },
    test() {
      axios.get("/api/example").then(resp => {
        console.log(resp.data);
      });
    }
  }
};
</script>
