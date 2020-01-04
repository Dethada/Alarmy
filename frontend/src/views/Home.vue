<template>
  <v-container>
    <v-row>
      <v-col>
        <p>Temperature Data</p>
      </v-col>
      <v-col align="right" justify="right">
        <v-btn-toggle v-model="tempDuration" color="deep-purple accent-3" mandatory justify-end>
          <v-btn value="RT">Real Time</v-btn>

          <v-btn value="24H">24 Hours</v-btn>

          <v-btn value="7D">7 Days</v-btn>

          <v-btn value="30D">30 Days</v-btn>

          <v-btn value="ALL">All</v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    <line-chart
      :precision="3"
      :data="allTemp"
      suffix="°C"
      xtitle="Time"
      ytitle="Temperature"
      :download="true"
    ></line-chart>
    <v-row>
      <v-col>
        <p>Gas Data</p>
      </v-col>
      <v-col align="right" justify="right">
        <v-btn-toggle v-model="gasDuration" color="deep-purple accent-3" mandatory justify-end>
          <v-btn value="RT">Real Time</v-btn>

          <v-btn value="24H">24 Hours</v-btn>

          <v-btn value="7D">7 Days</v-btn>

          <v-btn value="30D">30 Days</v-btn>

          <v-btn value="ALL">All</v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    <line-chart
      :precision="5"
      :data="gasData"
      suffix="g"
      xtitle="Time"
      ytitle="Parts Per Million (PPM)"
      :download="true"
    ></line-chart>
  </v-container>
</template>

<script>
import gql from "graphql-tag";

export default {
  name: "Home",
  sockets: {
    newValues(data) {
      this.$apollo.queries.allTemp.refetch();
      this.$apollo.queries.allGas.refetch();
    }
  },
  apollo: {
    allGas: {
      query: gql`
        query($duration: String) {
          allGas(duration: $duration) {
            captureTime
            lpg
            co
            smoke
          }
        }
      `,
      variables() {
        return {
          duration: this.gasDuration
        };
      },
      // pollInterval: 60000, // poll every 60 seconds
      update: data => {
        return data.allGas.map(function(edge) {
          return edge;
        });
      }
    },
    allTemp: {
      query: gql`
        query($duration: String) {
          allTemp(duration: $duration) {
            captureTime
            value
          }
        }
      `,
      variables() {
        return {
          duration: this.tempDuration
        };
      },
      // pollInterval: 60000, // poll every 60 seconds
      update: data => {
        return data.allTemp.map(function(edge) {
          return [edge.captureTime + "+08:00", edge.value];
        });
      }
    }
  },
  data() {
    return {
      allGas: [],
      allTemp: [],
      tempDuration: "RT",
      gasDuration: "RT",
    };
  },

  computed: {
    gasData: function() {
      let x = [
        { name: "LPG", data: {} },
        { name: "CO", data: {} },
        { name: "Smoke", data: {} }
      ];
      let lpg = {};
      let co = {};
      let smoke = {};
      this.allGas.forEach(item => {
        let capTime = item.captureTime + "+08:00";
        lpg[capTime] = item.lpg;
        co[capTime] = item.co;
        smoke[capTime] = item.smoke;
      });
      x[0].data = lpg;
      x[1].data = co;
      x[2].data = smoke;
      return x;
    }
  }
};
</script>
