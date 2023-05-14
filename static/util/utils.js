function setCookie(cname, cvalue, exhours) {
    let d = new Date();
    d.setTime(d.getTime() + (exhours*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookies(){
    return document.cookie.split("=")[1].split(":");
   
}

async function fetchTemplate(filename) {
    return fetch(filename)
    .then(response => response.text());
}

function logUserOut() {
    window.location.replace("../index.html");
    document.cookie = document.cookie.split("=")[0].split(":") + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function showErrorMsg(message) {
    document.getElementById("error-msg").innerText = message;
    document.getElementById("error-msg-outer").classList.add("open");
    setTimeout(() => {
        document.getElementById("error-msg-outer").classList.remove("open"); 
    }, 4000);
}

function showSuccessMsg(message) {
    document.getElementById("success-msg").innerText = message;
    document.getElementById("success-msg-outer").classList.add("open");
    setTimeout(() => {
        document.getElementById("success-msg-outer").classList.remove("open"); 
    }, 4000);
}
  

export { 
    setCookie, 
    getCookies, 
    fetchTemplate, 
    logUserOut, 
    showErrorMsg, 
    showSuccessMsg 
}