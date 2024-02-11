<script>
import axios from 'axios';
import { setTransitionHooks } from 'vue';

export default {
    name: 'MainDash',
    data() {
        return {
            msg: '',
            options: {
                chart: {
                    id: 'vuechart-example'
                },
                xaxis: {
                    categories: []
                }
            },
            series: [{
                name: 'series-1',
                data: []
            }]
        };
    },
    methods: {
        getHR() {
            const path = 'http://127.0.0.1:5000/heartrate';
            axios.get(path)
                .then((res) => {
                    if (this.series[0].data.length >= 16) {
                        this.series[0].data.shift();
                        this.series[0].data.push(res.data)
                    }
                    else {
                        this.series[0].data.push(res.data)
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created: async function () {
        this.getHR();
        this.getTime();

        setInterval(function () {
            this.getHR();
            this.getTime();
        }.bind(this), 1000);
    }
}
</script>

<template>
    <v-card max-width=600 class="mt-n3 mx-3 mb-3">
        <v-card-title class="text-center"> Heart Rate and Breathing Rate Chart</v-card-title>
        <apexchart width="600" type="line" :options="options" :series="series"></apexchart>
    </v-card>
</template>