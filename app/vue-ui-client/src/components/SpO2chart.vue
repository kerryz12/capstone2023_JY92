<script>
export default {
        data() {
            return {
          series: [70],
          chartOptions: {
            chart: {
              height: 300,
              type: 'radialBar',
            },
            plotOptions: {
              radialBar: {
                track: {
                  background: "#e7e7e7",
                  strokeWidth: '97%',
                  margin: 5, // margin is in pixels
                  dropShadow: {
                    enabled: true,
                    top: 2,
                    left: 0,
                    color: '#999',
                    opacity: 1,
                    blur: 2
                  }
                },
                hollow: {
                  size: '70%',
                }
              },
            },
            labels: ['SpO2 Level'],
          },
        }
        }, 
      }
</script>

<template>
    <v-card width = 250 class = "justify-center align-center" height = 225>
        <v-card-title class = "text-center mb-n4"> Blood Oxygenation</v-card-title>
            <apexchart type="radialBar" height="225" :options="chartOptions" :series="series"></apexchart>
    </v-card>
</template>