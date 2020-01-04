<template>
  <v-container fluid fill-width>
    <v-tabs v-model="tab" class="elevation-2">
      <v-tabs-slider></v-tabs-slider>

      <v-tab href="#person-tab">Person</v-tab>
      <v-tab href="#env-tab">Environment</v-tab>

      <v-tab-item value="person-tab">
        <v-card flat tile>
          <v-data-table
            :headers="person_headers"
            :items="allPersonAlert"
            item-key="alertTime"
            class="elevation-1"
          >
            <template v-slot:item.alertTime="{ item }">{{ formatTime(item.alertTime) }}</template>
            <template v-slot:item.image="{ item }">
              <!-- <v-btn text @click="$router.push('/alerts/image')">View</v-btn> -->
              <v-icon @click="$router.push('/alerts/detail?cid=' + item.cid)">photo</v-icon>
              <!-- <a v-bind:href="'data:image/jpeg;base64,'+item.image" target="_blank">View Image</a> -->
            </template>
            <template v-slot:item.action="{ item }">
              <v-icon small @click="deletePersonAlert(item)">delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-tab-item>
      <v-tab-item value="env-tab">
        <v-card flat tile>
          <v-data-table
            :headers="env_headers"
            :items="envAlertData"
            item-key="email"
            class="elevation-1"
          >
            <template v-slot:item.action="{ item }">
              <v-icon small @click="deleteEnvAlert(item)">delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-tab-item>
    </v-tabs>
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
                cid
              }
            }
          }
        }
      `,
      update: data => {
        return data.allPersonAlert.edges
          .map(function(edge) {
            return edge.node;
          })
          .reverse();
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
    allEnvalert: [],
    tab: null
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
      return moment(time).format("YYYY-MM-DD hh:mm:ss");
    },
    deletePersonAlert(alert) {
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation($cid: Int!) {
              deletePersonAlert(cid: $cid) {
                result
              }
            }
          `,
          // Parameters
          variables: {
            cid: alert.cid
          }
        })
        .then(data => {
          this.sendSuccess("Deleted Alert");
          this.$apollo.queries.allPersonAlert.refetch();
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to delete alert");
          // Error
          console.error(error);
        });
    },
    deleteEnvAlert(alert) {
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation($cid: Int!) {
              deleteEnvAlert(cid: $cid) {
                result
              }
            }
          `,
          // Parameters
          variables: {
            cid: alert.cid
          }
        })
        .then(data => {
          this.sendSuccess("Deleted Alert");
          this.$apollo.queries.allEnvalert.refetch();
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to delete alert");
          // Error
          console.error(error);
        });
    },
  }
};
</script>