<template>
    <main id="route-page">
        <div id="title-cnt">
            <div id="title">
                <h2>Getting Directions to {{name}}</h2>
            </div>
            <div id="sub-title">
                <h4>{{address}}</h4>
            </div>
        </div>
        <div id="map-cnt" style="height:100%; width: 100%;">
            <div id="map-c">
                <span v-if="!locationgranted">{{notifmessage}}</span>
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
                notifmessage: '',
                locationgranted: false
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
                    }if (status == 'ZERO_RESULTS'){
                        alert('No route could be found this gas station based on your current location')
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
        }

        },
  
        created(){
            this.id = this.$route.params.id;
            this.loadGasstion()
        },
  
        mounted(){
            if(navigator.geolocation){
                this.locationgranted = true
                navigator.geolocation.getCurrentPosition((position) => {
                        this.locationgranted = true
                        let myposition = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
                        let loadedStationLoc = new google.maps.LatLng(parseFloat(this.lat), parseFloat(this.lng))
                        this.mapCenter = myposition
                        console.log(position)
                        this.initMap()
                        this.setMarker(this.mapCenter, 'You')
                        this.setMarker(loadedStationLoc, 'Gas')
                },this.errorPostion , { enableHighAccuracy : true,timeout: 20000, maximumAge: 0 })
            }
            else{
                this.locationgranted = false;
                this.notifmessage = 'This Broswer does not support Geolocation. Please use a different broswer'
            }

            

        },

    }

</script>

<style>

#title-cnt {
    border: 2px solid #AA1414;
    border-radius: 5px;
    padding: 5px;
    margin-bottom: 50px;
}

#sub-title {
  width: 100%;
  text-align: center;
  font-style: italic;
}

#map-c {
    height: 500px;
    width: 100%;
    text-align: center;
}

span{
    color: #AA1414;
}


</style>