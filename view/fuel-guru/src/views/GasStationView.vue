<!-- this is the page based on the information pulled from the database
This would hold the template for all gas stations 
the components are not yet created -->

<template>    
    <main id="stationArea">
        <div class="stationGenInfo">
        <div class="row">
            <div class="col-md-12">
                <img src="@/assets/other.jpg" alt="Gas Station Image" id="other">
                
                <h2 id="cheapest-d-h">{{name}}</h2>
                <p>{{station.address}}</p>
                <button type="button" @click="goToMap" id="directions-btn" class="btn">Get Directions</button>

<!--stylesheet for stars-->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <br>
                <br>
                <br>
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
            
            <ul v-if="bestPrice!=null"><!-- v-if="gasList.length>0" not sure why this doesnt work-->
                <div id="cardRow" >

                    <li id="price" v-for="gas in bestPrice" :key="gas.id"> 
                        <h4> Type: {{gas.gas_type.gas_type_name}} </h4>
                         <h4> Price: ${{gas.price}} </h4> <!-- format number?-->
                         
                    </li> 
                     
                </div>    
            </ul>

            <div class="list-group-comments" v-else>
                  <p>There are no comments posted at this time.</p> 
            </div>
        
            <button v-show="this.hasToken" @click="show_vote_fuelprices=!show_vote_fuelprices" type="button" class="btn">View All Gas Price Suggestions</button>

            
        </div>
        <div id="suggestedPrices" v-show="show_vote_fuelprices">
          <h3>All Suggested Prices</h3>

          <div id="commentRow"  v-if="allsuggestedPrices.length>0">
                  
                <div  id="card" v-for="gasArray in allsuggestedPrices" :key="gasArray.id"> 
                        <h5 id="headline">Username: </h5><p id="headline">{{gasArray.creator.username}}</p>

                        <div  v-for="gas in gasArray.gases" :key="gas.id"> 
                            <h4> Type: {{gas.gas_type.gas_type_name}} </h4>  
                            <h4 id="headline"> Price: ${{gas.price}} </h4>
                            <hr>
                            <!-- Print ID for testing <p>id: {{gasArray.id}}</p> -->  
                        </div>
                <h5>Upvotes: {{gasArray.upvote_count}} &emsp;&emsp; DownVotes: {{gasArray.downvote_count}}  </h5>
                <i class="fa fa-thumbs-up" id="thumbs" @click="upvote(gasArray.id)"></i>&emsp; <!--functions to be added in-->
                <i class="fa fa-thumbs-down" id="thumbs" @click="downvote(gasArray.id)"></i>
                          
                </div>
                
            </div>
            <div v-else>
                  <p>There are no comments posted at this time.</p> 
            </div> 
            <br>
            <div id="sugg">
                <h5>Make a gas price suggestion!</h5>     
                Gas Type: <input type="text"  id="sugg-type" placeholder="Gas Type" v-model="sugg_type">
                &emsp;
                Gas Price: <input type="text"  id="sugg-price" placeholder="Gas Price" v-model="sugg_price">
                <br>
                <br>
                <button id="search-btn" @click="makeGasStationSuggestion(sugg_price,sugg_type)">Suggest Price</button>
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
            <div id="commentRow" v-if="comments.length>0">
                <ul>
                    <li id="comment" v-for="comment in comments" :key="comment.id">
                        <div id="comment-heading-grid">
                            <div id="comment-heading">
                                <h4>{{comment.creator.username}}</h4>
                            </div>
                            <div id="comment-created">
                                <h4>{{ comment.created_at }}</h4>
                            </div>
                            <div id="comment-rating">
                                <i class="fa fa-pencil-square" id="thumbs" @click="upvote(comment.id)"></i>   &nbsp;  
                                <i class="fa fa-trash" id="thumbs" @click="upvote(comment.id)"></i>
                            </div>
                        </div>
                         <!--<h4 id="amenity-h">{{ comment.creator.username }} &emsp; &emsp; Date: {{ comment.created_at }} 
                          &emsp;&emsp;&emsp;
                          
                          <i class="fa fa-thumbs-up" id="thumbs" @click="upvote(comment.id)"></i>{{ comment.upvote_count }}
                          &emsp;
                          <i class="fa fa-thumbs-down" id="thumbs" @click="downvote(comment.id)"></i>{{ comment.downvote_count }}
                          &emsp; 
                          <i class="fa fa-pencil-square" id="thumbs" @click="upvote(comment.id)"></i>
                          &emsp;
                          <i class="fa fa-trash" id="thumbs" @click="upvote(comment.id)"></i>
                        
                        </h4>  -->
                        
                        <p id="amenity-h">"{{ comment.body }}"</p>
                        <br>  
                        
                        <!--<h5 id="amenity-h">Up Votes:  &emsp;&emsp;       Down Votes: </h5>
                        check attributes for the comment from the user-->
                    </li>
                    
                    
                </ul>
              <div id="sugg">    
                  <input type="text"  id="commentEntry" placeholder="Leave a comment..." v-model="comment">
                  
                  
                  <button id="comment-btn" @click="makeNewComment(comment)">Add Comment</button>
                  <br>
                  <br>
                  <br>
              </div>            
            </div>
            <div class="list-group-comments" v-else>
              <p>There are no comments posted at this time.</p> 
            </div>
            
        </div>  
            <br>
            
        </div>
    </main>
</template>

<script>

import GasStationPageVue from '../components/GasStationPage.vue';


//access control issue '(Access-Control-Allow-Origin)

export default {
  
  
  data() {
    return {
        name: '',
        station: {},
        location: '',
        station_id: 1,
        amenities: {},
        bestPrice:{},
        allsuggestedPrices:{},
        comments: {},
        rating: 0,
        show_vote_fuelprices:false,
        sugg_price: '',
        sugg_type: '',
        post_id:22,
        hasToken: false,
        comment:"",
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
    checkToken(){
      if (localStorage.refreshToken!=null)
      {
        this.hasToken=true;
        console.log(this.hasToken);
      }
    },

    makeNewComment(commentBody){
        fetch('http://localhost:9000/posts', {
        body: JSON.stringify({
            "gas_station_id":parseInt(this.id),
            "post_type_id": 1,
            
            "comment":
            
            {
              "body":commentBody
            }
          }),
        headers: 
        {
          Authorization: 'Bearer ' + localStorage.refreshToken
        },
        method: "POST"
      })
      .then(result => result.json())
      .then(data => {
        this.post=data.data;
        console.log(this.id);
        
        alert(`You have successfully commented`);
        
        this.$router.go()
      })
      .catch(error => {
        console.log(error)
        alert(error);
      })
    },
    makeGasStationSuggestion(price,type_id)
    {
        fetch('http://localhost:9000/posts', {
        body: JSON.stringify({
            "gas_station_id":parseInt(this.id),
            "post_type_id": 5,
            "gas_price_suggestion":
            {
              
              "gases":[
                {
                  "gas_type_id":parseInt(type_id),
                  "price":parseInt(price)
                }
              ]
            }      
          }),
        headers: 
        {
          Authorization: 'Bearer ' + localStorage.refreshToken
        },
        method: "POST"
      })
      .then(result => result.json())
      .then(data => {

        if(data.error!=null)
        {
          alert(data.error);
        }
        else
        {
          alert(`You have successfully made a suggestion`);
          this.$router.go()
        }
        
      })
      .catch(error => {
        console.log(error)
        alert(error);
      })
    }
    ,
    upvote(post_id){
      fetch('http://localhost:9000/posts/upvote', {
        body: JSON.stringify({
            "post_id": post_id
          }),
        headers: 
        {
          Authorization: 'Bearer ' + localStorage.refreshToken
        },
        method: "POST"
      })
      .then(result => result.json())
      .then(data => {
        
        if(data.error!=null)
        {
          alert(data.error);
        }
        else
        {
          alert(`You have successfully toggled your upvote`);
          this.$router.go()
        }
        
        //console.log(localStorage.refreshToken);
      })
      .catch(error => {
        console.log("error is"+ error)
        
      })

    },
    downvote(post_id){
      fetch('http://localhost:9000/posts/downvote', {
        body: JSON.stringify({
            "post_id": post_id
          }),
        headers: 
        {
          Authorization: 'Bearer ' + localStorage.refreshToken
        },
        method: "POST"
      })
      .then(result => result.json())
      .then(data => {
        //this.post=data.data;
        if(data.error!=null)
        {
          alert(data.error);
        }
        else
        {
          alert(`You have successfully toggled your downvote`);
          this.$router.go()
        }
      
        console.log(localStorage.refreshToken);
      })
      .catch(error => {
        console.log(error)
      })

    },
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

        try{
          this.bestPrice = this.station.current_best_price.gases;
          
        }
        catch(e){
            this.bestPrice = null;

        }

        try{
            this.allsuggestedPrices = this.station.gas_price_suggestions;
            console.log(this.allsuggestedPrices);
        }
        catch(e)
        {
            alert("No suggestions");
            //this.allsuggestedPrices = null;
        }
        
        console.log("gas list is "+this.bestPrice);
        //console.log("allsuggestedPrices "+this.allsuggestedPrices);
        this.amenities = this.station.amenities;
        this.comments = this.station.comments;
        this.rating = 5//this.station.avg_rating;
        console.log(data.data);
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
    console.log("gas prices" + this.allsuggestedPrices);
    this.checkToken();
    
    
  }
}
//SELECT gas_price_suggestions.id, gas_price_suggestions.last_edited, gas_price_suggestions.post_id, posts.id,posts.created_at,posts.last_edited,posts.gas_station_id,posts.post_type_id,posts.creator_id FROM gas_price_suggestions INNER JOIN posts on gas_price_suggestions.post_id = posts.id;

</script>

<style>

.checked {
  color: #AA1414;
}


#stationarea {
  padding-top: 50px; 
  color: black;
  font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; 
}




#cardRow {
  display: grid;  
  grid-template-columns: auto auto auto auto ;
  text-align: center;
  column-gap: 15px;

}

#headline{
    display: inline;
    vertical-align: top;
    line-height: 28px;    
}
#headline h5{
  font-weight: bold;

}

#cardRow3 {
  display: grid;  
  grid-template-columns: auto auto auto auto;
  text-align: center;
  column-gap: 5px;
  gap: 10px;
}

#amenity,#price,#card{
  border: 2px solid #AA1414;
  border-radius: 25px;
  
  padding:15px;
  
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

#filter-area {
  padding-top: 30px;
  text-align: center;
  padding-bottom: 20px;
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

#commentRow{
  display: grid;  
  grid-template-columns: 80% ;
  text-align: center;
}

#comment-heading-grid{
  display: grid;  
  grid-template-columns: auto auto auto ;
  margin: 0px;
  height: 40%;
  padding:0px;
}

#comment{
  border: 2px solid #AA1414;
  border-radius: 25px;
  width: 100%;
  padding:0px;
  height: 90px;
  margin-bottom: 10px;
  display: inline-block;
  text-align: middle;
}

#commentEntry{
  width: 75%;
  padding:0px;
  height: 90px;
  margin-bottom: 10px;
  margin-left: 3%;
  text-align: left;
  float: left;
}

#sugg {
  text-align: left;
  padding:10px;
}
  
#sugg-type,#sugg-price {
  width: 100px;
}

#thumbs{
  font-size:25px;
  color:#AA1414;
  text-align: right;
  margin-top: 15px;
}
#thumbs:hover{
  cursor: pointer;
  color: #8a1010;

}

#comment-btn {
  border: 2px solid #AA1414;
  width: 160px;
  margin-top: 0px;
  margin-left: 15px;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 3%;
  padding-right: 3%;
  color: white;
  background-color: #AA1414;
  border-radius: 5px;
}

#directions-btn{
  display: inline;

}
.btn{
    border: 2px solid #AA1414;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 3%;
    padding-right: 3%;
    color: #AA1414;
    background-color: white;
    border-radius: 25px;
}

.btn:hover{
  background-color: #AA1414;
  color:white;
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

</style>