function bulmaForm() {
    var row1 = document.getElementById("_card_container_row1");
    row1.classList.add("field");

    var cardlabel = document.getElementById("_card_number_label");
    cardlabel.classList.add("label");

    var cardinput = document.getElementById("_card_number");
    cardinput.classList.add("input");

    var row2 = document.getElementById("_card_container_row2");
    row2.classList.add("field-body", "is-horizontal", "field");

    var expirylabel = document.getElementById("_expiry_label");
    expirylabel.classList.add("label", "field");

    var expiryinput = document.getElementById("_expiry");
    expiryinput.classList.add("input");

    var cvvlabel = document.getElementById("_cvv_label");
    cvvlabel.classList.add("label", "field");
    
    var cvvinput = document.getElementById("_cvv");
    cvvinput.classList.add("input");

    var submitbutton = document.getElementById("_submit_button");
    submitbutton.classList.add("button", "is-info");
}


// class jc_expiryLabel = label
// class jc_expiryInput = input
// class jc_cvvLabel = label
// class jc_cvvInput = input
// id _submit_button = button is-info