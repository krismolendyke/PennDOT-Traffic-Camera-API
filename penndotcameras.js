$(document).ready(function() {
(function(window, url, undefined) {

var pennDotCameras = function(url) {
    var DEFAULT = {
        'loc': { // Philly city hall!
            'lat': 39.95251,
            'lng': -75.16342
        },
        'num': 10,
        'callbackParam': '?callback=?'
    };

    var init = function() {
        getCameras();
    };

    var getCameras = function(lat, lng, num) {
        num = num || DEFAULT.num;
        if ((!lat || !lng) && navigator.geolocation) {
            // Exciting current location query!
            navigator.geolocation.getCurrentPosition(function(position) {
                lat = position.coords.latitude || DEFAULT.loc.lat;
                lng = position.coords.longitude || DEFAULT.loc.lng;
                $.getJSON(url + '/' + lat + '/' + lng + '/' + num +
                        DEFAULT.callbackParam, getCamerasSuccessCallback);
            });
        } else {
            // Boring default query.
            lat = lat || DEFAULT.loc.lat;
            lng = lng || DEFAULT.loc.lng;
            $.getJSON(url + '/' + lat + '/' + lng + '/' + num +
                    DEFAULT.callbackParam, getCamerasSuccessCallback);
        }
    };

    var getCamerasSuccessCallback = function(cameras) {
        $.each(cameras, function(index, camera) {
            $('#cameras').append('<h3>' + camera.name +
                    '</h3><p>' + camera.miles_away +
                    ' miles away</p>').append('<img src="' + camera.url +
                    '"/>').append('<hr />');
        });
    };

    init();

    return {
        'getCameras': getCameras
    };
};

window.pennDotCameras = new pennDotCameras(url);

}(window, 'http://localhost:1776')); // For development only!
});
