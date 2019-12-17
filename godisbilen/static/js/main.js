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

function addLiveEventListeners(selector, event, handler){
    document.querySelector("body").addEventListener(
         event
        ,function(evt){
            var target = evt.target;
            while (target != null){
                var isMatch = target.matches ? target.matches(selector) : target.msMatchesSelector(selector);
                if (isMatch){
                    handler(evt);
                    return;
                }
                target = target.parentElement;
            }
        }
        ,true
    );
}


var city_boundaries = {};
getJSON("POST", "/get_region_boundaries", function (err, data) {
    if (err !== null) {
        console.log("Something went wrong: " + err);
    } else {
        city_boundaries = data;
    }
});

function get_city_boundaries(callback){
    getJSON("POST", "/get_region_boundaries", callback);
}