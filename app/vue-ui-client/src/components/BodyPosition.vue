<script>

export default {
    data() {
        return {
            LDsrc: require('@/assets/images/LD.png'),
            // Sittingsrc: require('@/assets/images/Sitting.png'), 
            // Standingsrc: require('@/assets/images/Standing.png')
        };
    }
};
</script>


<template>
    <v-card color ="pink" max-width = 250 class = "pl-0 my-3">
        <img :src="LDsrc">
    </v-card>
</template>