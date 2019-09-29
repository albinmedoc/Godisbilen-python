var map = null;
var markers = [];
var currrent_pos_marker = undefined;
var currrent_pos_radius = undefined;
var infoWindow = null;

//Uppdatera ordrar vartannan minut
setInterval(function () {
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
                        infowindow.setContent("<a target='_blank' href='https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=" + orders[i]["lat"] + "," + orders[i]["lng"] + "'>" + orders[i]["street"] + " " + orders[i]["street_number"] + "<br><a href='sms:" + orders[i]["tel"] + "'</a>" + orders[i]["tel"]);
                        infowindow.open(map, marker);
                    }
                })(marker, i));
            }
            document.querySelectorAll("#current_order > .order_number")[0].innerHTML = orders[0]["order_number"];
            document.querySelectorAll("#current_order > .address")[0].innerHTML = "<a target='_blank' href='https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=" + orders[0]["lat"] + "," + orders[0]["lng"] + "'>" + orders[0]["street"] + " " + orders[0]["street_number"];
            document.querySelectorAll("#current_order > .phone_number")[0].innerHTML = "<a href='sms:" + orders[0]["tel"] + "'</a>" + orders[0]["tel"];
            if (orders[0]["phase"] == 1) {
                document.querySelectorAll("#current_order > .action")[0].onclick = start_order;
                document.querySelectorAll("#current_order > .action")[0].innerHTML = "Starta";
            } else if (orders[0]["phase"] == 2) {
                document.querySelectorAll("#current_order > .action")[0].onclick = add_products;
                document.querySelectorAll("#current_order > .action")[0].innerHTML = "Avsluta / Lägg till varor";
            }
        }
    }, "phase=1&phase=2");
}

function delete_markers() {
    //Loop through all the markers and remove
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
};

function reload_markers() {
    delete_markers();
    show_markers();
}

function start_order() {
    var order_number = document.querySelectorAll("#current_order > .order_number")[0].innerHTML;
    getJSON("POST", "/admin/start_order", function (err) {
        if (err !== null) {
            alert("Something went wrong: " + err);
        }
    }, "order_number=" + order_number);
    location.reload();
}

function add_products(){
    var order_number = document.querySelectorAll("#current_order > .order_number")[0].innerHTML;
    location.href = location.origin + "/admin/new_purchase?order_number=" + order_number + "&next=admin_route.map";
}