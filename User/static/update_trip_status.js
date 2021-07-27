var Trip_status = {
    Created : 1,
    Accepted : 2,
    Ongoing : 3,
    Finished : 4,
};

function search_driver(host,port,trip_id) {
    localStorage.setItem("trip_ongoing","true");
    window.trip_id = trip_id;
    var xhr = new XMLHttpRequest();
    var url = 'http://'+window.location.host+'/search_driver';
    xhr.open('post', url, true);
    xhr.setRequestHeader('token', localStorage.getItem("token"))
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("trip_id="+trip_id);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            console.info("--------------------")
            console.info(xhr.responseText)
            console.info("--------------------")
            if (xhr.responseText == "expired"){
                window.alert("you need to login again")
                window.location.replace('http://'+window.location.host+'/login');
            }
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
};

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
    var timer = window.setInterval(get_driver_location,1000);
    var xhr = new XMLHttpRequest();
    var url = 'http://'+window.location.host+'/get_driver_detail';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader('token', localStorage.getItem("token"));
    xhr.send("driver_id="+driver_id);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.responseText == "expired"){
                clearTimeout(timer);
                window.alert("you need to login again");
                window.location.replace('http://'+window.location.host+'/login');
            }
            var data = JSON.parse(xhr.response);
            var driver_name = document.createElement("p");
            var phone_number = document.createElement("p");
            driver_name.innerText = "driver name is : " + data["driver_name"];
            phone_number.innerText = "driver phone_number is : " + data["phone_number"];
            document.body.appendChild(driver_name);
            document.body.appendChild(phone_number);
            var trip_status = document.createElement("BUTTON");
            trip_status.innerText = "I am picked up";
            trip_status.onclick = function(){update_trip_status(window.trip_id,Trip_status.Ongoing)};
            trip_status.setAttribute("id","trip_status");
            document.body.appendChild(trip_status);
        }
    };
};

function update_trip_status(trip_id,status){
    if (status==Trip_status.Finished){
        localStorage.removeItem("trip_ongoing");
        var url = 'http://'+window.location.host+'/booking';
        window.location.replace(url);
    }
    var xhr = new XMLHttpRequest();
    var url = 'http://'+window.location.host+'/update_trip_status';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader('token', localStorage.getItem("token"))
    xhr.send("trip_id="+trip_id+'&'+"status="+status);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.responseText == "expired"){
                window.alert("you need to login again")
                window.location.replace('http://'+window.location.host+'/login');
            }
            trip_status = document.getElementById("trip_status");
            trip_status.innerText = "I am dropped off";
            trip_status.onclick = function(){
                update_trip_status(window.trip_id,Trip_status.Finished);
            };
        };
    };
};

function get_driver_location(){
    var xhr = new XMLHttpRequest();
    var url = 'http://'+window.location.host+'/get_driver_location';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader('token', localStorage.getItem("token"))
    xhr.send("driver_id="+window.driver_id);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.responseText == "expired"){
                window.alert("you need to login again")
                window.location.replace('http://'+window.location.host+'/login');
            }
            var data = JSON.parse(xhr.response);
            window.longitude.innerText = "logitude of driver location is : "+data['longitude'];
            window.latitude.innerText = "latitude of driver location is : "+data['latitude'];
        };
    };
};
