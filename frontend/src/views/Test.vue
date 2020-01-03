<template>
  <v-container fluid fill-width>
    <v-card>
      <v-container>
        <form>
          <v-switch v-model="alarmStatus" class="ma-2" @click="changeAlarm()" label="Alarm"></v-switch>
        </form>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
// import SocketIO from "socket.io-client";
import { mapActions } from 'vuex'

export default {
  name: "Test",

  sockets: {
    serverMsg(data) {
      this.sendError(data)
    }
  },

  data: () => ({
    alarmStatus: false,  
  }),

  methods: {
      ...mapActions(['sendError']),
    changeAlarm: function() {
      this.$socket.client.emit("alert_users", "stop_alert");
    }
  },
};
</script>