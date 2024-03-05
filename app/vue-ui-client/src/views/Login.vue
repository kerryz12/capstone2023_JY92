<script>
import logo from '@/assets/images/Logo.png'
import router from "@/router";

  export default {
    data() {
      return {
        form: false,
        email: "",
        password: "",
        tryagain: false,
        state: true,
      }
    },
    data() {
        return {
            logosrc: logo,
        };
    },
    methods: {
      submit () {
        if(this.email == "test@wshsm.com" && this.password == "test"){
          router.replace({ path: '/' })
        }
        tryagain = true;
      },
      required (v) {
        return !!v || 'Field is required'
      },
    },
  }
</script>

<template>
  <v-container class="d-flex align-center justify-center ml-80 mt-50"> 
  <v-flex>
    <v-card class="align-center justify-center" color ="blue-lighten-3" width="600">
        <v-card-title> Sign In</v-card-title>
    </v-card>
    <v-sheet width="600" class="align-center justify-center">
      <v-row align-center justify-center>
        <v-container class="align-center justify-center mt-4">
          <v-form v-model="form" @prevent.submit='submit'>
          <v-text-field
            v-model="email"
            :rules="[required]"
            type = 'email'
            class="mb-2"
            clearable
            label="Email"
          > </v-text-field>

          <v-text-field
            v-model="password"
            :rules="[required]"
            type ='password'
            clearable
            label="Password"
            placeholder="Enter your password"
          ></v-text-field>

        <br>

          <v-btn
            :disabled="!form"
            block
            color="primary"
            size="large"
            type="submit"
            variant="elevated"
            @click="submit"
          >
            Sign In
          </v-btn>
      </v-form>
      <v-row>
        <v-container>
          <v-img width ='200' :src = "logosrc" class = "mt-6 mx-auto"></v-img>
        </v-container>
      </v-row>
    </v-container>
    </v-row>
      <v-container>  
        <div class = "text-caption px-3 mt-n2 text-center"> Images from Flaticon </div> 
        <div class = "text-h8 px-3 mt-2 text-center"> 
          For login assistance, please visit your organization's IT department. </div> 
      </v-container>
    </v-sheet>
  </v-flex>
  </v-container>
</template>
  
 
  