<script>
  import axios from 'axios';

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
                    categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
                }
            },
            series: [{
                    name: 'series-1',
                    data: [30, 40, 45, 50, 49, 60, 70, 91]
                }]
        };
    },
}
</script>

<template>
    <v-card max-width = 600 class="mt-n3 mx-3 mb-3">
        <v-card-title class = "text-center"> Heart Rate and Breathing Rate Chart</v-card-title>
        <apexchart width="600" type="line" :options="options" :series="series"></apexchart>
    </v-card>
</template>