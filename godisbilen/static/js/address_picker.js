// Requires map element and #search, #lat, #lng input fields
function initMap() {
    var map = new google.maps.Map(document.getElementById("map"), {
        disableDefaultUI: true
    });

    //Setup autocomplete
    var input = document.getElementById("search");

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setComponentRestrictions(
        { "country": ["swe"] });
    autocomplete.setFields(
        ["address_components", "geometry", "icon", "name"]);


    // Create the infoWindow
    var infowindow = new google.maps.InfoWindow();
    var infowindowContent = document.getElementById("infowindow-content");
    infowindow.setContent(infowindowContent);
    infowindow.close();

    // Create the marker
    var marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0, -29)
    });

    function set_location(place){
        // Set lat & lng to the place specified by the user
        document.getElementById("lat").value = place.geometry.location.lat();
        document.getElementById("lng").value = place.geometry.location.lng();

        marker.setVisible(false);

        // Show the map
        document.getElementById("map").parentElement.classList.add("active");
        if (!place.geometry) {
            alert("No details available for input: '" + place.name + "'");
            return;
        }
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
        }
        map.setZoom(16);
        
        // Show the marker
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        // Set infoWindow content and show it
        infowindowContent.children["place-name"].textContent = place.address_components[1].long_name + " " + place.address_components[0].short_name;
        if(place.address_components[6] && place.address_components[6].short_name && place.address_components[3] && place.address_components[3].short_name){
            infowindowContent.children["postal"].textContent = place.address_components[6].short_name + " " + place.address_components[3].short_name;
        }
        infowindow.open(map, marker);
    }

    autocomplete.addListener("place_changed", function () {
        var place = autocomplete.getPlace();
        set_location(place);
    });

    var autofill = document.getElementById("autofill");
    if(autofill){
        // Add event listener
        autofill.addEventListener("click", function(){
            // Show the loader
            showLoader(true);

            // Check if browser supports geolocation
            if(navigator.geolocation){

                // Get the users location
                navigator.geolocation.getCurrentPosition(function(position){
                    var geocoder = new google.maps.Geocoder;
                    var latlng = new google.maps.LatLng({lat: position.coords.latitude, lng: position.coords.longitude});
                    // Get the place from the coordinates
                    geocoder.geocode({'location': latlng}, function(results, status) {
                        if (status === "OK" && results[0]) {
                            // Show location
                            set_location(results[0]);
                        }
                    });
                });
            }else{
                alert("Geolocation is not supported by this browser.");
            }

            // Hide the loader
            showLoader(false);
        });
    }
}