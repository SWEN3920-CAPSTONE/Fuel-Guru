<template>
    <main id="map-page">
        <div id="title">
            <h2>Google Maps Nearby Search</h2>
        </div>
        <div id="map-container">
          <div id="map-v">
            <span v-if="!locationgranted">{{notifmessage}}</span>
          </div>
        </div>
    </main>
</template>

<script>

export default {
    name: 'Map',
    data(){
      return{
        map: null,
        mapCenter: {lat: 18.024960, lng: -76.796557 }, //default location in Kingston
        nearbyGasstations: [],
        notifmessage: '',
        locationgranted: false
      }
    },

    methods: {
        initMap(){
          console.log('initMap')
          this.map = new google.maps.Map(document.getElementById('map-v'), {
            center: this.mapCenter,
            zoom: 13,
          })
        }, 

        setMarker(Points, Label){
          console.log('setMarker')
                const markers = new google.maps.Marker({
                    position:Points,
                    map: this.map,
                    label: {
                        text: Label,
                        color: '#000'
                    }
                })
          },

        findNearbyGasstations(mylat, mylng){
            console.log('findNearbyGasstations')
            var myPosition = new google.maps.LatLng(parseFloat(mylat), parseFloat(mylng))
            this.mapCenter = myPosition
            console.log(myPosition)    
            fetch('http://localhost:9000/gasstations/search/nearby', {
              body: JSON.stringify({
              'lat': mylat,
              'lng': mylng
              }),
            method: "POST"
            })
            .then(async (result) =>{
              if (result.status == 404){
                this.initMap()
                this.setMarker(myPosition, 'You')
                alert('You are not nearby (within 1500 meters of) any gas stations.')
              }
              else if(result.status == 200){
                result = await result.json()
                console.log(result)
                this.initMap()
                this.setMarker(myPosition, 'You')
                for (var i = 0; i < (result.data).length; i++){ 
                   this.setMarker((result.data)[i].geometry.location, (result.data)[i].name)
                };
              }
            }).catch(error => {
                console.log(error)
            })
        },

        errorPostion(error) {
          this.locationgranted = false
            switch(error.code){
                case error.PERMISSION_DENIED:
                   this.notifmessage ="User denied the request for Geolocation."
                break;
                case error.POSITION_UNAVAILABLE:
                   this.notifmessage ="Location information is unavailable."
                break;
                case error.TIMEOUT:
                   this.notifmessage ="The request to get user location timed out."
                break;
                case error.UNKNOWN_ERROR:
                   this.notifmessage ="An unknown error occurred."
                break;
            } 
        },
    },

    created(){
      
    },

    mounted(){
      const options= { enableHighAccuracy : true,timeout: 20000, maximumAge: 0 };

      if(navigator.geolocation){
        this.locationgranted = true
        navigator.geolocation.getCurrentPosition((position) => {
          this.locationgranted = true
          console.log(position)
          this.findNearbyGasstations(position.coords.latitude, position.coords.longitude)
         
        }, this.errorPostion, options)
      }else{
        this.locationgranted = false;
        this.notifmessage = 'This Broswer does not support Geolocation. Please use a different broswer'
      }
      console.log(this.notifmessage)
    }
}

</script>

<style>
#title {
  width: 100%;
  text-align: center;
  margin-bottom: 50px;
}

#map-v {
    height: 500px;
    width: 100%;
    text-align: center;
}

span{
    color: #AA1414;
}

</style>
