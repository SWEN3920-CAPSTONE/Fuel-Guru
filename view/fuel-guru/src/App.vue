<template>
  <header>
      <nav>
        <router-link :to="{name: 'Home'}" id="hme">Home</router-link>
        <router-link :to="{name: 'About'}" id="abt">About Us</router-link>
        <router-link :to="{name: 'Map'}" id="map">View Map</router-link>
        <router-link :to="{name: 'FuelPrices'}" id="fp">Fuel Prices</router-link>
        <router-link :to="{name: 'Home'}" id="logout" v-if="loggedIn" @click.stop.prevent="logoutUser">Logout</router-link>
        <router-link :to="{name: 'Signup'}" id="signup" v-else>Signup / Login</router-link>
        <!-- if the refresh_token is not empty then the user is logged in and can see the logout button -->
        <!-- <router-link :to="{name: 'Home'}" id="logout" >Logout</router-link> -->
      </nav>
  <router-view @update="checkloggedIn"/>
  </header>
</template>

<script setup>
import {ref} from 'vue';
import router from './router';

var loggedIn = ref('');

function checkloggedIn() {
  if (localStorage.getItem('refreshToken') !== null) {
    loggedIn.value = true;
  } else {
    loggedIn.value = false;
  }
}

function logoutUser() {
    loggedIn.value = false;
    localStorage.removeItem('refreshToken');
    router.push({name: 'Home'});
    alert(`You are logged out!`);
}
</script>


<style>
@import '@/assets/base.css';

#signup, #logout {
  border: 2px solid #AA1414;
  border-radius: 5px;
  padding: 5px;
}

#hme, #abt, #fp, #map {
  padding-right: 50px;
}
</style>
