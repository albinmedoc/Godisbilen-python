document.getElementById("join").addEventListener("click", function(){
    document.getElementById("address_picker_form").classList.add("active");
});

if(document.getElementById("lat").value != ""){
    document.getElementById("address_picker_form").classList.add("active");
}