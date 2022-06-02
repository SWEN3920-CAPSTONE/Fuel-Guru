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

<!--stylesheet for stars-->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

                <h3> Rating 
                  <!--Create number of stars based on rating -->
                  <span v-if="rating==0">
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                  </span>

                  <span v-if="rating==1">
                    <span class="fa fa-star checked"></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                  </span>

                  <span v-if="rating==2">
                    <span class="fa fa-star checked"></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                  </span>

                  <span v-if="rating==3">
                    <span class="fa fa-star checked"></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star" ></span>
                    <span class="fa fa-star" ></span>
                  </span>

                  <span v-if="rating==4">
                    <span class="fa fa-star checked"></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star" ></span>
                  </span>

                  <span v-if="rating==5">
                    <span class="fa fa-star checked"></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star checked" ></span>
                    <span class="fa fa-star checked" ></span>
                  </span>


             ({{rating}}) <!--Display rating in brackets-->
            
            </h3>
            </div>
        
        
                 
            

            
        </div>
        <!--- fuel prices -->
        <div class="row">
            <h3>HIGHEST UPVOTED FUEL PRICES</h3>
            
            <ul><!-- v-if="gasList.length>0" not sure why this doesnt work-->
                <div id="cardRow" >

                    <li id="price" v-for="gas in gasList" :key="gas.id"> 
                        <h4> Type: {{gas.gas_type.gas_type_name}} </h4> <!---E-10 87 Fuel -->
                        <h4> Price: ${{gas.price}} </h4> <!--- format number?-->
                    </li>  
                </div>    
            </ul>
        
            <button @click="show_vote_fuelprices=!show_vote_fuelprices" type="button" class="btn">Suggest a Price</button>

            <div v-show="show_vote_fuelprices" >
              
              <li id="price" v-for="gas in allsuggestedPrices" :key="gas.id"> 
                        <h4> Type: {{gas.gas_type.gas_type_name}} </h4> <!---E-10 87 Fuel -->
                        <h4> Price: ${{gas.price}} </h4> <!--- format number?-->
              </li>  
          </div>
        </div>
        <br>

        <!--- Amenities -->
        <div class="row">
            <h3>HIGHEST UPVOTED AMENITIES</h3>
            <div id="cardRow" v-if="amenities.length>0">
                <li id="card" v-for="amenity in amenities" :key="amenity.id"> 
                    <h4 id="title-card"> {{amenity.amenity_type.amenity_name}} </h4>
                
                </li>
            
            </div>
            <div class="list-group-comments"  v-else>
                <p>There are no amenities posted at this time.</p> 
            </div>
            <br>
            
        <button type="button" class="btn">Suggest an Amenity</button>
        </div>
        <br>

        <!--- Comments -->
        <div class="comments">
            <h3>Comments</h3>
            <div id="commentRow" >
                <ul v-if="comments.length>0">
                    <li id="card" v-for="comment in comments" :key="comment.id">
                        <h4 id="amenity-h">{{ comment.creator.username }} &emsp; &emsp; &emsp; Date: {{ comment.created_at }}</h4> 
                        
                        <p id="amenity-h">"{{ comment.body }}"</p>
                        
                        <h5 id="amenity-h">Up Votes: {{ comment.upvote_count }} &emsp;&emsp;       Down Votes: {{ comment.downvote_count }}</h5>
                      
                        <!--check attributes for the comment from the user-->
                    </li>
                    <br>
                    
                </ul>
                <div class="list-group-comments" v-else>
                             <p>There are no comments posted at this time.</p> 
                        </div>
            <button type="button" @click="getGasStation" class="btn">Leave a comment</button>

            </div>

        </div>  

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
        show_vote_fuelprices:false
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
        this.gasList = this.station.current_best_price;
        this.allsuggestedPrices = this.station.gas_price_suggestions;
        console.log("gas list is "+this.gasList);
        this.amenities = this.station.amenities;
        this.comments = this.station.comments;
        this.rating = 5//this.station.avg_rating;
        console.log(data.data);
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
  created() {
    this.id = this.$route.params.id
    this.getGasStation()
  }
}
//SELECT gas_price_suggestions.id, gas_price_suggestions.last_edited, gas_price_suggestions.post_id FROM gas_price_suggestions INNER JOIN posts on gas_price_suggestions.post_id = post.id;

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

#stationarea {
  padding-top: 50px; 
  color: black;
  font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; 
}

#commentRow{
  display: grid;  
  grid-template-columns: 650px ;
  text-align: center;
  column-gap: 100px;
}


#cardRow {
  display: grid;  
  grid-template-columns: 20% 20% 20% 20% ;
  text-align: center;
  column-gap: 50px;
}

#amenity,#price,#card{
  border: 2px solid #AA1414;
  border-radius: 25px;
  padding-bottom: 5px;
  
  display: inline-block;
  vertical-align: middle;
}

#amenity-h,#price-h {
  padding-left: 20px;
  padding-right: 20px;
  text-align: left;
}

#amenity-p,#price-p,#title-card {
  padding-left: 20px;
  padding-right: 20px;
  text-align: center;
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