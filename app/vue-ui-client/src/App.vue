<script>
import logo from '@/assets/images/Logo.png'

export default {
  name: "App",
  data() {
    return {
      logosrc: logo,
      loginstat: false,
      appTitle: 'A Wearable System for Health Status Monitoring',
      menuItems: [
          { title: 'login', path: '/login', icon: 'face' },
     ]
    }
  },
};
</script>

<template>
  <v-app>
    <v-toolbar color="blue-lighten-4" app>
      <template v-slot:prepend>
        <v-img width="50" :src = "logosrc" class="mx-auto"></v-img>
      </template>   
      <v-toolbar-title color = "blue"> 
        <v-btn variant='plain' to='/' v-if="loginstat==true" size="large">
          {{ appTitle }}
        </v-btn>
        <v-btn variant='plain' to='/login' v-if="loginstat==false" size="large">
          {{ appTitle }}
        </v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn
          flat
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path">
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    
    <v-content>
      <router-view></router-view>
    </v-content>
    
  </v-app>
  <!--<RouterView /> -->
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

