<template>
  <main id="home-page">
    <div id="left">
      <div id="left-heading">
        <h1>Welcome to <br> Fuel Guru</h1>    
      </div>    
      <div id="left-paragraph">
        <p>

          Wondering what gas prices around you are like? Look no further!
          In response to the rapidly fluctuating fuel prices and the lack of readily available general information on any gas station 
          in Jamaica, the Fuel Guru application allows consumers to quickly view all gas stations near their current location and 
          quickly find the prices of any gas station in Kingston Jamaica. 


        </p>
        </div>
      <div id="left-button">
        <router-link :to="{name: 'Login'}" id="home-page-btn">Signup / Login</router-link>
        <router-view/>
      </div>
    </div>
    <div id="right">
      <img src="@/assets/home_image1.jpg" alt="Fuel Guru Image" id="home-img">
    </div>
  </main>
</template>

<style>
  #home-page {
    display: grid;
    grid-template-columns: auto auto;
    column-gap: 160px;
  }

  #left {
    text-align: left;
  }

  h1 {
    font-size: 60px;
    text-align: left;
  }

  #home-page-btn {
    border: 2px solid #AA1414;
    border-radius: 25px;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: #AA1414;
    color: white;
  }

  #left-button {
    padding-top: 30px;
  }

  #home-img {
    height: 80%;
  }
</style>