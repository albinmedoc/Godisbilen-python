var map = null;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        disableDefaultUI: true
    });
    show_cities();
}

function show_cities(){
    get_city_boundaries(function(err, cities){
        if (err !== null) {
            alert("Kunde inte ladda in leveransområden!");
        }
        var bounds = new google.maps.LatLngBounds();
        for (var city in cities) {
            console.log("Rendering outline for: " + city);
            var outline = new google.maps.Polygon({
                paths: cities[city],
                strokeColor: "#00FF00",
                strokeOpacity: 1.0,
                strokeWeight: 3,
                fillColor: "#00FF00",
                fillOpacity: 0.35,
            });
            outline.setMap(map);
            for (var i = 0; i < cities[city].length; i++) {
                bounds.extend(cities[city][i]);
            }
        }
        map.fitBounds(bounds);
    });
}