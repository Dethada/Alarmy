<template>
  <v-snackbar
    v-model="getSnackbar.show"
    :bottom="getSnackbar.bottom"
    :right="getSnackbar.bottom"
    :timeout="getSnackbar.timeout"
  >
    {{ getSnackbar.text }}
    <v-btn :color="getSnackbar.color" text @click="closeSnackbar">Close</v-btn>
  </v-snackbar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Snackbar",
  computed: mapGetters(["getSnackbar"]),
  methods: {
    ...mapActions(["closeSnackbar"])
  }
};
</script>