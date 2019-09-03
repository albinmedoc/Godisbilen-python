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
    var input = document.getElementById("full_adress");

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setComponentRestrictions(
        { "country": ["swe"] });
    autocomplete.setFields(
        ["address_components", "geometry", "icon", "name"]);

    autocomplete.addListener("place_changed", function () {
        var place = autocomplete.getPlace();

        for (var component in componentForm) {
            document.getElementById(component).value = "";
            document.getElementById(component).disabled = false;
        }

        for (var i = 0; i < place.address_components.length; i++) {
            var addressType = place.address_components[i].types[0];
            if (componentForm[addressType]) {
                var val = place.address_components[i][componentForm[addressType]];
                document.getElementById(addressType).value = val;
            }
        }
        document.getElementById("lat").value = place.geometry.location.lat();
        document.getElementById("lng").value = place.geometry.location.lng();

        //Rensar felmeddelande
        document.getElementById("full_adress").nextElementSibling.nextElementSibling.innerHTML = "";
        document.getElementById("submit").removeAttribute("disabled");

        //Visar felmeddelande

        //Kontrollerar gatunummer
        if (!document.getElementById("street_number").value) {
            show_error("Gatunummer saknas");
        }
        //Kontrollerar gatunummer
        if (!document.getElementById("route").value) {
            show_error("Gata saknas");
        }
        //Kontrollerar gatunummer
        if (!document.getElementById("postal_town").value) {
            show_error("Stad saknas");
        }
        //Kontrollerar gatunummer
        if (!document.getElementById("postal_code").value) {
            show_error("Postnummer saknas");
        }
        //Hoppar över resten av koden om det finns felmeddelande
        if (document.getElementById("full_adress").nextElementSibling.nextElementSibling.innerHTML) {
            return;
        }

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

        //Kontrollerar om address är inom arbetsområde
        var inside = false;
        for (var city in city_boundaries) {
            if (google.maps.geometry.poly.containsLocation(place.geometry.location, city_boundaries[city])) {
                inside = true;
            }
        }
        if (!inside) {
            //Load city boundries
            get_city_boundaries(function (err, cities) {
                if (err === null) {
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
                    console.log(bounds.getCenter().lat() + ", " + bounds.getCenter().lng());
                    map.fitBounds(bounds);
                }
            });
        }
    });

    function show_error(message) {
        var error = document.createElement("p");
        error.classList.add("error");
        error.innerHTML = message;
        document.getElementById("full_adress").nextElementSibling.nextElementSibling.appendChild(error);
        document.getElementById("submit").setAttribute("disabled", "disabled");
    }

    var infowindow = new google.maps.InfoWindow();
    var infowindowContent = document.getElementById("infowindow-content");
    infowindow.setContent(infowindowContent);
    var marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0, -29)
    });
}