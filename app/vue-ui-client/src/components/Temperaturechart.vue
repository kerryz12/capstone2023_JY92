<script>
export default {
    data() {
        return {
          series: [76],
          chartOptions: {
            chart: {
              type: 'radialBar',
              offsetY: -20,
              sparkline: {
                enabled: true
              }
            },
            plotOptions: {
              radialBar: {
                startAngle: -90,
                endAngle: 90,
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
                dataLabels: {
                  name: {
                    show: false
                  },
                  value: {
                    offsetY: -2,
                    fontSize: '22px'
                  }
                }
              }
            },
            grid: {
              padding: {
                top: -10
              }
            },
            fill: {
              type: 'gradient',
              gradient: {
                shade: 'light',
                shadeIntensity: 0.4,
                inverseColors: false,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 50, 53, 91]
              },
            },
            labels: ['Average Results'],
          },
        }
      }
    }
</script>

<template>
    <v-card color ="purple" width = 250 class="mt-n3">
        <v-card-title class ="text-center"> Temperature </v-card-title>
        <apexchart type="radialBar" :options="chartOptions" :series="series"></apexchart>
    </v-card>
</template>