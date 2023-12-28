$( document ).ready(function() {
    console.log("window loaded");
    // https://github.com/d3/d3-request
    d3.csv("hotels_near_cities.csv", function(error, data) {
        if (error) throw error;
        
        console.log(data[0]); // verify data import

        data.forEach((element) => (
            city= element['Hotel City'],
            country=element['Hotel Country'], 
            lat=element['Hotel Latitude'],
            lon=element['Hotel Longitude'],
            hotel=element['Hotel Name'],
            email=element['Hotel Email'],
            address=element['Hotel Address'],
            phone=element['Hotel Phone'],
            website=element['Hotel Website'],
            description=element['Weather'],
            temp=element['Temperature'],
            
            console.log(hotel, city, country, lat, lon, address, phone, website, temp, description),
            
            markerLocation = new L.LatLng(lat, lon),
            marker = new L.Marker(markerLocation),
            map.addLayer(marker),
            marker.bindPopup(hotel + '<br> ' + city + '<br> ' + country + '<br> ' + temp + '<br> ' + description)

            
          

            
            
            
            
            )
           
        // console.log(element['City Name'])
        // markerLocation = new L.LatLng(lat, lon);
        // marker = new L.Marker(markerLocation);
        // map.addLayer(marker);

        // L.marker([oneSighting['latitude'], oneSighting['longitude ']]).addTo(markerLayer)
        // .bindPopup(oneSighting['comments'])
        // .openPopup();

        
        );

        

      });
    
    

        // add map location
        // const map = L.map("map",
        // {   center: [27.34045, -112.26761],
        //     zoom: 13,

        // })
        var map = L.map('map').setView([27.34045, -112.26761], 2);
        L.marker([27.34045, -112.26761]).addTo(map)
    .bindPopup('Santa Rosalia, Mexico.')
    .openPopup();
            
        
        // console.log(data[0]);
        // let slider = data[0];
        let accessToken='pk.eyJ1IjoiY2VyZWphcm9zaW5oYSIsImEiOiJja3ViY2xrdW8wcGMzMnBvMnVkYnIzem9oIn0.4DvP31zPvz6IhpuApq1BZA'
        
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: accessToken
        }).addTo(map);
            
    
})