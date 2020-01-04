<template>
  <v-container v-if="personAlert">
    <v-card class="mx-auto">
      <v-card-actions>
        <v-icon @click="$router.go(-1)">arrow_back</v-icon>
      </v-card-actions>
      <v-img :src="'data:image/jpeg;base64,'+personAlert.image" height="500px" contain></v-img>

      <v-card-title>Person Detected</v-card-title>

      <v-card-subtitle>Capture Time: {{ alertTime }}</v-card-subtitle>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red" text @click="deletePersonAlert">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import gql from "graphql-tag";
import moment from "moment";
import { mapActions } from 'vuex'

export default {
  name: "AlertDetail",
  apollo: {
    personAlert: {
      query: gql`
        query($cid: Int!) {
          personAlert(cid: $cid) {
            alertTime
            image
          }
        }
      `,
      variables() {
        return {
          cid: this.$route.query.cid
        };
      }
    }
  },
  data: () => ({
    personAlert: null
  }),

  computed: {
    alertTime: function() {
      return moment(this.personAlert.alertTime).format(
        "Do MMMM YYYY, h:mm:ss a"
      );
    }
  },

  methods: {
    ...mapActions(['sendError', 'sendSuccess']),
    deletePersonAlert() {
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
            cid: this.$route.query.cid
          }
        })
        .then(data => {
          this.sendSuccess("Deleted Alert");
          // Result
          console.log(data);
          this.$router.go(-1);
        })
        .catch(error => {
          this.sendError("Failed to delete alert");
          // Error
          console.error(error);
        });
    }
  }
};
</script>