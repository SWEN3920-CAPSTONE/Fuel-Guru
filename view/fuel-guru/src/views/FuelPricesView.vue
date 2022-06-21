<template>
<main id='fuelprices-area'>
  <div id='cheapest-prices'>
    <div id='cheapest-87'>
      <div id='cheapest-87-h'>
        <h2>Lowest <br> E-10 87 Fuel</h2>
      </div>      
      <div v-if="Object.keys(cheapest87Info).length !== 0">
        <p> {{cheapest87Info.name}} <br> {{cheapest87Info.address}} <br> {{ `$${cheapest87Info.price}` }}</p>        
        <button @click.stop.prevent='goToGasStation(cheapest87Info.id)'>View Location</button>
      </div>  
      <p v-else><br>No posts added today!</p>
    </div>
    <div id='cheapest-90'>
      <div id='cheapest-90-h'>
        <h2>Lowest <br> E-10 90 Fuel</h2>
      </div> 
      <div v-if="Object.keys(cheapest90Info).length !== 0">
        <p> {{cheapest90Info.name}} <br> {{cheapest90Info.address}} <br> {{ `$${cheapest90Info.price}` }}</p>        
        <button @click.stop.prevent='goToGasStation(cheapest90Info.id)'>View Location</button>
      </div>  
      <p v-else><br>No posts added today!</p>
    </div>
    <div id='cheapest-d'>
      <div id='cheapest-d-h'>
        <h2>Lowest <br>Diesel Fuel</h2>
      </div>      
      <div v-if="Object.keys(cheapestDieselInfo).length !== 0"> 
        <p>{{cheapestDieselInfo.name}} <br> {{cheapestDieselInfo.address}} <br> {{ `$${cheapestDieselInfo.price}` }}</p>
        <button @click.stop.prevent='goToGasStation(cheapestDieselInfo.id)'>View Location</button>
      </div>
      <p v-else>No posts added today!</p>
    </div>
    <div id='cheapest-sd'>
      <div id='cheapest-sd-h'>
        <h2>Lowest <br> ULSD Fuel</h2>
      </div>      
      <div v-if="Object.keys(cheapestULSDInfo).length !== 0">
        <p> {{cheapestULSDInfo.name}} <br> {{cheapestULSDInfo.address}} <br> {{ `$${cheapestULSDInfo.price}` }}</p>
        <button @click.stop.prevent='goToGasStation(cheapestULSDInfo.id)'>View Location</button>
      </div>
      <p v-else>No posts added today!</p>
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
      <option>87 Price</option>
      <option>90 Price</option>
      <option>Diesel Price</option>
      <option>ULSD Price</option>
    </select>
  </div>  
  <div id='results-area'>           
    <!-- v-for to display results for each gas station -->  
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
          <div v-if="gasStation.current_best_price !== null">
            <li v-for='gasType in gasStation.current_best_price' :key='gasType'> 
            <p> <b>{{ gasType.gas_type.gas_type_name }}</b> &nbsp;&nbsp;&nbsp; {{ `$${ parseFloat(gasType.price).toFixed(2)}` }}</p>
            </li>
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

getCheapestPrices();

//computed references to be displayed in the template
const cheapest87Info = computed(() => cheapest87.value);
const cheapest90Info = computed(() => cheapest90.value);
const cheapestDieselInfo = computed(() => cheapestDiesel.value);
const cheapestULSDInfo = computed(() => cheapestULSD.value);

/**
 * @returns the gas stations with the cheapest prices for each gas type
 */
function getCheapestPrices() {
   fetch( import.meta.env.VITE_HEROKULINK + '/gasstations/top', {
    method: 'GET'
  })
  .then(result => result.json())
  .then(data => {
    cheapestPricesObject.value = data.data;

    //console.log(cheapest87.value.length);
    console.log(cheapestPricesObject.value);

    if (cheapestPricesObject.value !== undefined) {
      for (let i = 0; i < cheapestPricesObject.value.length; i++) {
        let gasType = cheapestPricesObject.value[i].gas_type.gas_type_name;
        let gasPrice = cheapestPricesObject.value[i].price;
        let gasStationInfo = cheapestPricesObject.value[i].gas_post.gas_station;

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

      console.log(response.value);
    })
    .catch(error => {
      console.log(error)
    })
  } else {
   fetch( import.meta.env.VITE_HEROKULINK + '/gasstations', {
      method: 'GET'
    })
    .then(result => result.json())
    .then(data => {
      searchBar.value = ' ';
      searchBar.value = '';
      response.value = data.data;
   })
    .catch(error => {
      console.log(error)
    })
  }
}

/**
 * sorts the list of gas stations by price 
 */
function sortByPrice() {
   if (searchBar.value !=='') {
    fetch( import.meta.env.VITE_HEROKULINK + '/gasstations/search', {
      body: JSON.stringify({
        'cheapest': searchBar.value
      }),
      method: 'POST'
    })
    .then(result => result.json())
    .then(data => {
      searchBar.value = ''; //not sure why this doesn't work without it being cleared
      response.value = data.data;

      console.log(response.value);
    })
    .catch(error => {
      console.log(error)
    })
  }
}

/** 
 * @param {integer} id 
 * Allows the user to get directions to the gas station with the best prices.
 */
function goToGasStation(id) {
  router.push('/route/' + id);
}
</script>

<style>
#results-area {
  margin-left: 80px;
  margin-right: 80px;
}

#fuelprices-area {
  display: block;
  padding-bottom: 20px;
  padding-top: 30px;
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
