<template>
  <v-container fluid fill-width>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="allUsers"
      item-key="email"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>Users</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">New User</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-text-field v-model="newUser.name" label="Name" required></v-text-field>
                  </v-row>
                  <v-row>
                    <v-text-field
                      v-if="formTitle === 'New User'"
                      v-model="newUser.email"
                      label="Email"
                      type="email"
                      required
                    ></v-text-field>
                    <v-text-field
                      v-else
                      v-model="newUser.email"
                      label="Email"
                      type="email"
                      readonly
                    ></v-text-field>
                  </v-row>
                  <v-row>
                    <v-select v-model="newUser.role" :items="roles" label="Role" required></v-select>
                  </v-row>
                  <v-row>
                    <v-select
                      v-model="newUser.getAlerts"
                      :items="[true, false]"
                      label="Notify"
                      required
                    ></v-select>
                  </v-row>
                  <v-row>
                    <v-text-field
                      v-model="newUser.password"
                      label="Password"
                      type="password"
                      required
                    ></v-text-field>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">Close</v-btn>
                <v-btn
                  v-if="formTitle === 'New User'"
                  color="blue darken-1"
                  text
                  @click="createUser"
                >Create</v-btn>
                <v-btn v-else color="blue darken-1" text @click="editUser">Edit</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.notify="{ item }">
        <v-switch v-model="item.getAlerts" class="ma-2" @click="changeNotify(item)"></v-switch>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon
          v-if="userInfo.email !== item.email"
          small
          class="mr-2"
          @click="editUserForm(item)"
        >edit</v-icon>
        <v-icon
          v-else
          small
          class="mr-2"
          @click="$router.push('/Profile') "
        >edit</v-icon>
        <v-icon small @click="deleteUser(item)">delete</v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import gql from "graphql-tag";
import { mapActions } from "vuex";

export default {
  name: "ManageUser",
  apollo: {
    allUsers: {
      query: gql`
        query {
          allUsers {
            edges {
              node {
                name
                email
                role
                getAlerts
              }
            }
          }
        }
      `,
      update: data => {
        return data.allUsers.edges.map(function(edge) {
          return edge.node;
        });
      }
    },
    userInfo: gql`
      query {
        userInfo {
          email
        }
      }
    `
  },

  data: () => ({
    headers: [
      { text: "Name", value: "name" },
      { text: "Email", value: "email" },
      { text: "Role", value: "role" },
      { text: "Notify", value: "notify" },
      { text: "Actions", value: "action", sortable: false }
    ],
    newUser: {
      name: "",
      email: "",
      role: "",
      getAlerts: "",
      password: ""
    },
    roles: ["Admin", "User"],
    selected: [],
    dialog: false,
    formTitle: "New User"
  }),

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  methods: {
    ...mapActions(["sendError", "sendSuccess"]),
    close() {
      this.dialog = false;
      setTimeout(() => {
        this.newUser = {
          name: "",
          email: "",
          role: "",
          password: ""
        };
        this.formTitle = "New User";
      }, 300);
    },
    editUserForm(user) {
      this.newUser = {
        name: user.name,
        email: user.email,
        role: user.role,
        getAlerts: user.getAlerts,
        password: ""
      };
      this.formTitle = "Edit User";
      this.dialog = true;
    },
    changeNotify(user) {
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation(
              $email: String
              $getAlerts: Boolean
            ) {
              updateUser(
                email: $email
                getAlerts: $getAlerts
              ) {
                user {
                  email
                  getAlerts
                }
              }
            }
          `,
          // Parameters
          variables: {
            email: user.email,
            getAlerts: !user.getAlerts,
          }
        })
        .then(data => {
          this.sendSuccess("Updated notify for user");
          this.dialog = false;
          this.$apollo.queries.allUsers.refetch();
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to update notify for user");
          this.dialog = false;
          // Error
          console.error(error);
        });
    },
    editUser() {
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation(
              $email: String
              $name: String
              $password: String
              $role: String
              $getAlerts: Boolean
            ) {
              updateUser(
                email: $email
                name: $name
                newPassword: $password
                role: $role
                getAlerts: $getAlerts
              ) {
                user {
                  name
                  email
                  role
                  getAlerts
                }
              }
            }
          `,
          // Parameters
          variables: {
            email: this.newUser.email,
            name: this.newUser.name,
            password:
              this.newUser.password === "" ? null : this.newUser.password,
            role: this.newUser.role,
            getAlerts: this.newUser.getAlerts
          }
        })
        .then(data => {
          this.sendSuccess("Updated user");
          this.dialog = false;
          this.$apollo.queries.allUsers.refetch();
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to update user");
          this.dialog = false;
          // Error
          console.error(error);
        });
    },
    deleteUser(user) {
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation($email: String) {
              deleteUser(email: $email) {
                result
              }
            }
          `,
          // Parameters
          variables: {
            email: user.email
          }
        })
        .then(data => {
          this.sendSuccess("Deleted user");
          this.$apollo.queries.allUsers.refetch();
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to delete user");
          // Error
          console.error(error);
        });
    },
    createUser() {
      // Call to the graphql mutation
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation(
              $email: String!
              $name: String!
              $password: String!
              $role: String!
              $getAlerts: Boolean!
            ) {
              createUser(
                email: $email
                name: $name
                password: $password
                role: $role
                getAlerts: $getAlerts
              ) {
                user {
                  name
                  email
                  role
                }
              }
            }
          `,
          // Parameters
          variables: {
            email: this.newUser.email,
            name: this.newUser.name,
            password: this.newUser.password,
            role: this.newUser.role,
            getAlerts: this.newUser.getAlerts
          }
        })
        .then(data => {
          this.sendSuccess("Created new user");
          this.$apollo.queries.allUsers.refetch();
          this.dialog = false;
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to create user");
          this.dialog = false;
          // Error
          console.error(error);
        });
    }
  }
};
</script>