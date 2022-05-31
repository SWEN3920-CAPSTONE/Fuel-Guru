<!-- this is the page based on the information pulled from the database
This would hold the template for all gas stations 
the components are not yet created -->

<template>    
  <main id="gasStation-area">
    <div id="gasStation-info">
      <div>
        <img src="@/assets/other.jpg" alt="Gas Station Image" id="other2">
      </div>
      <div>
        <h1 id="gasStationName">Gas Station Name</h1>
        <h2>Gas Station Location</h2>
      </div>
    </div>
    <div>
      <div id="rating-area">
        <h3>Gas Station Rate</h3>
        <button id="rate-btn">Rate</button>
      </div>
    </div>

      <div id="pricesInfo">
        <h3>Fuel prices with the most upvotes for today.</h3>
        <div id="prices">
          <div>
            <h4>E-10 87 Fuel</h4>
            <p>PRICE</p>
          </div>
          <div>
            <h4>E-10 90 Fuel</h4>
            <p>PRICE</p>
          </div>
          <div>
            <h4>ULSD Fuel</h4>
            <p>PRICE</p>
          </div>
          <div>
            <h4>Diesel Fuel</h4>
            <p>PRICE</p>
          </div>
        </div>    
        <div>
          <div>
            <!--list of 5 votes-->
            <h3>Vote on existing fuel prices or suggest the correct a price.</h3>
          </div>
          <div>
            <button id="suggest-price">Suggest A Price</button>
          </div>
        </div>
      </div>
      
      <div id="amenityInfo">
        <h3>Amenities with the most upvotes.</h3>
        <div id="amenity">
          <div>
            <h4>Amenity</h4>
            <p>NAME</p>
          </div>
          <div>
            <h4>Amenity</h4>
            <p>NAME</p>
          </div>
        </div>
        <div id="upvoted-amenities">
          <h3>Vote on existing fuel amenities or suggest the correct amenities.</h3>
        </div>    
        <div>
          <button id="suggest-amenity">Suggest Amenity</button>
        </div>
      </div>  

      <div id="comments-area">
          <h3>COMMENTS</h3>          
          <div id="prevComments">
            <!--comments-->
          </div>
          <div id="makeComment">     
            <textarea id="comment-input" placeholder="Comment.." rows="4" cols="100" ></textarea>
            <button id="comment-btn" >Comment</button>
          </div>
      </div>
  </main>
</template>

<script setup>

</script>


<style>
#gasStation-area {
  display: block;
  padding-bottom: 20px;
}

#gasStationName {
  font-size: 40px;
}

#gasStation-info {
  display: grid;
  grid-template-columns: 30% 70%;
  padding-bottom: 30px;
}

#other2 {
  height: 200px;
}

#prices, #amenity {
  display: grid;  
  grid-template-columns: auto auto auto auto ;
  text-align: center;
  column-gap: 100px;
}

#prices div, #amenity div {
  border: 2px solid #AA1414;
  border-radius: 20px;
}

#suggest-price, #suggest-amenity, #rate-btn{
  border: 2px solid #AA1414;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 3%;
  padding-right: 3%;
  color: white;
  background-color: #AA1414;
  border-radius: 25px;
}

#prevComments {
  height: 500px;
  overflow-x: hidden; 
  overflow-y: auto;
}

#makeComment {
  display: block;
}

#rating-area, #pricesInfo, #amenityInfo{
  padding-bottom: 50px;
}

#comment-btn {
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