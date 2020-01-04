<template>
  <v-container fluid fill-width>
    <v-card>
      <v-container>
        <v-form action="#" @submit.prevent="updateDeviceSettings">
          <v-text-field v-model="deviceInfo.pollInterval" label="Poll Interval"></v-text-field>
          <v-text-field v-model="deviceInfo.alertInterval" label="Alert Interval"></v-text-field>
          <v-text-field v-model="deviceInfo.alarmDuration" label="Alarm Duration"></v-text-field>
          <v-text-field v-model="deviceInfo.email" label="From Email"></v-text-field>
          <v-text-field v-model="deviceInfo.motd" counter=32 label="Message of the Day"></v-text-field>
          <v-text-field
            v-model="deviceInfo.alarmCode"
            :type="visibleCode ? 'text' : 'password'"
            :append-icon="visibleCode ? 'visibility_off' : 'visibility'"
            @click:append="() => (visibleCode = !visibleCode)"
            counter=16
            label="Alarm Code"
          ></v-text-field>
          <v-switch v-model="deviceInfo.alarm" class="ma-2" label="Toggle Alarm"></v-switch>
          <v-switch v-model="deviceInfo.vflip" class="ma-2" label="Vertically flip camera"></v-switch>
          <v-btn class="mr-4" type="submit">submit</v-btn>
        </v-form>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import gql from "graphql-tag";
import { mapActions } from "vuex";

export default {
  name: "Device",
  apollo: {
    deviceInfo: gql`
      query {
        deviceInfo {
          alarm
          pollInterval
          alertInterval
          alarmDuration
          email
          vflip
          motd
          alarmCode
        }
      }
    `
  },

  data() {
    return {
      visibleCode: false
    };
  },

  methods: {
    ...mapActions(["sendError", "sendSuccess"]),
    updateDeviceSettings: function() {
      this.$apollo
        .mutate({
          // Query
          mutation: gql`
            mutation(
              $pollInterval: Int
              $alertInterval: Int
              $alarmDuration: Int
              $alarm: Boolean
              $email: String
              $vflip: Boolean
              $motd: String
              $alarmCode: String
            ) {
              updateDevice(
                pollInterval: $pollInterval
                alertInterval: $alertInterval
                alarmDuration: $alarmDuration
                alarm: $alarm
                email: $email
                vflip: $vflip
                motd: $motd
                alarmCode: $alarmCode
              ) {
                device {
                  alarm
                }
              }
            }
          `,
          variables: {
            pollInterval: this.deviceInfo.pollInterval,
            alertInterval: this.deviceInfo.alertInterval,
            alarmDuration: this.deviceInfo.alarmDuration,
            alarm: this.deviceInfo.alarm,
            email: this.deviceInfo.email,
            vflip: this.deviceInfo.vflip,
            motd: this.deviceInfo.motd,
            alarmCode: this.deviceInfo.alarmCode
          }
        })
        .then(data => {
          this.sendSuccess("Updated Device");
          // Result
          console.log(data);
        })
        .catch(error => {
          this.sendError("Failed to update device");
          // Error
          console.error(error);
        });
    }
  }
};
</script>