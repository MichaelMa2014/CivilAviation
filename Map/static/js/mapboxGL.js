/**
 * Created by Liao on 2017/3/2 0002.
 * mapbox GL地图函数
 */
mapboxgl.accessToken = 'pk.eyJ1Ijoic3R1cGlnIiwiYSI6ImNpanV2c211bTBoaGp0c204cDFhNGltMW8ifQ.i2d7l3ljIr4GvyLWj6Hh3w';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    zoom: 5,
    minZoom: 2,
    center: [116.46, 39.92],
    renderWorldCopies: true,
});
map.on('zoomend',function () {
    test1();
});
map.on('moveend',function(){
    test1();
});

map.on('click', function (e) {
    if(e.originalEvent.target.id.match('flight_marker'))
    {
        id = e.originalEvent.target.id.replace('flight_marker_','')
        document.getElementsByClassName('table')[0].innerHTML = '这是table_'+id;
        jQuery.ajax({
            url: "/getDataByID/" + id,
            success: function (data) {
                flightinfo = data;
                console.log(data);
            }
        });
        console.log(e.originalEvent.target.id);
    }

});

function stdlnglat(lnglats){
    s = []
    lnglats.forEach(function (array) {
        array.forEach(function (num) {
            s.push(Math.ceil(num))
        })
    })
    return s;
}
function test() {
    jQuery.ajax({
        url: "/getDataByDate/2017-01-23",
        success: function (data) {
            console.log(new Date().getSeconds())
            console.log("Successfully load data from API server.");

            for(var i in data) {
                var img = document.createElement('img');
                    img.src = '../static/images/airplane_2.svg'
                    img.style.width = '30px';
                    img.style.height = '30px';

                    // add marker to map
                    var m = new mapboxgl.Marker(img)
                        .setLngLat([data[i].lon,data[i].lat])
                        .addTo(map);
            }
            console.log(new Date().getSeconds());
            console.log("Successfully draw pushpins");
        }
    })
}
function test1() {
    jQuery.ajax({
        url: "/getDataByRect/"+stdlnglat(map.getBounds().toArray())+','+Math.ceil(map.getZoom()),
        success: function (data) {
            parent = document.getElementsByClassName('mapboxgl-canvas-container mapboxgl-interactive')[0];
            while(parent.childNodes.length > 1)
            {
                parent.removeChild(parent.lastChild);
            }
            for(var i in data) {
                var img = document.createElement('img');
                    img.src = '../static/images/airplane_2.svg';
                    img.id = 'flight_marker_' + data[i].id;
                    img.style.width = '30px';
                    img.style.height = '30px';

                    // add marker to map
                    var m = new mapboxgl.Marker(img)
                            .setLngLat([data[i].lon,data[i].lat])
                            .addTo(map);
            }
        }
    })
}
function getTableHTML() {

}
test1();
