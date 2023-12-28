function copyToClipboard() {
    var messageText = document.getElementById("message").innerText;
    var tempInput = document.createElement("textarea");
    tempInput.value = messageText;
    document.body.appendChild(tempInput);
    tempInput.select();
    tempInput.setSelectionRange(0, 99999); /* For mobile devices */
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    alert("Copied to clipboard");
}
