const myInput = document.getElementById("signup_email");
const email = document.getElementById("email");
const letter = document.getElementById("letter");

// When the user clicks on the email field, show the message box
myInput.onfocus = function () {
    document.getElementById("message").style.display = "block";
}

// When the user clicks outside the email field, hide the message box
myInput.onblur = function () {
    document.getElementById("message").style.display = "none";
}

// When the user starts to type something inside the email field
myInput.onkeyup = function () {
    // Validate email special char: @
    let emailValidation = /@/g;
    if (myInput.value.match(emailValidation)) {
        email.classList.remove("invalid");
        email.classList.add("valid");
    } else {
        email.classList.remove("valid");
        email.classList.add("invalid");
    }
    // Validate cnam subdomain:
    let cnamValidation = /lecnam.net/g;
    if (myInput.value.match(cnamValidation)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
    } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }
}