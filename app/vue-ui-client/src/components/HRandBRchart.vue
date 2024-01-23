
<script>
new Vue({
    el: '#app',
    components: {
      apexchart: VueApexCharts,
    },
    data: {
      
      series: [{
        data: data.slice()
      }],
      chartOptions: {
        chart: {
          id: 'realtime',
          height: 350,
          type: 'line',
          animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
              speed: 1000
            }
          },
          toolbar: {
            show: false
          },
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        title: {
          text: 'Dynamic Updating Chart',
          align: 'left'
        },
        markers: {
          size: 0
        },
        xaxis: {
          type: 'datetime',
          range: XAXISRANGE,
        },
        yaxis: {
          max: 100
        },
        legend: {
          show: false
        },
      },
      
      
    },
    mounted: function () {
      var me = this
      window.setInterval(function () {
        getNewSeries(lastDate, {
          min: 10,
          max: 90
        })
        
        me.$refs.chart.updateSeries([{
          data: data
        }])
      }, 1000)
    
      // every 60 seconds, we reset the data to prevent memory leaks
      window.setInterval(function () {
        resetData()
        
        me.$refs.chart.updateSeries([{
          data
        }], false, true)
      }, 60000)
    },
  })
</script>

<template>
<div id="chart">
    <apexchart type="line" height="350" ref="chart" :options="chartOptions" :series="series"></apexchart>
</div>
</template>