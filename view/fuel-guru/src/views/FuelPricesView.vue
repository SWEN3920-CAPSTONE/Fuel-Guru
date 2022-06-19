<template>
<main id='fuelprices-area'>
  <div id='cheapest-prices'>
    <div id='cheapest-87'>
      <div id='cheapest-87-h'>
        <h2>Lowest <br> E-10 87 Fuel</h2>
      </div>      
      <div>
        <p> {{cheapest87Info.name}} <br> {{cheapest87Info.address}} <br> ${{cheapest87Info.price}}</p>
        <button @click.stop.prevent='goToGasStation(cheapest87Info.id)'>View Location</button>
      </div>
    </div>
    <div id='cheapest-90'>
      <div id='cheapest-90-h'>
        <h2>Lowest <br> E-10 90 Fuel</h2>
      </div>      
      <div>
        <p> {{cheapest90Info.name}} <br> {{cheapest90Info.address}} <br> ${{cheapest90Info.price}}</p>
        <button @click.stop.prevent='goToGasStation(cheapest90Info.id)'>View Location</button>
      </div>
    </div>
    <div id='cheapest-d'>
      <div id='cheapest-d-h'>
        <h2>Lowest <br>Diesel Fuel</h2>
      </div>      
      <div>
        <p> {{cheapestDieselInfo.name}} <br> {{cheapestDieselInfo.address}} <br> ${{cheapestDieselInfo.price}}</p>
        <button @click.stop.prevent='goToGasStation(cheapestDieselInfo.id)'>View Location</button>
      </div>
    </div>
    <div id='cheapest-sd'>
      <div id='cheapest-sd-h'>
        <h2>Lowest <br> ULSD Fuel</h2>
      </div>      
      <div>
        <p> {{cheapestULSDInfo.name}} <br> {{cheapestULSDInfo.address}} <br> ${{cheapestULSDInfo.price}}</p>
        <button @click.stop.prevent='goToGasStation(cheapestULSDInfo.id)'>View Location</button>
      </div>
    </div>
  </div>
  <div id='search-area'>     
    <input type='text'  id='search-fp' placeholder='Search..' v-model='searchBar'>
    <button id='search-btn' @click.stop.prevent='getGasStations'>Search</button>
  </div>
  <div id='filter-area'>    
    <label for='parish'>PARISH: </label>
    <select id='parish' v-model='parish'>
      <option disabled>Please select one</option>
      <option>Clarendon</option>
      <option>Hanover</option>
      <option>Kingston & St. Andrew</option>
      <option>Manchester</option>
      <option>Portland</option>
      <option>St. Ann</option>
      <option>St. Catherine</option>
      <option>St. Elizabeth</option>
      <option>St. James</option>
      <option>St. Mary</option>
      <option>St. Thomas</option>
      <option>Trelawny</option>
      <option>Westmoreland</option>
    </select>
    <label for='sortby'>SORT BY: </label>
    <select id='sortby' v-model='sortby'> 
      <option disabled>Please select one</option>
      <option>Price</option>
      <option>Location</option>
    </select>
  </div>  
  <div id='results-area'>           
    <!-- v-for to display results -->  
    <li v-for='gasStation in response.value' :key='gasStation'> 
    <router-link :to="{ name: 'GasStation', params: { id: gasStation.id } }">
      <div id='lst-item'>
        <div>
          <!-- for image -->
          <img src='@/assets/other.jpg' alt='Gas Station Image' id='other'>
          </div>
          <div>
            <h3>{{ gasStation.name.toUpperCase() }}</h3>
            <p>
              {{ gasStation.address }} 
            </p>
          </div>
          <div>
            <p v-if="best87Price !== null"> <b>E-10 87 Fuel</b> &nbsp;&nbsp;&nbsp; ${{ best87Price }}</p>
            <p v-else-if="best90Price !== null"> <b>E-10 90 Fuel</b> &nbsp;&nbsp;&nbsp; ${{ best90Price }}</p>
            <p v-else-if="bestDieselPrice !== null"> <b>Deisel Fuel</b> &nbsp;&nbsp;&nbsp; ${{ bestDieselPrice }}</p>
            <p v-else-if="bestULSDPrice !== null"> <b>ULSD Fuel</b> &nbsp;&nbsp;&nbsp; ${{ bestULSDPrice }} </p>
            <p v-else></p>
          </div>
      </div>   
      </router-link>
    </li> 
    </div>    
</main>  
</template>

<script setup>
import { ref, computed } from 'vue';
import router from '../router/index.js';

var searchBar = ref(''); 
var parish = ref(''); 
var sortby = ref(''); 
var response = {}; 
var cheapestPricesObject = {};
var cheapest87 = ref({});
var cheapest90 = ref({});
var cheapestDiesel = ref({});
var cheapestULSD = ref({});
var bestPrices87= ref(null);
var bestPrices90 = ref(null);
var bestPricesDiesel = ref(null);
var bestPricesULSD = ref(null);

getCheapestPrices();

//computed references to be displayed in the template
const cheapest87Info = computed(() => cheapest87.value);
const cheapest90Info = computed(() => cheapest90.value);
const cheapestDieselInfo = computed(() => cheapestDiesel.value);
const cheapestULSDInfo = computed(() => cheapestULSD.value);
const best87Price = computed(() => bestPrices87.value);
const best90Price = computed(() => bestPrices90.value);
const bestDieselPrice = computed(() => bestPricesDiesel.value);
const bestULSDPrice = computed(() => bestPricesULSD.value);


/**
 * @returns the gas stations with the cheapest prices for each gas type
 */
function getCheapestPrices() {
  fetch('http://localhost:9000/gasstations/top', {
    method: 'GET'
  })
  .then(result => result.json())
  .then(data => {
    //console.log(data);
    cheapestPricesObject.value = data.data;
    //console.log(data.data[0].gas_post.gas_station.name);

    for (let i = 0; i < cheapestPricesObject.value.length; i++) {
      let gasType = cheapestPricesObject.value[i].gas_type.gas_type_name;
      let gasPrice = cheapestPricesObject.value[i].price;
      let gasStationInfo = cheapestPricesObject.value[i].gas_post.gas_station;

      /*
      console.log(data.data[0].gas_post.gas_station.name);
      console.log(gasType);
      console.log(gasPrice);
      console.log(gasStationInfo);*/

      if (gasType === '87') {
        cheapest87.value = gasStationInfo;
        cheapest87.value['price'] = parseFloat(gasPrice).toFixed(2);
      }
      if (gasType === '90') {
        cheapest90.value = gasStationInfo;
        cheapest90.value['price'] = parseFloat(gasPrice).toFixed(2);
      }
      if (gasType === 'Diesel') {
        cheapestDiesel.value = gasStationInfo;
        cheapestDiesel.value['price'] = parseFloat(gasPrice).toFixed(2);        
      }
      if (gasType === 'ULSD') {
        cheapestULSD.value = gasStationInfo;
        cheapestULSD.value['price'] = parseFloat(gasPrice).toFixed(2);
      }
    }
  })
  .catch(error => {
    console.log(error)
  })
}

/**
 * @returns the gas station data for each gas station that matches the word in the search bar
 */
function getGasStations() {
  if (searchBar.value !=='') {
    fetch( import.meta.env.VITE_HEROKULINK + '/gasstations/search', {
      body: JSON.stringify({
        'name': searchBar.value
      }),
      method: 'POST'
    })
    .then(result => result.json())
    .then(data => {
      searchBar.value = ''; //not sure why this doesn't work without it being cleared
      response.value = data.data;

      // getting the best prices for each gas type
      for (let i = 0; i < response.value.length; i++) {
        bestPrices87.value = null;
        bestPrices90.value = null;
        bestPricesDiesel.value = null;
        bestPricesULSD.value = null;
        let gasInfo = response.value[i].current_best_price.gases;

        if (gasInfo !== null) {
          for (let j = 0; j < gasInfo.length; j++) {
            let gasType = gasInfo[j].gas_type.gas_type_name;
            let gasPrice = gasInfo[j].price;
            
            if (gasType === '87') {
              bestPrices87.value = parseFloat(gasPrice).toFixed(2);
            }
            if (gasType === '90') {
              bestPrices90.value = parseFloat(gasPrice).toFixed(2);
            }
            if (gasType === 'Diesel') {
              bestPricesDiesel.value = parseFloat(gasPrice).toFixed(2);      
            }
            if (gasType === 'ULSD') {
              bestPricesULSD.value = parseFloat(gasPrice).toFixed(2);
            }
          }
        } 
      }
    })
    .catch(error => {
      console.log(error)
    })
  } else {
    fetch('http://localhost:9000/gasstations', {
      method: 'GET'
    })
    .then(result => result.json())
    .then(data => {
      searchBar.value = ' ';
      searchBar.value = '';
      response.value = data.data;
      
      // getting the best prices for each gas type
      for (let i = 0; i < response.value.length; i++) {
        bestPrices87.value = null;
        bestPrices90.value = null;
        bestPricesDiesel.value = null;
        bestPricesULSD.value = null;
        let gasInfo = response.value[i].current_best_price.gases;

        if (gasInfo !== null) {
          for (let j = 0; j < gasInfo.length; j++) {
            let gasType = gasInfo[j].gas_type.gas_type_name;
            let gasPrice = gasInfo[j].price;
            
            if (gasType === '87') {
              bestPrices87.value = parseFloat(gasPrice).toFixed(2);
            }
            if (gasType === '90') {
              bestPrices90.value = parseFloat(gasPrice).toFixed(2);
            }
            if (gasType === 'Diesel') {
              bestPricesDiesel.value = parseFloat(gasPrice).toFixed(2);      
            }
            if (gasType === 'ULSD') {
              bestPricesULSD.value = parseFloat(gasPrice).toFixed(2);
            }
          }
        } 
      }
   })
    .catch(error => {
      console.log(error)
    })
  }
}

/**
 * 
 * @param {integer} id 
 * Allows the user to get directions to the gas station with the best prices.
 */
function goToGasStation (id) {
  router.push('/route/' + id);
}
</script>

<style>
main {
  padding-top: 50px; 
  color: black;
  font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; 
}

#results-area {
  margin-left: 80px;
  margin-right: 80px;
}

#fuelprices-area {
  display: block;
  padding-bottom: 20px;
}

#cheapest-prices {
  display: grid;  
  grid-template-columns: auto auto auto auto ;
  text-align: center;
  column-gap: 100px;
}

#cheapest-87, #cheapest-90, #cheapest-d, #cheapest-sd {
  border: 2px solid #AA1414;
  border-radius: 25px;
  padding-bottom: 15px;
}

#cheapest-87-h, #cheapest-90-h, #cheapest-d-h, #cheapest-sd-h {
  padding-left: 20px;
  padding-right: 20px;
}

#cheapest-87 h2, #cheapest-90 h2, #cheapest-d h2, #cheapest-sd h2 {
  border-bottom: 2px solid #AA1414;
}

#search-area {
  padding-top: 70px;
  text-align: center;
  padding-bottom: 20px;
}

#filter-area {
  padding-top: 30px;
  text-align: center;
  padding-bottom: 20px;
}
  
#search-fp {
  width: 500px;
}

#search-btn {
  border: 2px solid #AA1414;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 3%;
  padding-right: 3%;
  color: white;
  background-color: #AA1414;
  border-radius: 5px;
}

#cheapest-prices button {
  border: 2px solid #AA1414;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 3%;
  padding-right: 3%;
  color: white;
  background-color: #AA1414;
  border-radius: 25px;
}

#lst-item:hover {
  color: #AA1414;
}

label {
  padding-right: 5px;
  padding-left: 30px;
}

#other{
  height: 80px;
}

</style>
