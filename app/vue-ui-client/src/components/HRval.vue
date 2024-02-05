<script>
import HR from '@/assets/images/HR.png'

export default {
    data() {
        return {
            HRsrc: HR,
            heart: 190,
        };
    }
};

</script>


<template>
    <v-card max-width = 275 class="ml-4 mt-4 px-1 pt-1">
        <v-row>
            <v-col no-gutters>
                <v-img width = 43 :src = "HRsrc" class = "ml-2 mr-1"></v-img>
            </v-col>
            <v-col no-gutters>
                <v-row>
                    <v-card-title class="pl-0"> Current Heart Rate: </v-card-title>
                </v-row>
                <v-row>
                    <v-card-title class="mx-auto mt-n6">{{ heart }}</v-card-title>
                </v-row>
            </v-col>
        </v-row> 
    </v-card>
</template>