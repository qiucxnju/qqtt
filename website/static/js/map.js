$(document).ready(function() {
    console.log("hehe");
    var map = new BMap.Map("allmap");   
    var myGeo = new BMap.Geocoder();
    var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
    var top_left_navigation = new BMap.NavigationControl(); 
    map.addControl(top_left_control);        
    map.addControl(top_left_navigation); 
    console.log("haha");
});
