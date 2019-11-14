document.getElementById("order_btn").addEventListener("click", function(){
    document.getElementById("order_form").classList.add("active");
});

if(document.getElementById("lat").value != ""){
    document.getElementById("order_form").classList.add("active");
}