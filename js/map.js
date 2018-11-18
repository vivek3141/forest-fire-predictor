function addDraggableMarker(map, behavior) {

    var marker = new H.map.Marker({lat: 41.9, lng: -6.85});
    // Ensure that the marker can receive drag events
    marker.draggable = true;
    map.addObject(marker);

    map.addEventListener('dragstart', function (ev) {
        var target = ev.target;
        if (target instanceof H.map.Marker) {
            behavior.disable();
        }
    }, false);

    map.addEventListener('dragend', function (ev) {
        var target = ev.target;
        if (target instanceof mapsjs.map.Marker) {
            behavior.enable();
        }
    }, false);

    map.addEventListener('drag', function (ev) {
        console.log(marker.getCurrentPosition());
        var target = ev.target,
            pointer = ev.currentPointer;
        if (target instanceof mapsjs.map.Marker) {
            target.setPosition(map.screenToGeo(pointer.viewportX, pointer.viewportY));
        }
    }, false);
    const button = document.getElementById("graph");

    button.addEventListener("click", e => {
        console.log("hi");
        var endpoint="https://forest-fire.herokuapp.com/predict?c='";
        const xhr = new XMLHttpRequest();
        xhr.addEventListener("readystatechange", function () {
            if (this.readyState === this.DONE) {
                console.debug(this.responseText);
            }
        });
        xhr.open("GET", endpoint);
        xhr.send();

        var value = 0;
        document.getElementById("text").textContent = value;
    });
}

/**
 * Boilerplate map initialization code starts below:
 */

//Step 1: initialize communication with the platform
var platform = new H.service.Platform({
    app_id: 'devportal-demo-20180625',
    app_code: '9v2BkviRwi9Ot26kp2IysQ',
    useHTTPS: true
});
var pixelRatio = window.devicePixelRatio || 1;
var defaultLayers = platform.createDefaultLayers({
    tileSize: pixelRatio === 1 ? 256 : 512,
    ppi: pixelRatio === 1 ? undefined : 320
});

//Step 2: initialize a map - this map is centered over Boston
var map = new H.Map(document.getElementById('map'),
    defaultLayers.normal.map, {
        center: {lat: 41.9, lng: -6.85},
        zoom: 10,
        pixelRatio: pixelRatio
    });

//Step 3: make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Step 4: Create the default UI:
var ui = H.ui.UI.createDefault(map, defaultLayers, 'en-US');

// Add the click event listener.
addDraggableMarker(map, behavior);
