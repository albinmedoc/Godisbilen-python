hide_order_number_form_row(true);

document.getElementsByName("subject")[0].addEventListener("input", function(){
    hide_order_number_form_row(this.value != "Angående order")
});

function hide_order_number_form_row(hide){
    var order_number_form_row = document.getElementById("order_number").parentElement.parentElement;
    if(hide){
        order_number_form_row.style.display = "none";
    }else{
        order_number_form_row.style.display = "flex";
    }
}