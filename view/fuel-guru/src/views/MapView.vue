<template>
    <main id="map-page">
        <div id="title">
            <h2>Google Maps Nearby Search</h2>
        </div>
        <div id="map-container">
            <GoogleMap api-key="AIzaSyDRP8nSFiRqi-kKZMOBKYoghzawthJgUhs" style="width: 100%; height: 500px" :center="center" :zoom="15">
              <Marker v-for="marker in markers" :options="marker" :key="marker"/>
            </GoogleMap>
        </div>
    </main>
</template>

<script>
import { defineComponent } from "vue";
import { GoogleMap, Marker } from "vue3-google-map";

export default defineComponent({
  components: { GoogleMap, Marker },
  setup() {
    var markers = [];

    function errorPostion(error) {
            switch(error.code){
                case error.PERMISSION_DENIED:
                    x.innerHTML="User denied the request for Geolocation."
                break;
                case error.POSITION_UNAVAILABLE:
                    x.innerHTML="Location information is unavailable."
                break;
                case error.TIMEOUT:
                    x.innerHTML="The request to get user location timed out."
                break;
                case error.UNKNOWN_ERROR:
                    x.innerHTML="An unknown error occurred."
                break;
            } 
        }

        const options= { enableHighAccuracy : true,timeout: 20000, maximumAge: 0 };

    const center = { lat: 18.024960, lng: -76.796557 }; //map centred in Kingston by default
    if(navigator.geolocation){ //if location access granted
    console.log('location access granted')
      navigator.geolocation.getCurrentPosition((position) => {
        center.lat = position.coords.latitude
        center.lng = position.coords.longitude    

      fetch('http://localhost:9000/gasstations/search/nearby', {
      body: JSON.stringify({
        'lat': center.lat,
        'lng': center.lng 
      }),
      method: "POST"
    })
    .then(result => {result.json()
    if(result.status == 404){
      alert('No gas stations were found near you')
    }
    })
    .then(data => {
        for (var i = 0; i < (data.data).length; i++){
          markers.push({ position: (data.data)[i].geometry.location, label: (data.data)[i].name})
        };
        console.log(markers)
      })
      .catch(error => {
        console.log(error)
      })
      }, errorPostion, options);
    console.log(center)
    }
    console.log(markers)
    return { center, markers };
  },
});

</script>

<style>
#title {
  width: 100%;
  text-align: center;
}
</style>
