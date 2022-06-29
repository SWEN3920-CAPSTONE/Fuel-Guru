<template>
  <main id="about-page">
    <div id="left">
      <div id="about-page-info">
        <h1>About Fuel Guru</h1>  
        <p>In response to the rapidly fluctuating fuel prices and the lack of readily available general information on any gas station 
          in Jamaica, the Fuel Guru application allows consumers to quickly view all gas stations near their current location and 
          quickly find the prices of any gas station in Kingston Jamaica. 
        </p>
           </div>
      <div id="about-page-btn">
        <router-link :to="{name: 'Signup'}" id="home-page-btn">Signup Today!</router-link>
        <router-view/>
      </div>
    </div>
  </main>
</template>

<style>
  #about-page-btn {
    padding-top: 30px; 
  }
</style>
