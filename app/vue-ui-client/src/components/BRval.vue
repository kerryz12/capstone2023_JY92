<script>
import BR from '@/assets/images/BR.png'

export default {
    data() {
        return {
            BRsrc: BR,
            breath: 99
        };
    }
};
</script>


<template>
    <v-card color ="orange" max-width = 500 class="ml-n4 mr-4 mt-4 px-1 pt-1">
        <v-row>
            <v-col no-gutters>
                <v-img width = 50 :src = "BRsrc" class = "ma-auto"></v-img>
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