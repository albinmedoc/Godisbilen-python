function add_product(e){
    var template = document.getElementById("template").cloneNode(true);
    template.removeAttribute("id");
    var inputs = template.querySelectorAll(".input_container > input");
    console.log(document.getElementById("campaign_form").querySelectorAll(".form_row").length -3);
    for(var i = 0; i < inputs.length; i++){
        var id = "products-" + (document.getElementById("campaign_form").querySelectorAll(".form_row").length -2) + "-" + (inputs[i].type == "text" ? "product": "count");
        inputs[i].name = id;
        inputs[i].id = id;
    }
    document.getElementById("campaign_form").insertBefore(template, e.parentNode.parentNode);
}