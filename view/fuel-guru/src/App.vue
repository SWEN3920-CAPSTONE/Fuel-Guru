<script>
import HelloWorld from '@/components/HelloWorld.vue'
</script>

<template>
  <header>
      <nav>
        <router-link :to="{name: 'Home'}" id="hme">Home</router-link>
        <router-link :to="{name: 'About'}" id="abt">About Us</router-link>
        <router-link :to="{name: 'Map'}" id="map">View Map</router-link>
        <router-link :to="{name: 'FuelPrices'}" id="fp">Fuel Prices</router-link>
        <router-link :to="{name: 'Login'}" id="login">Signup / Login</router-link>
      </nav>
  <router-view />
  </header>
</template>

<style>
@import '@/assets/base.css';

#login {
  border: 2px solid #AA1414;
  border-radius: 5px;
  padding: 5px;
}

#hme, #abt, #fp, #map {
  padding-right: 50px;
}
</style>
