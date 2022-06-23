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
                 <span v-if="rating>=0 && rating<1">
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="rating>=1  && rating<2">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="rating>=2  && rating<3">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="rating>=3 && rating<4">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="rating>=4  && rating<5">
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
                        <h4> Price: ${{parseFloat(gas.price).toFixed(2)}}</h4> <!-- format number?-->    
                   </li>         
               </div>   
           </ul>
 
           <div class="list-group-comments" v-else>
                 <p>There are no highest upvoted gas price suggestions posted at this time.</p>
           </div>
      
           <button v-show="this.hasToken" @click="show_vote_fuelprices=!show_vote_fuelprices" type="button" class="btn">View All Gas Price Suggestions</button>
 
       </div>
       <div id="suggestedPrices" v-show="show_vote_fuelprices">
         <h3>All Suggested Prices</h3>
 
         <div  v-if="allsuggestedPrices.length>0">
                
               <div  v-for="gasArray in allsuggestedPrices" :key="gasArray.id">
                      
 
                       <div id="fuelRow" v-for="gas in gasArray.gases" :key="gas.id">
                          <h5 id="headline">{{gasArray.creator.username}} </h5>
                           <h5 id="headline">{{gas.gas_type.gas_type_name}}</h5>
                           <h5 id="headline"> ${{parseFloat(gas.price).toFixed(2)}} </h5>
                           <i class="fa fa-thumbs-up" id="thumbs" @click="upvote(gasArray.id)">: {{gasArray.upvote_count}} &emsp;&emsp; </i>
                              
                           <i class="fa fa-thumbs-down" id="thumbs" @click="downvote(gasArray.id)">: {{gasArray.downvote_count}}  </i>
                          <hr>
       
                       </div>
               
               &emsp; <!--functions to be added in-->
               
                        
               </div>
               <br>
               <p>NOTE: You can suggest the correct gas price if it does not exist. If the price was submitted by another user, simply upvote the price by selecting the thumbs up icon.</p>
              
         </div>
         <div v-else>
           <p>There are no gas price suggestions posted at this time.</p>
         </div>
           <br>
         <div id="sugg" >
           <h5>Make a gas price suggestion!</h5>
 
           <!-- Selection of Gas Types -->
           
                  
                   <select id="sugg-type" v-model="sugg_type">
                     <option value="" disabled selected hidden>Select a Gas Type</option>
                     <option v-for="gas in gasTypes" :key="gas.id" :value="gas.id" placeholder="Select the Gas Type">{{gas.gas_type_name}}</option>
                   </select>
                   <br>
                   
                   <input type="text"  id="sugg-price" placeholder="Enter suggested gas price" v-model="sugg_price">
                 
 
                    <br>
                   <button id="search-btn" @click="makeGasStationSuggestion(sugg_price,sugg_type)">Suggest Price</button>
                
 
           
         </div>
       </div>
        
       <br>
 
       <!--- Amenities -->
       <div class="row">
           <h3>AMENITIES</h3>
           <div id="cardRow" v-if="amenities.length>0">
               <li id="card" v-for="amenity in amenities" :key="amenity.id">
                   <h4 id="title-card"> {{amenity.amenity_type.amenity_name}} </h4>
                   <h5>Upvotes: {{amenity.upvote_count}} &emsp;&emsp; DownVotes: {{amenity.downvote_count}}  </h5>
                   <i class="fa fa-thumbs-up" id="thumbs" @click="upvote(amenity.id)"></i>&emsp; <!--functions to be added in-->
                   <i class="fa fa-thumbs-down" id="thumbs" @click="downvote(amenity.id)"></i>
               </li>
          
           </div>
           <div class="list-group-comments"  v-else>
               <p>There are no amenities posted at this time.</p>
           </div>
           <br>
          
          <!-- When clicked, this button shows the area to suggest an amenity. This button only shows if the user
          is logged in. -->
           <button type="button" class="btn" v-show="this.hasToken" @click="show_suggest_amenity=!show_suggest_amenity">Suggest an Amenity</button>
 
           <div id="suggestedPrices" v-show="show_suggest_amenity">
              
  
              <div id="commentRow">
                    <h4 >Suggest an Amenity</h4>
                      
                        <select id="sugg-type" v-model="amenity_type">
                          <option value="" disabled selected hidden>Select an Amenity Type</option>
                          <option v-for="amenity in amenityTypes" :key="amenity.id" :value="amenity.id" placeholder="Select the Amenity Type">{{amenity.amenity_name}}</option>
                        </select>
                        <br>
                      
                        <button id="search-btn" @click="makeAmenitySuggestion(amenity_type)">Suggest Amenity</button>
                      
              </div>
           </div>
       </div>
       <br>
 
       <!--- Comments -->
       <div class="comments">
           <h3>Reviews</h3>
           <div id="commentRow" v-if="comments.length>0">
               <ul>
                   <li id="comment" v-for="comment in comments" :key="comment.id">
                       <div id="review-heading-grid">
                           <div id="comment-heading">
                               <h4>{{comment.creator.username}}</h4>
                           </div>
                           <div id="comment-created" >
                                
                               <h4>{{ comment.created_at }}</h4>
                           </div>

                       
                        <div id="comment-icons">

                         <span v-if="comment.rating_val>=0 && rating<1">
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="comment.rating_val>=1  && comment.rating_val<2">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="comment.rating_val>=2  && comment.rating_val<3">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="comment.rating_val>=3 && comment.rating_val<4">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="comment.rating_val>=4  && comment.rating_val<5">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star" ></span>
                 </span>
 
                 <span v-if="comment.rating_val==5">
                   <span class="fa fa-star checked"></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   <span class="fa fa-star checked" ></span>
                   
                 </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                           
                               <i class="fa fa-pencil-square" id="thumbs" @click="editComment(comment.id,comment.body,comment.rating_val)"></i>   &nbsp; 
                               <i class="fa fa-trash" id="thumbs" @click="deleteComment(comment.id)"></i>
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
           </div>
           <div class="list-group-comments" v-else>
             <p>There are no reviews posted at this time.</p>
           </div>

       </div> 
       <br>
       <div id="sugg" v-show="this.hasToken">  
         <hr>
                <h4>Leave a review!</h4> 

                <!--- Selection of Rating -->
                <div id="twocol">
                <h5>Rating&emsp; </h5>
                <select id="ratingbox" v-model="sugg_rating">
                   <option value="" selected disabled hidden>Rate the Gas Station</option>
                    <option value="1" >1</option>
                    <option value="2" >2</option>
                    <option value="3" >3</option>
                    <option value="4" >4</option>
                    <option value="5" >5</option>
                </select>
                </div>
                <br>
                 <input type="text"  id="commentEntry" placeholder="Leave a comment..." v-model="body">

                
                
                 <button id="comment-btn" @click="makeNewReview(body,sugg_rating)">Add Review</button>
                 
                 <br>
                 <br>
             </div>  
           <br>
          
       </div>
   </main>
</template>
 
<script>
//access control issue '(Access-Control-Allow-Origin)
import moment from 'moment';
import {sanitise_inputs, isEmpty} from '../assets/scripts/validate.js';

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
       sugg_rating: 0,
       show_vote_fuelprices:false,
       show_suggest_amenity:false,
       sugg_price: '',
       sugg_type: '',
       post_id:22,
       hasToken: false,
       body:"",
       gasTypes: [],
       amenityTypes: [],
       sugg_amenity: '',
       amenity_type: '',
       date: '',
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
  
  
   //Get Amenities for a specific gas station
   makeNewAmenity()
   {
     fetch(import.meta.env.VITE_HEROKULINK + '/posts', {
       body: JSON.stringify({
           "gas_station_id":parseInt(this.id),
           
         }),
       headers:
       {
         Authorization: 'Bearer ' + localStorage.refreshToken
       },
       method: "POST"
     })
     .then(result => result.json())
     .then(data => {
       this.amenities=data.data;
       console.log(this.amenities);
       this.getGasStation();
     })
     .catch(error => {
       console.log(error)
     })
   },
 
   makeNewReview(body,sugg_rating){

      
      if(body=="" || sugg_rating==""){
        alert("Please fill in all fields");
      }
      else{
          body = sanitise_inputs(body);
        fetch(import.meta.env.VITE_HEROKULINK + '/posts', {
        body: JSON.stringify({
            "gas_station_id":parseInt(this.id),
            "post_type_id": 1,
            
            "review":
            
            {
              "body":body,
              "rating_val":parseInt(sugg_rating)
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

        if(data.error!=null)
        {
          alert(data.error);
        }
        else
        {
            alert(`You have successfully made a review`);
            this.getGasStation();
        }
      
      })
      .catch(error => {
        console.log(error)
        alert(error);
      })
      }
      
   },
 
   editComment(commentId, currComment,currRating){
       let newComment = prompt("Please enter your edited comment", currComment);
      let newRating = prompt("Please enter your edited comment", currRating);
        if(newComment=="" || newRating==""){
          alert("Please fill in all fields");
        }
        newComment = sanitise_inputs(newComment);
        newRating = sanitise_inputs(newRating);

       fetch(import.meta.env.VITE_HEROKULINK + '/posts', {
       body: JSON.stringify({
           "post_id": parseInt(commentId),
           "review":
          
           {
             "body":newComment,
             "rating_val":parseInt(newRating)
           }
         }),
       headers:
       {
         Authorization: 'Bearer ' + localStorage.refreshToken
       },
       method: "PUT"
     })
     .then(result => result.json())
     .then(data => {
       this.post=data.data;
 
       if(data.error!=null)
       {
         alert(data.error);
       }
       else
       {
          alert(`You have successfully edited your review`);
          this.getGasStation();
       }
    
     })
     .catch(error => {
       console.log(error)
       alert(error);
     })
   },
 
   deleteComment(commentId){
      
       fetch(import.meta.env.VITE_HEROKULINK + '/posts', {
       body: JSON.stringify({
           "post_id": parseInt(commentId),
         }),
       headers:
       {
         Authorization: 'Bearer ' + localStorage.refreshToken
       },
       method: "DELETE"
     })
     .then(result => result.json())
     .then(data => {
       this.post=data.data;
 
       if(data.error!=null)
       {
         alert(data.error);
       }
       else
       {
          alert(`You have successfully deleted your review`);
          this.getGasStation();
       }
    
     })
     .catch(error => {
       console.log(error)
       alert(error);
     })
   },
 
   makeGasStationSuggestion(price,type_id)
   {
      if(price=="" || type_id==""){
        alert("Please fill in all fields");
      }
      else{
            price = sanitise_inputs(price);
          fetch(import.meta.env.VITE_HEROKULINK + '/posts', {
          body: JSON.stringify({
              "gas_station_id":parseInt(this.id),
              "post_type_id": 3,
              "gas_price_suggestion":
              {
                
                "gases":[
                  {
                    "gas_type_id": parseInt(type_id),
                    "price":parseFloat(price).toFixed(2)
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
            this.getGasStation();
          }
          
        })
        .catch(error => {
          console.log(error)
          alert(error);
        })
      }
      
   },

  makeAmenitySuggestion(type_id)
  {
      if(type_id==""){
      alert("Please fill in all fields");
    }
    else{
      fetch(import.meta.env.VITE_HEROKULINK + '/posts', {
       body: JSON.stringify({
           "gas_station_id":parseInt(this.id),
           "post_type_id": 4,
           "amenity_tag":
           {
              "amenity_id":parseInt(type_id),   
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
         //alert(`You have successfully made a suggestion`);
         this.getGasStation();
         //this.$router.go()
       }
      
     })
     .catch(error => {
       console.log(error)
       alert(error);
     })
    }
  }, 

   //Upvote a post
   upvote(post_id){
     fetch(import.meta.env.VITE_HEROKULINK + '/posts/upvote', {
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
      console.log(data);
       if(data.error!=null)
       {
         alert(data.error);
       }
       else
       {
         alert(`You have successfully toggled your upvote`);
         this.getGasStation(); //Update values
         //this.$router.go()
       }
      
       //console.log(localStorage.refreshToken);
     })
     .catch(error => {
       console.log("error is"+ error)
      
     })
 
   },
   downvote(post_id){
     fetch(import.meta.env.VITE_HEROKULINK + '/posts/downvote', {
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
         this.getGasStation();
       }
    
       console.log(localStorage.refreshToken);
     })
     .catch(error => {
       console.log(error)
     })
 
   },


   convertDate(reviews){
    for (var i = 0; i < reviews.length; i++) 
    {
      reviews[i].created_at = moment(reviews[i].created_at).utcOffset(-5).format('MMMM Do YYYY, h:mm a');
    }
    return reviews;
  },
  
   //Get all posts for a specific gas station
   getGasStation() {
     console.log("station id is " + this.id)
     fetch(import.meta.env.VITE_HEROKULINK + '/gasstations/'+this.id, {
     
       method: "GET"
     })
     .then(result => result.json())
     .then(data => {
       this.station=data.data;
       this.name = this.station.name;
       this.location = this.station.location;
 
       try{
         this.bestPrice = this.station.current_best_price; //Check this line
        
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
      
      
       this.amenities = this.station.amenities;
       console.log("Amenities");
       console.log(this.amenities);
       this.comments = this.convertDate(this.station.reviews);
       
       this.rating = this.station.avg_rating.toFixed(1);
       console.log(data.data);
     })
     .catch(error => {
       console.log(error)
     })
   },
 
   goToMap() {
     this.$router.push('/route/' + this.id)
   },
 
   getGasTypes(){
     fetch(import.meta.env.VITE_HEROKULINK + '/posts/gas/types', {
       method: "GET",
       headers:
       {
         Authorization: 'Bearer ' + localStorage.refreshToken
       }
     })
     .then(result => result.json())
     .then(data => {
       this.gasTypes = data.data;
       console.log("gas types are: " + data.data);
     })
     .catch(error => {
       console.log(error)
     })
   },

   getAmenityTypes(){
     fetch(import.meta.env.VITE_HEROKULINK + '/posts/amenities/types', {
       method: "GET",
       headers:
       {
         Authorization: 'Bearer ' + localStorage.refreshToken
       }
     })
     .then(result => result.json())
     .then(data => {
       this.amenityTypes = data.data;
       console.log("amenity types are: " + data.data);
     })
     .catch(error => {
       console.log(error)
     })
   },
 },
 
  created() {
   this.id = this.$route.params.id
   this.getGasStation()
   this.checkToken();
   this.getGasTypes();
    this.getAmenityTypes();
  }
}
//SELECT gas_price_suggestions.id, gas_price_suggestions.last_edited, gas_price_suggestions.post_id, posts.id,posts.created_at,posts.last_edited,posts.gas_station_id,posts.post_type_id,posts.creator_id FROM gas_price_suggestions INNER JOIN posts on gas_price_suggestions.post_id = posts.id;
 
</script>
 
<style>
 
.fa-star {
   color: black;
}

.checked {
 color: #AA1414;
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

#thumbs{
 font-size:1em;
 color:#AA1414;
 text-align: right;
 margin-top: 15px;
}
#thumbs:hover{
 cursor: pointer;
 color: #8a1010;
 
}


#fuelRow{
 display: grid; 
 margin-left: 30px;
 width: 70%;
 height: 20px;
 grid-template-columns: 15% 10% 10% 15% 15%;
 text-align: center;
}


#fuelRow p{
  margin-left: 30px;
}
#fuelRow i{
  font-size: 1.5em;
  height: 20px;
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
 grid-template-columns: 20% 60% 20% ;
 text-align: left;
 margin-left: 20px;
 height: 40%;
 padding:0px;
}

#review-heading-grid{
 display: grid; 
 grid-template-columns: 20% 30% 20% 20%;
 text-align: left;
 margin-left: 20px;
 height: 40%;
 padding:0px;
}
 
#comment-icons{
 float: right;
 text-align: left;
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

#ratingbox{
  display: inline-block;
  margin-top: 18px;
  vertical-align: middle;
  height: 28px;
}
#twocol{

  display: grid; 
  grid-template-columns: 20% auto ;
  text-align: right;
  column-gap: 5px;
  margin-left: 20px;
}

div #sugg{
  display: grid;
  grid-template-columns: 50%;
  width:90%;
  vertical-align: middle;
  margin-left: 20px;
}
#sugg {
 text-align: left;
 padding:10px;
 }

 div #sugg button{
    width:20%;
    
  }

  #commentRow div button{
    vertical-align: center;
  }

   #sugg-type{
  width: 310px;
  float:left;
}
  #commentRow #search-btn{
    width: 310px;
  }
  #commentRow h4{
    text-align: left;
  }

 @media only screen and (max-width: 890px) {
  #fuelRow{
    display: grid;
    width: 70%; 
    grid-template-columns: 20% 10% 10% 15% 15% ;
    height: 40px;
    text-align: center;
    column-gap: 25px;
  }

  div #sugg{
    display: grid;
    border-top: 20px black;
    grid-template-columns: 80%;
    width:90%;
    vertical-align: middle;
    text-align: center;
    margin-left: 50px;
  }

  div #sugg select, div #sugg input{
    width:100%;
    vertical-align: middle;
    text-align: center;
  }
  div #sugg button{
    width:100%;
    
  }
  #commentRow #search-btn{
    width: 100%;
  }

  div #sugg input{
    width:96%;
    vertical-align: middle;
    text-align: center;
  }

  #commentRow h4{
    text-align: center;
  }

  #commentRow{
    text-align: center;
    margin-left: 50px;
  }

  #sugg-type{
    width: 100%;
    float:left;
  }

  #twocol input{
    width:100%;
    margin-left: 10px;
  }
  #sugg input{
    width:100px;
    margin-left: 20px;
  }
  
  #cardRow {
  display: grid; 
  grid-template-columns: 30% 30% 30% ;
  
  text-align: center;
  vertical-align: center;
  column-gap: 15px;
  
  }
  
}

 
#sugg-price {
 width: 300px;
 float:left;
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
#price-btn {
 border: 2px solid #AA1414;
 padding-top: 5px;
 padding-bottom: 5px;
 padding-left: 3%;
 padding-right: 3%;
 float: right;
 color: white;
 background-color: #AA1414;
 border-radius: 5px;
}
 
</style>

