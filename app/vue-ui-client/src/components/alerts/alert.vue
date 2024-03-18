<script>
import Warning from '@/assets/images/Warn.png'

export default {
  data() {
    return {
      Warnsrc: Warning,
      isModalVisible: true,
    };
  },
  methods: {
    showModal() {
      this.isModalVisible = true;
    }
  }
};

</script>

<template>
  <transition name="modal-fade" v-if="isModalVisible" class="shake">
    <div class="modal-backdrop">
      <v-card>
        <v-img height="100" :src="Warnsrc"></v-img>
        <v-card-title class="text-center"> Please check on patient!</v-card-title>
        <v-sheet width=400>
          <p class="text-body-1 text-center"> The wearable health status monitoring system
            has detected that the patient is in distress.</p>
        </v-sheet>
        <v-btn style="float: right;" variant="text" @click="isModalVisible = false" class="text-button"
          color="red-lighten-1">OK</v-btn>
      </v-card>
    </div>
  </transition>
</template>

<style>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(247, 141, 141, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.shake {
  animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
}

@keyframes shake {

  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>