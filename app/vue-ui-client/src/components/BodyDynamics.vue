<script>
import axios from 'axios'

export default {
    data() {
        return {
            dynamic: ["Stationary", "Shaking", "Falling"],
            state: "Unknown",
            dyn_val: 0,
        };
    },
    methods: {
        getDynamic() {
            const path = 'http://127.0.0.1:5000/dynamic';
            axios.get(path)
                .then((res) => {
                    this.state = this.dynamic[parseInt(res.data)];
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created: async function () {
        this.getDynamic();

        setInterval(function () {
            this.getDynamic();
        }.bind(this), 1000);
    }
};
</script>

<template>
    <v-card width="225" height="200" class="mt-n3">
        <v-card-title class="text-center"> Body Dynamics </v-card-title>
        <v-container>
            <div class="text-h8 px-3 mt-n4 text-center" v-if="pos_val != 0">
                Patient is currently:
            </div>
        </v-container>
        <v-card-title class="text-center"> {{ state }} </v-card-title>
        <!-- does this mean: in distress v. calm or stationary, walking, agitated-->
    </v-card>
</template>
