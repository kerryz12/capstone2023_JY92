  <script>
  import axios from 'axios';
  import SpO2chart from '@/components/SpO2chart.vue';
  import tempHRBR from '@/components/tempHRBR.vue';
  import Temperaturechart from '@/components/Temperaturechart.vue';
  import BodyPosition from '@/components/BodyPosition.vue';
  import Location from '@/components/Location.vue';
  import HRval from '@/components/HRval.vue';
  import BRval from '@/components/BRval.vue';
  
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
    components: { SpO2chart, tempHRBR, Temperaturechart, BodyPosition, Location, HRval, BRval }
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
            <v-container class="ml-n2">
              <v-row>
                <v-col no-gutters>
                  <HRval></HRval>
                </v-col>
                <v-col no-gutters>
                  <BRval></BRval>
                </v-col>
              </v-row>
            </v-container>

            <v-container class="ml-n2">
              <v-row>
                <v-container>
                  <tempHRBR></tempHRBR>
                </v-container>
              </v-row>
            </v-container>
          </v-col>
          
          <v-col no-gutters>
          <v-container class="mt-3 ml-n8">
            <v-row>
              <v-container >
                <SpO2chart></SpO2chart>
              </v-container>
            </v-row>
           
            <v-row>
              <v-container >
                <Temperaturechart></Temperaturechart>
              </v-container>
            </v-row>
          </v-container>
          </v-col>
       
          <v-col no-gutters>
          <v-container class="mt-3 ml-n4">
            <v-row>
              <v-container >
                <BodyPosition></BodyPosition>
              </v-container>
            </v-row>
          </v-container>
          </v-col>
          

        </v-row>
      </v-sheet>
  </v-container>
</template>