<template>
  <!-- <v-container md>{{ allEnvalert }}</v-container> -->
  <v-container fluid fill-width>
    <v-data-table
      :headers="headers"
      :items="envAlertData"
      item-key="email"
      class="elevation-1"
    >
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
</template>

<script>
import gql from "graphql-tag";
import { mapActions } from "vuex";
import moment from 'moment';

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
    }
  },

  data: () => ({
    headers: [
      { text: "Time", value: "time" },
      { text: "Reason", value: "reason" },
      { text: "Temperature °C", value: "temperature" },
      { text: "LPG (PPM)", value: "lpg" },
      { text: "CO (PPM)", value: "co" },
      { text: "Smoke (PPM)", value: "smoke" },
      { text: "Actions", value: "action", sortable: false }
    ],
    allEnvalert: [],
  }),

  computed: {
      envAlertData: function() {
          let x = []
          this.allEnvalert.forEach(item => {
              x.unshift({
                  time: moment(item.alertTime).format('YYYY-MM-DD hh:mm:ss'),
                  reason: item.reason,
                  temperature: item.temperature.value.toFixed(2),
                  lpg: item.gas.lpg.toFixed(5),
                  co: item.gas.co.toFixed(5),
                  smoke: item.gas.smoke.toFixed(5),
                })
          })
          return x
      }
  },

  methods: {
    ...mapActions(["sendError", "sendSuccess"]),
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
    },
  }
};
</script>