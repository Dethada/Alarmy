<template>
  <v-container>
    <p>Temperature Data</p>
    <line-chart :precision="3" :data="allTemp" suffix="°C" xtitle="Time" ytitle="Temperature" :download="true"></line-chart>
    <p>Gas Data</p>
    <line-chart :precision="5" :data="gasData" suffix="g" xtitle="Time" ytitle="Parts Per Million (PPM)" :download="true"></line-chart>
  </v-container>
</template>

<script>
import gql from "graphql-tag";

export default {
  name: "Home",
  apollo: {
    allGas: {
      query: gql`
        query($last: Int!) {
          allGas(last: $last) {
            edges {
              node {
                captureTime
                lpg
                co
                smoke
              }
            }
          }
        }
      `,
      variables: {
        last: 10,
      },
      pollInterval: 60000, // poll every 60 seconds
      update: data => {
        return data.allGas.edges.map(function(edge) {
          return edge.node;
        });
      }
    },
    allTemp: {
      query: gql`
        query($last: Int!) {
          allTemp(last: $last) {
            edges {
              node {
                captureTime
                value
              }
            }
          }
        }
      `,
      variables: {
        last: 10,
      },
      pollInterval: 60000, // poll every 60 seconds
      update: data => {
        return data.allTemp.edges.map(function(edge) {
          return [edge.node.captureTime + '+08:00', edge.node.value];
        });
      }
    }
  },
  data() {
    return {
      allGas: [],
      allTemp: [],
    };
  },

  computed: {
    gasData: function() {
      let x = [
        {name: 'LPG', data:{}},
        {name: 'CO', data:{}},
        {name: 'Smoke', data:{}},
      ]
      let lpg = {};
      let co = {};
      let smoke = {};
      this.allGas.forEach(item => {
        let capTime = item.captureTime + '+08:00'
        lpg[capTime] = item.lpg
        co[capTime] = item.co
        smoke[capTime] = item.smoke
      });
      x[0].data = lpg
      x[1].data = co
      x[2].data = smoke
      return x
    }
  },
};
</script>

<style>
.small {
  max-width: 600px;
  margin: 150px auto;
}
</style>
