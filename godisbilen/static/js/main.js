var getJSON = function (method, url, callback, params) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.responseType = "json";
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    if (params == undefined) {
        params = "";
    }
    xhr.send(params);
};


var city_boundaries = {};
getJSON("POST", "/get_city_boundaries", function (err, data) {
    if (err !== null) {
        console.log("Something went wrong: " + err);
    } else {
        city_boundaries = data;
    }
});

function get_city_boundaries(callback, cities){
    getJSON("POST", "/get_city_boundaries", callback);
}