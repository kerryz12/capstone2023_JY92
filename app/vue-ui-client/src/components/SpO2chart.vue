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
    <v-card color ="red" width = 250 class = "my-3">
        <v-card-title class = "text-center"> Blood Oxygenation</v-card-title>
            <apexchart type="radialBar" height="200" :options="chartOptions" :series="series"></apexchart>
    </v-card>
</template>