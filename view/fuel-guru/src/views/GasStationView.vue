<!-- this is the page based on the information pulled from the database
This would hold the template for all gas stations 
the components are not yet created -->

<template>    
    <main id="stationArea">
        <div class="stationGenInfo">
        <div class="row">
            <div class="col-md-12">
                <img src="@/assets/other.jpg" alt="Gas Station Image" id="other">
                <br>
                <h2 id="cheapest-d-h">{{name}}</h2>
                <p>{{station.address}}</p>
            </div>
            <div class="row">
                <br>
                <h3>Rating {{rating}}/5 </h3>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </div> <!--Create number of stars based on rating 
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>-->
        </div>


        <!--- fuel prices -->
        <div class="row">
            <h3>Fuel prices with the most upvotes for today</h3>
            
            <ul id="cheapest-prices">
                <div id="price">

                    <li id="price-h" v-for="gas in gasList" :key="gas.id"> 
                        <h4> {{gas.name}} </h4> <!---E-10 87 Fuel -->
                        <h4> {{gas.price}} </h4> <!--- E-10 87 Fuel -->
                    </li>  
                </div>    
            </ul>
        
            <button type="button" class="btn">Suggest a Price</button>

        </div>

        <!--- Amenities -->
        <div class="amenities-voted">
            <h3>Amenties with the most upvotes</h3>
            <div id="amenity">
                <li id="amenity-h" v-for="amenity in amenities" :key="amenity.id"> 
                    <h4> {{station.amenity.name}} </h4>
                </li>
            </div>
            <br>
            <button type="button" class="btn">Suggest an Amenity</button>

        </div>

        <!--- Comments -->
        <div class="comments">
            <h3>Comments</h3>
            <div class="col-md-12">
                <ul class="list-group-comments">
                    <li class="list-group-comment" v-for="comment in comments" :key="comment.id">
                        <div class="row">
                            
                            <div id="comment">
                                <h4>{{ comment.name }}</h4> <!--check attributes for the comment from the user-->
                            </div>
                            
                        </div>
                    </li>
                </ul>
            </div>
            <button type="button" @click="getGasStation" class="btn">Leave a comment</button>

        </div>  
            <button type="button" @click="goToMap" class="btn">Get Directions</button>
        </div>
    </main>
</template>

<script>

//access control issue '(Access-Control-Allow-Origin)

export default {
  
  
  data() {
    return {
        name: '',
        station: {},
        location: '',
        station_id: 1,
        amenities: {},
        gasList:{},
        comments: {},
        rating: 0,
    }
  },
  methods: {

    //GetComments for a specific gas station
    //get the amenities for a specific gas station
    //get the fuel prices for a specific gas station


        // need to find a way to have the id of the gas station entered
       /* body: JSON.stringify({
          "station_id": this.station_id
        }),*/
    getGasStation() {
      console.log("station id is " + this.id)
      fetch('http://localhost:9000/gasstations/'+this.id, {
       
        method: "GET"
      })
      .then(result => result.json())
      .then(data => {
        this.station=data.data;
        this.name = this.station.name;
        this.location = this.station.location;
        this.gasList = this.station.gas_price_suggestion;
        this.amenities = this.station.amenities;
        this.comments = this.station.comments;
        this.rating = this.station.avg_rating;
        console.log(this.station);
      })
      .catch(error => {
        console.log(error)
      })
    },

    goToMap() {
      this.$router.push('/route/' + this.id)
    }
  },
  created() {
    this.id = this.$route.params.id
    this.getGasStation()
  }
}

</script>

<style>

.checked {
  color: #AA1414;
}

.btn{
    border: 2px solid #AA1414;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 3%;
    padding-right: 3%;
    color: white;
    background-color: #AA1414;
    border-radius: 25px;
}

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

#amenities-voted,#cheapest-prices {
  display: grid;  
  grid-template-columns: auto auto auto auto ;
  text-align: center;
  column-gap: 100px;
}

#amenity,#price{
  border: 2px solid #AA1414;
  border-radius: 25px;
  padding-bottom: 15px;
}

#amenity-h,#price-h {
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

#other{
  height: 150px;
  float: left;
}

</style>