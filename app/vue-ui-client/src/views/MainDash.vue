<script>
import axios from 'axios';
import SpO2chart from '@/components/SpO2chart.vue';
import tempHRBR from '@/components/tempHRBR.vue';
import HRandBRchart from '@/components/HRandBRchart.vue';
import Temperaturechart from '@/components/Temperaturechart.vue';
import BodyPosition from '@/components/BodyPosition.vue';
import BodyDynamics from '@/components/BodyDynamics.vue';
import Location from '@/components/Location.vue';
import HRval from '@/components/HRval.vue';
import BRval from '@/components/BRval.vue';
import alert from '@/components/alerts/alert.vue';

constant HR_ALERT = 150

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

    pollAlert() {
      if (this.$refs.hr.heartrate > HR_ALERT) {
        this.$refs.alert.showModal();
      }
    }
  },
  created() {
    this.getMessage();

    setInterval(function () {
      this.pollAlert();
    }.bind(this), 1000);
  },
  components: {
    SpO2chart, tempHRBR, HRandBRchart, Temperaturechart,
    BodyPosition, Location, HRval, BRval, BodyDynamics, alert
  }
};
</script>

<template>
  <v-container class="align-center justify-center">
    <v-card class="align-center justify-center" color="blue-lighten-3">
      <v-card-title class="align-center"> Prototype
        <v-btn style="float: right"> Reset Device</v-btn>
      </v-card-title>
    </v-card>
    <v-sheet color="blue-lighten-5" rounded class="align-center justify-center">
      <v-row no-gutters>
        <v-col no-gutters>
          <v-container class="ml-n2">
            <v-row>
              <v-col no-gutters>
                <HRval ref="hr"></HRval>
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
              <v-container>
                <SpO2chart></SpO2chart>
              </v-container>
            </v-row>

            <v-row>
              <v-container>
                <Temperaturechart></Temperaturechart>
              </v-container>
            </v-row>

            <v-row>
              <v-container>
                <Location></Location>
              </v-container>
            </v-row>
          </v-container>

        </v-col>

        <v-col no-gutters>
          <v-container class="mt-3 ml-n4">
            <v-row>
              <v-container>
                <BodyPosition></BodyPosition>
              </v-container>
            </v-row>
            <v-row>
              <v-container>
                <BodyDynamics></BodyDynamics>
              </v-container>
            </v-row>
          </v-container>
        </v-col>

      </v-row>
    </v-sheet>
  </v-container>

  <alert ref="alert"></alert>
</template>