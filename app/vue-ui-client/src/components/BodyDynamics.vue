<script>
export default {
  data() {
    return {
      dynamic: ["stationary", "walking", "agitated"],
      state: "Unknown",
      dyn_val: 0,
    };
  },
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
