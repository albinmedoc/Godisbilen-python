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

    autocomplete.addListener("place_changed", function () {
        var place = autocomplete.getPlace();
        document.getElementById("lat").value = place.geometry.location.lat();
        document.getElementById("lng").value = place.geometry.location.lng();

        document.getElementById("map").parentElement.classList.add("active");
        infowindow.close();
        marker.setVisible(false);
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
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        infowindowContent.children["place-icon"].src = place.icon;
        infowindowContent.children["place-name"].textContent = place.name;
        if(place.address_components[6] && place.address_components[6].short_name && place.address_components[3] && place.address_components[3].short_name){
            infowindowContent.children["postal"].textContent = place.address_components[6].short_name + " " + place.address_components[3].short_name;
        }
        infowindow.open(map, marker);
    });

    var infowindow = new google.maps.InfoWindow();
    var infowindowContent = document.getElementById("infowindow-content");
    infowindow.setContent(infowindowContent);
    var marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0, -29)
    });
}