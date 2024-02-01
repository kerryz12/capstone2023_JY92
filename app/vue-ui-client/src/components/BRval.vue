<script>
import BR from '@/assets/images/BR.png'
import axios from 'axios'

export default {
    data() {
        return {
            BRsrc: BR,
            breath: 0
        };
    },
    methods: {
        getMessage() {
            const path = 'http://localhost:5000/heartrate';
            axios.get(path)
                .then((res) => {
                    this.breath = res.data[3];
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
};
</script>


<template>
    <v-card color="orange" max-width=500 class="ml-n4 mr-4 mt-4 px-1 pt-1">
        <v-row>
            <v-col no-gutters>
                <v-img width=50 :src="BRsrc" class="ma-auto"></v-img>
            </v-col>
            <v-col no-gutters>
                <v-row>
                    <v-card-title class="pl-0"> Current Breathing Rate: </v-card-title>
                </v-row>
                <v-row>
                    <v-card-title class="mx-auto mt-n6">{{ breath }}</v-card-title>
                </v-row>
            </v-col>
        </v-row>
    </v-card>
</template>