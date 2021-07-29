function check_token(in_show_trip=false) {
    window.token = localStorage.getItem("token");
    window.trip_ongoing = localStorage.getItem("trip_ongoing")
    if (window.token == null){
        window.alert("you are not logged in")
        window.location.replace('http://'+window.location.host+'/login');
    }
    if (window.trip_ongoing != null && in_show_trip == false){
        window.alert("you have one ongoing trip")
        window.location.replace('http://'+window.location.host+'/show_trip'+'/'+localStorage.getItem("trip_id"));
    }
}
