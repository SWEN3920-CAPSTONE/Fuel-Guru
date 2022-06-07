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
      </nav>
  <router-view @update="checkloggedIn"/>
  </header>
</template>


<script setup>
import {ref} from 'vue';
import router from './router';

var loggedIn = ref('');

/**
 * Checks if the user is still logged in if the refresh token they were 
 * given upon successfully logging in is still stored in local storage
 */
function checkloggedIn() {
  if (localStorage.getItem('accessToken') !== null) {
    loggedIn.value = true;
  } else {
    loggedIn.value = false;
  }
}

/**
 * Allows the user to log out and clear the local storgae of their 
 * refresh token
 */
function logoutUser() {
  //console.log(localStorage.getItem('accessToken'));
  fetch('http://localhost:9000/auth/logout', {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.refreshToken}`
    }
    })
    .then(result => result.json())
    .then(data => {
      //console.log(data);           
      loggedIn.value = false;
      //the data.refresh_token should be in local storage 
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      router.push({name: 'Home'}); 
    })
    .catch(error => {
      console.log(error);        
    })    
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

#logout.router-link-exact-active { 
  color: black;
  text-decoration: none;
}

#logout:hover { 
  color: #AA1414;
  text-decoration: underline;
}
</style>
