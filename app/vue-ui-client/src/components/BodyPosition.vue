<script>
import LD from '@/assets/images/LD.png'
import Sitting from '@/assets/images/Sitting.png'
import Standing from '@/assets/images/Standing.png'
import NoData from '@/assets/images/NoData.png'

import axios from 'axios'

export default {
    data() {
        return {
            LDsrc: LD,
            Sittingsrc: Sitting,
            Standingsrc: Standing,
            NoDatasrc: NoData,
            position: ["none", "lying", "sitting", "standing"],
            time: 0,
            pos_val: 2,
            last_pos: 2
        };
    },
    methods: {
        getPosition() {
            const path = 'http://127.0.0.1:5000/position';
            axios.get(path)
                .then((res) => {
                    this.pos_val = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
            if (this.last_pos != this.pos_val) {
                this.time = 0;
            }
            else {
                this.time += 1;
            }
            this.last_pos = this.pos_val;
        },
    },
    created: async function () {
        this.getPosition();

        setInterval(function () {
            this.getPosition();
        }.bind(this), 1000);
    }
};
</script>

<template>
    <v-card width=225 height="300" class="justify-center align-center">
        <v-card-title class="text-center mb-n4"> Body Postition </v-card-title>
        <v-flex class="align-center justify-center">
            <v-container v-if="pos_val == 1">
                <v-img width=200 :src="LDsrc" class="mt-12 mx-auto"></v-img>
                <div class="text-h8 px-3 text-center"> Laying</div>
            </v-container>
            <v-container v-if="pos_val == 2">
                <v-img width=60 :src="Sittingsrc" class="mx-auto mt-n1"></v-img>
                <div class="text-h8 px-3 text-center"> Sitting</div>
            </v-container>
            <v-container v-if="pos_val == 3">
                <v-img width=60 :src="Standingsrc" class="mx-auto"></v-img>
                <div class="text-h8 px-3 text-center"> Standing</div>
            </v-container>
            <v-container v-if="pos_val == 0">
                <v-img width="150" :src="NoDatasrc" class="mx-auto"></v-img>
                <div class="text-h8 px-3 text-center"> No Data Available</div>
            </v-container>
        </v-flex>
        <v-container>
            <div class="text-h8 px-3 mt-n4 text-center" v-if="pos_val != 0">
                The patient has been {{ position[pos_val] }} for the past {{ time }} seconds.</div>
        </v-container>
    </v-card>
</template>