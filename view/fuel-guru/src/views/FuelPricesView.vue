<template>
<main id="fuelprices-area">
  <div id="cheapest-prices">
    <div id="cheapest-87">87
    </div>
    <div id="cheapest-90">90
    </div>
    <div id="cheapest-diesel">diesel
    </div>
    <div id="cheapest-ulsd">usld
    </div>
  </div>
  <div id="search-area">     
    <input type="text"  id="search-fp" placeholder="Search..">
    <button id="search-btn">Search</button>
    <div id="filter-area">    
    </div>  
  </div> 
  <div id="results-area">     
  </div>     
</main>  
</template>


<style>
main {
  padding-top: 50px; 
  color: black;
  font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; 
}

#fuelprices-area {
  display: block;
}

#cheapest-prices {
  display: grid;  
  grid-template-columns: auto auto auto auto ;
  text-align: center;
  column-gap: 100px;
}

#cheapest-prices div {
  border: 2px solid #AA1414;
  border-radius: 5px;
  padding: 5px;
}

#search-area {
  padding-top: 50px;
  text-align: center;
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
}
</style>
