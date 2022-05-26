<template>
<main id="fuelprices-area">
  <div id="cheapest-prices">
    <div id="cheapest-87">
      <div id="cheapest-87-h">
        <h2>Lowest <br> E-10 87 Fuel</h2>
      </div>      
      <div>
        <p>GAS STATION NAME <br> GAS STATION LOCATION <br> GAS PRICE</p>
        <button id="location-87">View Location</button>
      </div>
    </div>
    <div id="cheapest-90">
      <div id="cheapest-90-h">
        <h2>Lowest <br> E-10 90 Fuel</h2>
      </div>      
      <div>
        <p>GAS STATION NAME <br> GAS STATION LOCATION <br> GAS PRICE</p>
        <button id="location-90">View Location</button>
      </div>
    </div>
    <div id="cheapest-d">
      <div id="cheapest-d-h">
        <h2>Lowest <br>Diesel Fuel</h2>
      </div>      
      <div>
        <p>GAS STATION NAME <br> GAS STATION LOCATION <br> GAS PRICE</p>        
        <button id="location-d">View Location</button>
      </div>
    </div>
    <div id="cheapest-sd">
      <div id="cheapest-sd-h">
        <h2>Lowest <br> ULSD Fuel</h2>
      </div>      
      <div>
        <p>GAS STATION NAME <br> GAS STATION LOCATION <br> GAS PRICE</p>
        <button id="location-sd">View Location</button>
      </div>
    </div>
  </div>
  <div id="search-area">     
    <input type="text"  id="search-fp" placeholder="Search..">
    <button id="search-btn">Search</button>
  </div>
  <div id="filter-area">    
    <label for="parish">PARISH: </label>
    <select id="parish">
      <option>Please select one</option>
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
    <label for="company">COMPANY: </label>
    <select id="company">
      <option>Please select one</option>
      <option>Blaze</option>
      <option>Cool Oasis</option>
      <option>Fesco</option>
      <option>Independent</option>
      <option>Rubis</option>
      <option>Texaco</option>
      <option>Total</option>
      <option>Unipet</option>
    </select>
    <label for="sortby">SORT BY: </label>
    <select id="sortby"> 
      <option>Please select one</option>
      <option>Price</option>
      <option>Name</option>
    </select>
  </div>  
  <div id="results-area">     
    <!--v-for to display results-->
    <p>S</p>
  </div>     
</main>  
</template>

<!--
<script>
///"/gasstations/search"

//access control issue '(Access-Control-Allow-Origin)
/*
export default {
  methods: {
    getGasStations() {
      fetch('http://localhost:9000/gasstations/search', {
        body: JSON.stringify({
          "name": "Total"
        }),
        method: "POST"
      })
      .then(result => result.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
created() {
  this.getGasStations()
}
}*/
</script>
-->
<style>
main {
  padding-top: 50px; 
  color: black;
  font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; 
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

#location-87, #location-90, #location-d, #location-sd {
  border: 2px solid #AA1414;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 3%;
  padding-right: 3%;
  color: white;
  background-color: #AA1414;
  border-radius: 25px;
}

label {
  padding-right: 5px;
  padding-left: 30px;
}
</style>
