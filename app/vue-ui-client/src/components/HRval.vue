<script>
import HR from '@/assets/images/HR.png'

export default {
    data() {
        return {
            HRsrc: HR,
            heartrate: 500,
        };
    },
    methods: {
        getMessage() {
            const path = 'http://localhost:5173/';
            axios.get(path)
            .then((res) => {
                this.heartrate = res.data[1];
            })
            .catch((error) => {
                console.error(error);
            });
        },
    },
    created: async function() {
        console.log("hi");
        const response = await fetch("http://localhost:5173/");
        const gObject = await gResponse.json();
        this.heartrate = gObject.heartrate;
    }
};

</script>


<template>
    <v-card color ="teal" max-width = 275 class="ml-4 mt-4 px-1 pt-1">
        <v-row>
            <v-col no-gutters>
                <v-img width = 50 :src = "HRsrc" class = "ma-auto"></v-img>
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