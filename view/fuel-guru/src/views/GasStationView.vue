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
            
            <ul><!-- v-if="gasList.length>0" not sure why this doesnt work-->
                <div id="cardRow" >

                    <li id="price" v-for="bestprice in gasList" :key="gas.id"> 
                        <h4> test {{bestprice.gases}} </h4> <!---E-10 87 Fuel -->
                        <h4> {{gas.price}} </h4> <!--- E-10 87 Fuel -->
                    </li>  
                </div>    
            </ul>
        
            <button type="button" class="btn">Suggest a Price</button>

        </div>

        <!--- Amenities -->
        <div class="row">
            <h3>Amenties with the most upvotes</h3>
            <div id="cardRow" v-if="amenities.length>0">
                <li id="card" v-for="amenity in amenities" :key="amenity.id"> 
                    <h4 id="amenity-h"> {{amenity.amenity_type.amenity_name}} </h4>
              
                    <br>
                    <br>
                </li>
            
            </div>
            <div class="list-group-comments"  v-else>
                <p>There are no amenities posted at this time.</p> 
            </div>
            <br>
            <button type="button" class="btn">Suggest an Amenity</button>

        </div>

        <!--- Comments -->
        <div class="comments">
            <h3>Comments</h3>
            <div id="cardRow" >
                <ul v-if="comments.length>0">
                    <li id="card" v-for="comment in comments" :key="comment.id">
                        <h4 id="amenity-h">{{ comment.creator.username }}</h4> <h4 id="amenity-h">{{ comment.created_at }}</h4> 
                        <p id="amenity-h">{{ comment.body }}</p>
                        
                        <h4 id="amenity-h">Up Votes: {{ comment.upvote_count }} &emsp;&emsp;       Down Votes: {{ comment.downvote_count }}</h4>
                      
                        <!--check attributes for the comment from the user-->
                    </li>
                </ul>
                <div class="list-group-comments" v-else>
                             <p>There are no comments posted at this time.</p> 
                        </div>
            </div>
            <button type="button" @click="getGasStation" class="btn">Leave a comment</button>

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
        console.log("gas list is "+this.gasList);
        this.amenities = this.station.amenities;
        this.comments = this.station.comments;
        this.rating = this.station.avg_rating;
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


#cardRow {
  display: grid;  
  grid-template-columns: auto auto auto ;
  text-align: center;
  column-gap: 100px;
}

#amenity,#price,#card{
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