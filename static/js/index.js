//////////////////////////////////////// For Mobile view menus//////////////////////////////////////////


var sidenav = document.getElementById('sidenav');
var menubar = document.getElementById('menubar');
var closemark = document.getElementById('closemark');

sidenav.style.width = "0px";
menubar.onclick = () => {
    if (sidenav.style.width == "0px") {
        sidenav.style.width = "100%";
        sidenav.style.height = "167vh"
    }
    else {

        sidenav.style.width = "0px";
    }
}

closemark.onclick = () => {
    sidenav.style.width = "0px";
}

//////////////////////////////////// Sidenav2////////////////////////////////

const sidenav1 = document.getElementById('sidenav1');
const menubar1 = document.getElementById('cartitems');
const closemark1 = document.getElementById('closemark1');
const overlay = document.getElementById('overlay');

sidenav1.style.width = "0px";
menubar1.onclick = () => {
    if (sidenav1.style.width == "0px") {
        sidenav1.style.width = "2rem";
        // sidenav1.style.height = "167vh"
        document.body.style['overflow-y'] = 'hidden';
        if (window.matchMedia('(max-width: 991.98px)').matches) {
            sidenav1.style.width = "24rem";
        }
        else {
            sidenav1.style.width = "30rem";
        }
    }
    else {

        sidenav1.style.width = "0px";
    }
}


closemark1.onclick = () => {
    sidenav1.style.width = "0px";
    document.body.style['overflow-y'] = 'auto';
}

///////////////////////////////////Meet the team Card-1

function mycarda() {
    var dots1 = document.getElementById("dotscard-a");
    var moreText1 = document.getElementById("morecard-a");
    var btnText1 = document.getElementById("mycard-a");

    if (dots1.style.display === "none") {
        dots1.style.display = "inline";
        btnText1.innerHTML = "Read more";
        moreText1.style.display = "none";
    } else {
        dots1.style.display = "none";
        btnText1.innerHTML = "Read less";
        moreText1.style.display = "inline";
    }
}

///////////////////////////////////Meet the team Card-2
function mycardb() {
    var dots1 = document.getElementById("dotscard-b");
    var moreText1 = document.getElementById("morecard-b");
    var btnText1 = document.getElementById("mycard-b");

    if (dots1.style.display === "none") {
        dots1.style.display = "inline";
        btnText1.innerHTML = "Read more";
        moreText1.style.display = "none";
    } else {
        dots1.style.display = "none";
        btnText1.innerHTML = "Read less";
        moreText1.style.display = "inline";
    }
}
///////////////////////////////////Meet the team Card-3
function mycardc() {
    var dots1 = document.getElementById("dotscard-c");
    var moreText1 = document.getElementById("morecard-c");
    var btnText1 = document.getElementById("mycard-c");

    if (dots1.style.display === "none") {
        dots1.style.display = "inline";
        btnText1.innerHTML = "Read more";
        moreText1.style.display = "none";
    } else {
        dots1.style.display = "none";
        btnText1.innerHTML = "Read less";
        moreText1.style.display = "inline";
    }
}
///////////////////////////////////Meet the team Card-4
function mycardd() {
    var dots1 = document.getElementById("dotscard-d");
    var moreText1 = document.getElementById("morecard-d");
    var btnText1 = document.getElementById("mycard-d");

    if (dots1.style.display === "none") {
        dots1.style.display = "inline";
        btnText1.innerHTML = "Read more";
        moreText1.style.display = "none";
    } else {
        dots1.style.display = "none";
        btnText1.innerHTML = "Read less";
        moreText1.style.display = "inline";
    }
}
///////////////////////////////////Meet the team Card-5
function mycarde() {
    var dots1 = document.getElementById("dotscard-e");
    var moreText1 = document.getElementById("morecard-e");
    var btnText1 = document.getElementById("mycard-e");

    if (dots1.style.display === "none") {
        dots1.style.display = "inline";
        btnText1.innerHTML = "Read more";
        moreText1.style.display = "none";
    } else {
        dots1.style.display = "none";
        btnText1.innerHTML = "Read less";
        moreText1.style.display = "inline";
    }
}
///////////////////////////////////Meet the team Card-6
function mycardf() {
    var dots1 = document.getElementById("dotscard-f");
    var moreText1 = document.getElementById("morecard-f");
    var btnText1 = document.getElementById("mycard-f");

    if (dots1.style.display === "none") {
        dots1.style.display = "inline";
        btnText1.innerHTML = "Read more";
        moreText1.style.display = "none";
    } else {
        dots1.style.display = "none";
        btnText1.innerHTML = "Read less";
        moreText1.style.display = "inline";
    }
}

/////////////////////////////// Magnifying Product Image

const options = {
    width: 400,
    height: 250,
    zoomWidth: 400,
    offset: {
        vertical: 0, horizontal: 10
    },
    scale: 1.5,
}


// if we want to change the image on click in products page






