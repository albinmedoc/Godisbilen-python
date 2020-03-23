// -- Loading form from URL --
const urlParams = new URLSearchParams(window.location.search);
var name = urlParams.get("name") || "";
document.getElementById("name").value = name;
var email = urlParams.get("email") || "";
document.getElementById("email").value = email;
var subject = urlParams.get("subject") || "";
document.getElementById("subject").parentElement.childNodes[2].value = subject;
var order_number = urlParams.get("order_number") || "";
document.getElementById("order_number").value = order_number;
var message = urlParams.get("message") || "";
if(message != ""){
    message = replaceAll(message, "%0A", "\n");
}
document.getElementById("message").value = message;


function show_hide_order_number(){
    var order_number_input = document.getElementById("order_number").parentElement.parentElement;
    var subject_value = document.getElementsByName("subject")[0].value;
    if(subject_value !== "Angående order"){
        order_number_input.style.display = "none";
    }else{
        order_number_input.style.display = "flex";
    }
}

// -- Hiding and showing order_number input -- 
show_hide_order_number();
document.getElementsByName("subject")[0].addEventListener("input", function(){
    show_hide_order_number();
});

// Autosize message
var autosize = new AutosizeTextarea(document.getElementById("message"));