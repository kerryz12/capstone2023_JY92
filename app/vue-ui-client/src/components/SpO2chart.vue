<script>
import axios from 'axios'

export default {
    data() {
        return {
            series: [0],
            chartOptions: {
                chart: {
                    height: 300,
                    type: 'radialBar',
                },
                plotOptions: {
                    radialBar: {
                        hollow: {
                            size: '0%',
                        }
                    },
                },
                labels: ['SpO2 Level'],
            },
        }
    },
    methods: {
        getSPO2() {
            const path = 'http://127.0.0.1:5000/spo2';
            axios.get(path)
                .then((res) => {
                    this.series[0] = res.data;
                    this.chartOptions.plotOptions.radialBar.hollow.size = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created: async function () {
        this.getSPO2();

        setInterval(function () {
            this.getSPO2();
        }.bind(this), 500);
    }
}
</script>

<template>
    <v-card color="red" width=250 class="justify-center align-center" height=225>
        <v-card-title class="text-center mb-n4"> Blood Oxygenation</v-card-title>
        <apexchart type="radialBar" height="225" :options="chartOptions" :series="series"></apexchart>
    </v-card>
</template>