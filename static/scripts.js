// function to check register page
// make sure everything is
function ccheck() {

    var x;
    var y;
    var z;
    var a;

    y = document.getElementById("order").value;
    if (isNaN(y)) {
        alert("Order number is supposed to be numeric");
        return false;
    }

    z = document.getElementById("price").value;
    if (isNaN(z)) {
        alert("Price is supposed to be numeric");
        return false;
    }

    x = document.getElementById("phone").value;
    x = change(x);

    // function to remove all letters and spec characters
    function change(x) {

        x = x.replace(/[^0-9]/g, "");
        return x;

    }

    document.getElementById("phone").value = x;

    // make sure the lenght of phone number is 10
    a = x.toString().length;
    if (a != 10) {
        alert("Incorrect phone number format");
        return false;
    }
}


// strip the phone number + make sure that user entered at least something
function find() {

    var x;
    var y;
    var z;
    var o;

    x = document.getElementById("order").value;
    y = document.getElementById("last").value;
    z = document.getElementById("phone").value;
    o = document.getElementById("d_in").value;

    z = change(z);

    // actually remove everything but numbers
    function change(z) {

        z = z.replace(/[^0-9]/g, "");
        return z;

    }

    document.getElementById("phone").value = z;

    x = x.toString().length;
    y = y.toString().length;
    z = z.toString().length;
    o = o.toString().length;

    // check if its empty
    if (x == "" && y == "" && z == "" && o == "") {
        alert("You must provide some information");
        return false;
    }
}


// for deletion we need both fields
function cconfirm() {

    var x;
    var y;

    x = document.getElementById("id").value;
    y = document.getElementById("order").value;

    x = x.toString().length;
    y = y.toString().length;

    // make sure they are not empty
    if (x == "" || y == "") {
        alert("You must provide all information");
        return false;
    }

    // making sure
    var a;
    a = confirm("Are you sure?");
    if (a == false) {
        return false;
    }

}


// for estimate we need all that info
function estimate() {

    var total = 0;

    var rb = document.getElementById("rb");
    calc(rb);
    var lbat = document.getElementById("lbat");
    calc(lbat);
    var bc = document.getElementById("bc");
    calc(bc);
    var wt = document.getElementById("wt");
    calc(wt);
    var min = document.getElementById("min");
    calc(min);
    var mins = document.getElementById("mins");
    calc(mins);
    var pl = document.getElementById("pl");
    calc(pl);
    var pls = document.getElementById("pls");
    calc(pls);
    var sap = document.getElementById("sap");
    calc(sap);
    var saps = document.getElementById("saps");
    calc(saps);
    var lb = document.getElementById("lb");
    calc(lb);
    var prlb = document.getElementById("prlb");
    calc(prlb);
    var rub = document.getElementById("rub");
    calc(rub);
    var ny = document.getElementById("ny");
    calc(ny);
    var bra = document.getElementById("bra");
    calc(bra);
    var prbra = document.getElementById("prbra");
    calc(prbra);
    var crown = document.getElementById("crown");
    calc(crown);
    var prcrown = document.getElementById("prcrown");
    calc(prcrown);
    var hand = document.getElementById("hand");
    calc(hand);
    var hands = document.getElementById("hands");
    calc(hands);
    var marker = document.getElementById("marker");
    calc(marker);
    var clean = document.getElementById("clean");
    calc(clean);
    var refcase = document.getElementById("refcase");
    calc(refcase);
    var refbra = document.getElementById("refbra");
    calc(refbra);


    // calculate the total
    function calc(x) {
        if (x.checked == true) {
            total += parseInt(x.value, 10);
        }
    }
    document.getElementById("total").innerHTML = "$" + total;
}

