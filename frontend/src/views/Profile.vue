<template>
  <v-container fluid fill-width>
    <v-card>
      <v-container>
        <form>
          <v-text-field v-model="userInfo.name" :counter="100" label="Name"></v-text-field>
          <v-text-field v-model="userInfo.email" label="Email" readonly></v-text-field>
          <v-select v-model="userInfo.role" :items="['Admin', 'User']" label="Role" readonly></v-select>
          <v-select v-model="userInfo.getAlerts" :items="[true, false]" label="Notify"></v-select>
          <v-text-field v-model="old_pw" label="Old Password" type="password"></v-text-field>
          <v-text-field v-model="new_pw" label="New Password" type="password"></v-text-field>

          <v-btn class="mr-4" @click="submit">submit</v-btn>
        </form>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import gql from "graphql-tag";
import { mapActions } from "vuex";

export default {
  name: "Profile",
  apollo: {
    userInfo: gql`
      query {
        userInfo {
          name
          email
          role
          getAlerts
        }
      }
    `
  },

  data: () => ({
    old_pw: undefined,
    new_pw: undefined
  }),

  methods: {
    ...mapActions(["sendError", "sendSuccess"]),
    submit() {
      //  Set to undefined if empty so we dont send it
      if (this.old_pw === "") {
        this.old_pw = undefined;
      }
      if (this.new_pw === "") {
        this.new_pw = undefined;
      }
      // Call to the graphql mutation
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation(
              $name: String
              $getAlerts: Boolean
              $new_password: String
              $old_password: String
            ) {
              updateUser(
                name: $name
                getAlerts: $getAlerts
                newPassword: $new_password
                oldPassword: $old_password
              ) {
                user {
                  name
                }
              }
            }
          `,
          // Parameters
          variables: {
            name: this.userInfo.name,
            getAlerts: this.userInfo.getAlerts,
            old_password: this.old_pw,
            new_password: this.new_pw
          }
        })
        .then(data => {
          this.sendSuccess("Updated profile");
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to update profile");
          // Error
          console.error(error);
        });
    }
  }
};
</script>