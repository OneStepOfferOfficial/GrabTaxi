var timer;
function search_driver() {
    // timer = setInterval(update_status(),4000);
    var xhr = new XMLHttpRequest();
    xhr.open('post', 'http://127.0.0.1:5002/update_trip_status',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("trip_id='{{trip_id}}'");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var driver_id = xhr.responseText
            var new_t = document.createElement("p");
            new_t.innerText = "driver id is : " + driver_id;
            document.body.replaceChild(new_t,t);
            
        }
    };
    var t = document.createElement("p"); 
    // document.body.removeChild(t);   
    t.innerText = "Searching for driver";
    document.body.appendChild(t);
}

function update_status(){
    var myForm = document.createElement("form"); 
    myForm.method = "post"; 
    myForm.action = "http://localhost:5002/update_trip_status"; 
    var myInput = document.createElement("input");  
    myInput.type = "text";  
    myInput.name="trip_id";  
    myInput.value="{{trip_id}}";  
    console.log(myInput.value);
    myForm.appendChild(myInput); 
    document.body.appendChild(myForm);  
    myForm.submit();  
    document.body.removeChild(myForm);
}

function stopTimer() {
    alert("Timer stopped");
    clearInterval(timer); 
}

document.getElementById('test-button').addEventListener('click', search_driver);
