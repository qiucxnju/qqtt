$(document).ready(function() {
    console.log("hehe");
    var map = new BMap.Map("allmap");   
    map.centerAndZoom(new BMap.Point(121.494543,31.31042), 17);  
    map.enableScrollWheelZoom(true);    
    var myGeo = new BMap.Geocoder();
    var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
    var top_left_navigation = new BMap.NavigationControl(); 
    map.addControl(top_left_control);        
    map.addControl(top_left_navigation); 
    console.log("haha");
     myGeo.getPoint("仁德苑", function(point){
         console.log(point);
           },"上海市");

    /*
    */
});
