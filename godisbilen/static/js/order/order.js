var componentForm = {
    street_number: "short_name",
    route: "long_name",
    postal_town: "long_name",
    country: "short_name",
    postal_code: "short_name"
};

var city_boundaries = {};
get_city_boundaries(function (err, cities) {
    if (err === null) {
        for (var city in cities) {
            city_boundaries[city] = new google.maps.Polygon({ paths: cities[city] });

        }
    }
});


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

        var address = '';
        if (place.address_components) {
            address = [
                (place.address_components[0] && place.address_components[0].short_name || ''),
                (place.address_components[1] && place.address_components[1].short_name || ''),
                (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
        }

        infowindowContent.children["place-icon"].src = place.icon;
        infowindowContent.children["place-name"].textContent = place.name;
        infowindowContent.children["place-address"].textContent = address;
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