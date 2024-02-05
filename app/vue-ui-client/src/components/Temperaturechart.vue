<script>
import axios from 'axios'

export default {
    data() {
        return {
            temperature: 50,
        }
    },
    methods: {
        getTemp() {
            const path = 'http://127.0.0.1:5000/temperature';
            axios.get(path)
                .then((res) => {
                    this.temperature = res.data;
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
        <v-card-title class ="text-center blue-text"> {{temperature}} &deg;C </v-card-title>
    </v-card>
</template>