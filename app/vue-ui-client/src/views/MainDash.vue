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

const HR_ALERT_THRESHOLD_UPPER = 150
const BR_ALERT_THRESHOLD_UPPER = 24
const SPO2_ALERT_THRESHOLD_UPPER = 105
const TEMP_ALERT_THRESHOLD_UPPER = 40

const HR_ALERT_THRESHOLD_LOWER = 30
const BR_ALERT_THRESHOLD_LOWER = 6
const SPO2_ALERT_THRESHOLD_LOWER = 90
const TEMP_ALERT_THRESHOLD_LOWER = 34

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
      if (this.$refs.hr.heartrate > HR_ALERT_THRESHOLD_UPPER || this.$refs.hr.heartrate < HR_ALERT_THRESHOLD_LOWER) {
        this.$refs.alert.showModal("Heartrate");
      }
      else if (this.$refs.br.breath > BR_ALERT_THRESHOLD_UPPER || this.$refs.br.breath < BR_ALERT_THRESHOLD_LOWER) {
        this.$refs.alert.showModal("Breathing");
      }
      else if (this.$refs.spo2.series[0] > SPO2_ALERT_THRESHOLD_UPPER || this.$refs.spo2.series[0] < SPO2_ALERT_THRESHOLD_LOWER) {
        this.$refs.alert.showModal("Blood SPO2");
      }
      else if (this.$refs.temperature.temperature > TEMP_ALERT_THRESHOLD_UPPER || this.$refs.temperature.temperature < TEMP_ALERT_THRESHOLD_LOWER) {
        this.$refs.alert.showModal("Temperature");
      }
    }
  },
  created() {
    this.getMessage();

    setInterval(function () {
      this.pollAlert();
    }.bind(this), 10000);
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
                <BRval ref="br"></BRval>
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
                <SpO2chart ref="spo2"></SpO2chart>
              </v-container>
            </v-row>

            <v-row>
              <v-container>
                <Temperaturechart ref="temperature"></Temperaturechart>
              </v-container>
            </v-row>

            <v-row>
              <v-container>
                <Location ref="location"></Location>
              </v-container>
            </v-row>
          </v-container>

        </v-col>

        <v-col no-gutters>
          <v-container class="mt-3 ml-n4">
            <v-row>
              <v-container>
                <BodyPosition ref="position"></BodyPosition>
              </v-container>
            </v-row>
            <v-row>
              <v-container>
                <BodyDynamics ref="dynamics"></BodyDynamics>
              </v-container>
            </v-row>
          </v-container>
        </v-col>

      </v-row>
    </v-sheet>
  </v-container>

  <alert ref="alert"></alert>
</template>