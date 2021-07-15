function search_driver(host,port,trip_id) {
    var xhr = new XMLHttpRequest();
    var url = 'http://'+host+':'+port+'/search_driver';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("trip_id="+trip_id);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var driver_id = xhr.responseText
            var new_t = document.createElement("p");
            new_t.innerText = "driver id is : " + driver_id;
            document.body.replaceChild(new_t,t);
            startTimer(host,port,driver_id);
        }
    };
    var button = document.getElementById("button");
    button.parentNode.removeChild(button);
    var t = document.createElement("p"); 
    t.innerText = "Searching for driver";
    document.body.appendChild(t);
}

function startTimer(host,port,driver_id){
    window.host = host;
    window.port = port;
    window.driver_id = driver_id;
    window.longitude = document.createElement("p"); 
    window.longitude.innerText = "Updating the longitude of driver location";
    document.body.appendChild(window.longitude);
    window.latitude = document.createElement("p"); 
    window.latitude.innerText = "Updating the latitude of driver location";
    document.body.appendChild(window.latitude);
    var timer = window.setInterval(update_driver_location,1000)
    var xhr = new XMLHttpRequest();
    var url = 'http://'+host+':'+port+'/get_driver_detail';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("driver_id="+driver_id);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var data = JSON.parse(xhr.response);
            var driver_name = document.createElement("p");
            var phone_number = document.createElement("p");
            driver_name.innerText = "driver name is : " + data["driver_name"];
            phone_number.innerText = "driver phone_number is : " + data["phone_number"];
            document.body.appendChild(driver_name);
            document.body.appendChild(phone_number);
        }
    };
};

function update_driver_location(){
    var xhr = new XMLHttpRequest();
    var url = 'http://'+window.host+':'+window.port+'/update_driver_location';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("driver_id="+window.driver_id);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var data = JSON.parse(xhr.response)
            window.longitude.innerText = "logitude of driver location is : "+data['longitude'];
            window.latitude.innerText = "latitude of driver location is : "+data['latitude'];
        }
    };
}
