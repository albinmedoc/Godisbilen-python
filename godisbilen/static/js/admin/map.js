var map = null;
var markers = [];
var infoWindow = null;

addLiveEventListeners(".pin_complete", "click", function(e){
    if(!confirm("Har du slutfört leveransen?")){
        e.preventDefault();
    }
});

//Uppdatera ordrar vartannan minut
setInterval(function () {
    // Dont reload if no change in database
    // Save the current order_id and compare it with the latest in database
    reload_markers();
}, 120000);

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: new google.maps.LatLng(55.642849, 13.206270),
        disableDefaultUI: true,
        gestureHandling: "greedy",
    });

    infowindow = new google.maps.InfoWindow();
    show_markers();
}

function show_markers() {
    getJSON("POST", "/get_orders", function (err, orders) {
        if (err !== null) {
            alert("Something went wrong: " + err);
        } else {
            if (!orders.length) {
                return;
            }
            for (var i = 0; i < orders.length; i++) {
                var point = new google.maps.LatLng(parseFloat(orders[i]["lat"]), parseFloat(orders[i]["lng"]));
                var icon_color = (orders[i]["phase"] == 1) ? "blue" : "green";

                var marker = new google.maps.Marker({
                    map: map,
                    position: point,
                    icon: "https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_" + icon_color + orders[i]["queue_position"] + ".png",
                });
                markers.push(marker);

                google.maps.event.addListener(marker, "click", (function (marker, i) {
                    return function () {
                        infowindow.setContent("<a target='_blank' href='https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=" + orders[i]["lat"] + "," + orders[i]["lng"] + "'>" + orders[i]["formatted_address"] + "<br><a href='sms:" + orders[i]["tel"] + "'</a>" + orders[i]["tel"] + "<br><a class='pin_complete' href='/admin/complete_order/" + orders[i]["order_number"] + "'>Färdig</a>");
                        infowindow.open(map, marker);
                    }
                })(marker, i));
            }

            document.querySelectorAll("#current_order > .estimated_delivery")[0].innerHTML = "Beräknad leverans: " + orders[0]["estimated_delivery"].substring(11, 16);
            document.querySelectorAll("#current_order > .address")[0].innerHTML = "<a target='_blank' href='https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=" + orders[0]["lat"] + "," + orders[0]["lng"] + "'>" + orders[0]["formatted_address"];
            document.querySelectorAll("#current_order > .phone_number")[0].innerHTML = "<a href='sms:" + orders[0]["tel"] + "'</a>" + orders[0]["tel"];
            if (orders[0]["phase"] == 1) {
                document.querySelectorAll("#current_order > .action")[0].innerHTML = "<a href='/admin/start_order/" + orders[0]["order_number"] + "'>Starta</a>";
            } else if (orders[0]["phase"] == 2) {
                document.querySelectorAll("#current_order > .action")[0].innerHTML = "<a href='/admin/complete_order/" + orders[0]["order_number"] + "'>Färdig</a>";
            }
            document.querySelectorAll("#current_order > .orders_count")[0].innerHTML = "Antal ordrar: " + orders.length;
        }
    }, "phase=1&phase=2");
}

function delete_markers() {
    //Loop through all the markers and remove
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    document.querySelectorAll("#current_order > .order_number")[0].innerHTML = null;
    document.querySelectorAll("#current_order > .estimated_delivery")[0].innerHTML = null;
    document.querySelectorAll("#current_order > .address")[0].innerHTML = null;
    document.querySelectorAll("#current_order > .phone_number")[0].innerHTML = null;
    document.querySelectorAll("#current_order > .action")[0].onclick = null;
    document.querySelectorAll("#current_order > .action")[0].innerHTML = "Ingen order";
};

function reload_markers() {
    delete_markers();
    show_markers();
}