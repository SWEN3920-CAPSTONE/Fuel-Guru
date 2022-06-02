<template>
    <main id="route-page">
        <div id="title">
            <h2>Getting Directions to {{name}}</h2>
        </div>
        <div id="sub-title">
            <h4>{{address}}</h4>
        </div>
        <div id="map-cnt" style="height:100%; width: 100%;">
            <div id="map-c">
                <!-- <span v-if="!locationgranted">Please give location permissions</span> -->
            </div>
        </div>
      
    </main>
</template>

<script>


    export default {
        name: 'RouteMap',
        data(){
            return {
                map: null,
                mapCenter: {lat: 18.024960, lng: -76.796557 },
                name: '',
                address: '',
                lat: 19.024960,
                lng: -76.796557,
            }
        },

        methods: {
            loadGasstion(){
                fetch('http://localhost:9000/gasstations/'+this.id, {
       
                method: "GET"
                })
                .then(result => result.json())
                .then(data => {
                    this.loadedStation = data.data;
                    this.name = this.loadedStation.name
                    this.address = this.loadedStation.address
                    this.lat = this.loadedStation.lat
                    this.lng = this.loadedStation.lng
                })
            },

            initMap(){
                console.log('initMap')
                var directionsService = new google.maps.DirectionsService();
                var directionsRenderer = new google.maps.DirectionsRenderer();
                var loadedStationLoc = new google.maps.LatLng(parseFloat(this.lat), parseFloat(this.lng));
                this.map = new google.maps.Map(document.getElementById('map-c'), {
                    center: this.mapCenter,
                    zoom: 14,
                })

                let request = {
                    origin: this.mapCenter,
                    destination: loadedStationLoc,
                    travelMode: 'DRIVING',
                };

                directionsRenderer.setMap(this.map);
                directionsService.route(request, function(result, status) {
                    if (status == 'OK') {
                        directionsRenderer.setDirections(result);
                    }else{
                        console.log(status)
                    }
                 });
            },

            setMarker(Points, Label){
                const markers = new google.maps.Marker({
                    position:Points,
                    map: this.map,
                    label: {
                        text: Label,
                        color: '#FFF'
                    }
                })
            },

            errorPostion(error) {
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

        },

        created(){
            this.id = this.$route.params.id;
            this.loadGasstion()
        },

       

        mounted(){
            if(navigator.geolocation){
                navigator.geolocation.getCurrentPosition((position) => {
                        this.mapCenter.lat = position.coords.latitude
                        this.mapCenter.lng = position.coords.longitude
                        console.log(position)
                        this.initMap()
                        this.setMarker(this.mapCenter, 'A')
                        this.setMarker({lat: this.lat, lng: this.lng}, 'B')
                },this.errorPostion , { enableHighAccuracy : true,timeout: 20000, maximumAge: 0 })
            }
            else{

            }

            

        },

    }

</script>

<style>
#sub-title {
  width: 100%;
  text-align: center;
  font-style: italic;
}

#map-c {
    height: 500px;
    width: 100%
}


</style>