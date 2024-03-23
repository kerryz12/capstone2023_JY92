<script>
import HR from '@/assets/images/HR.png'
import axios from 'axios'

export default {
    data() {
        return {
            HRsrc: HR,
            heartrate: '75',
            calibration_counter: 0,
        };
    },
    methods: {
        getHR() {
            const path = 'http://127.0.0.1:5000/heartrate';
            axios.get(path)
                .then((res) => {
                    if (this.calibration_counter > 4) this.heartrate = res.data;
                    else this.calibration_counter += 1;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created: async function () {
        this.getHR();

        setInterval(function () {
            this.getHR();
        }.bind(this), 1000);
    }
};

</script>


<template>
    <v-card max-width=275 class="ml-4 mt-4 px-1 pt-1">
        <v-row>
            <v-col no-gutters>
                <v-img width=43 :src="HRsrc" class="ml-2 mr-1"></v-img>
            </v-col>
            <v-col no-gutters>
                <v-row>
                    <v-card-title class="pl-0"> Current Heart Rate: </v-card-title>
                </v-row>
                <v-row>
                    <v-card-title class="mx-auto mt-n6">{{ heartrate }}</v-card-title>
                </v-row>
            </v-col>
        </v-row>
    </v-card>
</template>