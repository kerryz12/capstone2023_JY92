<script>
export default {
    data() {
        return {
            dynamic: ["stationary", "walking", "agitated"],
            dyn_val: 0
        };
    }
};
</script>


<template>
    <v-card width = 225 class="mt-n3">
        <v-card-title class="text-center"> Body Dynamics </v-card-title>
        <div class="text-h8 px-3 mt-1"> Patient is currently: </div>
        <!-- does this mean: in distress v. calm or stationary, walking, agitated-->
    </v-card>
</template>