if(!!document.getElementById("order_btn") && !!document.getElementById("address_picker_form")){
    document.getElementById("order_btn").addEventListener("click", function(){
        document.getElementById("address_picker_form").classList.add("active");
    });

    if(document.getElementById("lat").value != ""){
        document.getElementById("address_picker_form").classList.add("active");
    }
}