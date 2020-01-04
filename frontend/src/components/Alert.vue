<template></template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Alert",

  sockets: {
    alert(data) {
      this.sendAlert(data);
    }
  },

  methods: {
    ...mapActions(["sendAlert"])
  }
};
</script>