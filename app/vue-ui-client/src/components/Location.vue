<script>
import axios from "axios";

export default {
  data() {
    return {
      room_val: "0",
      room_string: "Unknown",
    };
  },
  methods: {
    getLocation() {
      const path = "http://127.0.0.1:5000/location";
      axios
        .get(path)
        .then((res) => {
          this.room_val = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
      if (this.room_val == "1") this.room_string = "Room 1";
      else if (this.room_val == "2") this.room_string = "Room 2";
      else if (this.room_val == "3") this.room_string = "Hallway";
      else this.room_string = "Unknown";
    },
  },
  created: async function () {
    this.getLocation();

    setInterval(
      function () {
        this.getLocation();
      }.bind(this),
      1000
    );
  },
};
</script>

<template>
  <v-card width="250" class="mt-n3">
    <v-card-title class="text-center"> Location </v-card-title>
    <v-card-title class="text-center blue-text"> {{ room_string }} </v-card-title>
  </v-card>
</template>
