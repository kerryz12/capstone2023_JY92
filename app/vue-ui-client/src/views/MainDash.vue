  <script>
  import axios from 'axios';
  import SpO2chart from '@/components/SpO2chart.vue';
  import tempHRBR from '@/components/tempHRBR.vue';
  import Temperaturechart from '@/components/Temperaturechart.vue';
  import BodyPosition from '@/components/BodyPosition.vue';
  
  export default {
    name: 'MainDash',
    data() {
        return {
        };
    },
    methods: {
        getMessage() {
            const path = 'http://localhost:5001/';
            axios.get(path)
                .then((res) => {
                this.msg = res.data;
            })
                .catch((error) => {
                console.error(error);
            });
        },
    },
    created() {
        this.getMessage();
    },
    components: { SpO2chart, tempHRBR, Temperaturechart, BodyPosition }
};
  </script>

<template>
  <v-container class="align-center justify-center"> 
    <v-card class="align-center justify-center" color ="blue-lighten-3"> 
      <v-card-title class="align-center"> Prototype 
        <v-btn style="float: right" > Reset Device</v-btn>
      </v-card-title>
    </v-card>
      <v-sheet color = "yellow" rounded class="align-center justify-center">
        <v-row no-gutters>
          <v-col no-gutters>
            <v-container>
              <tempHRBR></tempHRBR>
            </v-container>
          </v-col>
          <v-col>
        <v-row>
          <v-container>
            <SpO2chart></SpO2chart>
          </v-container>
        </v-row>
        <v-row>
          <v-container>
            <Temperaturechart></Temperaturechart>
          </v-container>
        </v-row>
      </v-col>
      <v-col>
      <v-row>
        <v-container>
          <BodyPosition></BodyPosition>
        </v-container>
      </v-row>
      <v-row>
        <v-container>
        <v-card color ="green" max-width = 250>
        <v-btn>hi</v-btn>
        </v-card>
        </v-container>
      </v-row>
      </v-col>
      </v-row>
      </v-sheet>
  </v-container>
</template>