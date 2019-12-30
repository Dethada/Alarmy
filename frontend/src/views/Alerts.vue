<template>
  <!-- <v-container md>{{ allEnvalert }}</v-container> -->
  <v-container fluid fill-width>
    <v-container fluid fill-width>
      <v-data-table :headers="person_headers" :items="allPersonAlert" item-key="alertTime" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>Person Alerts</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
          </v-toolbar>
        </template>
        <template v-slot:item.alertTime="{ item }">
          {{ formatTime(item.alertTime) }}
        </template>
        <template v-slot:item.image="{ item }">
          <a v-bind:href="'data:image/jpeg;base64,'+item.image" target="_blank">View Image</a>
        </template>
        <template v-slot:item.action="{ item }">
          <v-icon small>delete</v-icon>
        </template>
      </v-data-table>
    </v-container>
    <v-container fluid fill-width>
      <v-data-table :headers="env_headers" :items="envAlertData" item-key="email" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>Environment Alerts</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
          </v-toolbar>
        </template>
        <template v-slot:item.action="{ item }">
          <v-icon small>stop</v-icon>
        </template>
      </v-data-table>
    </v-container>
  </v-container>
</template>

<script>
import gql from "graphql-tag";
import { mapActions } from "vuex";
import moment from "moment";

export default {
  name: "Alerts",
  apollo: {
    allEnvalert: {
      query: gql`
        query {
          allEnvalert {
            edges {
              node {
                alertTime
                reason
                gas {
                  lpg
                  co
                  smoke
                }
                temperature {
                  value
                }
              }
            }
          }
        }
      `,
      update: data => {
        return data.allEnvalert.edges.map(function(edge) {
          return edge.node;
        });
      }
    },
    allPersonAlert: {
      query: gql`
        query {
            allPersonAlert {
              edges {
                node {
                  alertTime
                  image
                }
              }
            }
          }
        `,
        update: data => {
        return data.allPersonAlert.edges.map(function(edge) {
          return edge.node;
        }).reverse();
      }
    }
  },

  data: () => ({
    env_headers: [
      { text: "Time", value: "time" },
      { text: "Reason", value: "reason" },
      { text: "Temperature °C", value: "temperature" },
      { text: "LPG (PPM)", value: "lpg" },
      { text: "CO (PPM)", value: "co" },
      { text: "Smoke (PPM)", value: "smoke" },
      { text: "Actions", value: "action", sortable: false }
    ],
    person_headers: [
      { text: "Time", value: "alertTime" },
      { text: "Image", value: "image" },
      { text: "Actions", value: "action", sortable: false }
    ],
    allEnvalert: []
  }),

  computed: {
    envAlertData: function() {
      let x = [];
      this.allEnvalert.forEach(item => {
        x.unshift({
          time: moment(item.alertTime).format("YYYY-MM-DD hh:mm:ss"),
          reason: item.reason,
          temperature: item.temperature.value.toFixed(2),
          lpg: item.gas.lpg.toFixed(5),
          co: item.gas.co.toFixed(5),
          smoke: item.gas.smoke.toFixed(5)
        });
      });
      return x;
    }
  },

  methods: {
    ...mapActions(["sendError", "sendSuccess"]),
    formatTime(time) {
      return moment(time).format("YYYY-MM-DD hh:mm:ss")
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
          this.$apollo.queries.allEnvalert.refetch();
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to delete user");
          // Error
          console.error(error);
        });
    }
  }
};
</script>