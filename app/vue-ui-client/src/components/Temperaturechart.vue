<script>
import axios from 'axios'

export default {
    data() {
        return {
            chart: {
                type: 'bar',
                dataLabels: {
                    enabled: true,
                    dropShadow: {
                        enabled: true,
                        left: 2,
                        top: 2,
                        opacity: 0.5
                    }
                }
            },
            series: [{
                data: [{
                    x: 'Temperature',
                    y: 10
                }]
            }]
        }
    },
    methods: {
        getTemp() {
            const path = 'http://127.0.0.1:5000/temperature';
            axios.get(path)
                .then((res) => {
                    this.series[0].data[0].y = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created: async function () {
        this.getTemp();

        setInterval(function () {
            this.getTemp();
        }.bind(this), 500);
    }
}
</script>

<template>
    <v-card width = 250 class="mt-n3">
        <v-card-title class ="text-center"> Temperature </v-card-title>
        <apexchart type="radialBar" :options="chartOptions" :series="series"></apexchart>
    </v-card>
</template>