<script>
import LD from '@/assets/images/LD.png'
import Sitting from '@/assets/images/Sitting.png'
import Standing from '@/assets/images/Standing.png'
import NoData from '@/assets/images/NoData.png'

export default {
    data() {
        return {
            LDsrc: LD,
            Sittingsrc: Sitting,
            Standingsrc: Standing,
            NoDatasrc: NoData,
            LD: true,
            sit: false,
            stand: false,
            notavail: false,
            position: ["notavail", "laying", "sitting", "standing"],
            time: 30,
            pos_val: 0
        };
    }
};
</script>


<template>
    <v-card color ="pink" width = 225 height="400" class = "justify-center align-center">
        <v-card-title class = "text-center mb-n4"> Body Postition </v-card-title>
        <v-flex class="align-center justify-center">
            <v-container v-if="LD">
                <v-img width = 200 :src = "LDsrc" class = "mt-12 mx-auto" v-if="LD"></v-img>
                <h4 class = "text-center"> Laying</h4>
            </v-container>
            <v-container v-if="sit">
                <v-img width = 65 :src = "Sittingsrc" class="mx-auto" v-if="sit"></v-img>
                <h4 class = "text-center"> Sitting</h4>
            </v-container>
            <v-container v-if="stand">
                <v-img width = 65 :src = "Standingsrc" class="mx-auto" v-if="stand"></v-img>
                <h4 class = "text-center"> Standing</h4>
            </v-container>
            <v-container v-if="notavail">
                <v-img width="150" :src = "NoDatasrc" class="mx-auto" v-if="notavail"></v-img>
                <h4 class = "text-center"> No Data Available</h4>
            </v-container>
        </v-flex> 
        <v-container>
            <h4 class = "text-center" v-if="pos_val != 0 "> 
                The patient has been {{ position[pos_val] }} for the past {{ time }} minutes.</h4>
        </v-container>
     </v-card>
</template>