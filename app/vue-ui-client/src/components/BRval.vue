<script>
import BR from '@/assets/images/BR.png'
import axios from 'axios'

export default {
    data() {
        return {
            BRsrc: BR,
            breath: 10
        };
    },
    methods: {
        getBR() {
            const path = 'http://127.0.0.1:5000/br';
            axios.get(path)
                .then((res) => {
                    this.breath = parseInt(res.data);
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created: async function () {
        this.getBR();

        setInterval(function () {
            this.getBR();
        }.bind(this), 1000);
    }
};
</script>


<template>
    <v-card max-width = 500 class="ml-n4 mr-4 mt-4 px-1 pt-1">
        <v-row>
            <v-col no-gutters>
                <v-img width = 50 :src = "BRsrc" class = "ma-auto "></v-img>
            </v-col>
            <v-col no-gutters>
                <v-row>
                    <v-card-title class="pl-0"> Current Breathing Rate: </v-card-title>
                </v-row>
                <v-row>
                    <v-card-title class="mx-auto mt-n6">{{ breathrate }}</v-card-title>
                </v-row>
            </v-col>
        </v-row>
    </v-card>
</template>