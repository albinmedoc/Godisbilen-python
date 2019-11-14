document.getElementById("join").addEventListener("click", function(){
    document.getElementById("join_form").classList.add("active");
});

if(document.getElementById("lat").value != ""){
    document.getElementById("join_form").classList.add("active");
}