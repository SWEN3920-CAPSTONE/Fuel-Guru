<template>
    <main id="map-page">
        <div id="title">
            <h2>Google Maps Nearby Search</h2>
        </div>
        <div id="map-container">
            <GoogleMap api-key="AIzaSyDRP8nSFiRqi-kKZMOBKYoghzawthJgUhs" style="width: 100%; height: 500px" :center="center" :zoom="15">
              <Marker v-for="marker in markers" :options="marker" />
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
    const center = { lat: 18.024960, lng: -76.796557 }; //map centred in Kingston by default
    if(navigator.geolocation){ //if location access granted
      navigator.geolocation.getCurrentPosition((position) => {
        center.lat = position.coords.latitude
        center.lng = position.coords.longitude

      fetch('http://localhost:9000/gasstations/search/nearby', {
      body: JSON.stringify({
        'lat': position.coords.latitude,
        'lng': position.coords.longitude 
      }),
      method: "POST"
    })
    .then(result => result.json())
    .then(data => {
        for (var i = 0; i < (data.data).length; i++){
          markers.push({ position: (data.data)[i].geometry.location, label: (data.data)[i].name})
        };
        console.log(markers)
      })
      .catch(error => {
        console.log(error)
      })
      });
    console.log(center)
    }
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