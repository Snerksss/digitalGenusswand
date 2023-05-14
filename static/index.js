import {
    HTTP_JSON_HEADERS,
    HTTP_METHOD_POST,
    REQUEST_URL,
    TOKEN_EXPIRE_HOURS,
    USER_CREATE_USER,
    USER_TOKEN_URL
} from "./constants.js";
import {getCookies, setCookie} from "./util/utils.js";

function login(username, passwd) {
    const params = {"username": username,
                    "password": passwd};
    let form_data = new FormData();

    for (let key in params) {
        form_data.append(key, params[key]);
    }
    const formdataParams = new URLSearchParams(form_data.entries())

    fetch(REQUEST_URL+USER_TOKEN_URL, {method:HTTP_METHOD_POST, body:formdataParams})
    .then( response => {
      if(response.status !== 200){
        document.getElementById("message").classList.remove("display");
        return;
      }
      return response.json();
    })
    .then((data) =>
    {
      if(data){
        setCookie("token", data.access_token, TOKEN_EXPIRE_HOURS);
        window.location.replace("./oneGenusswand/genusswand.html");
      }
    });
}

function signUp(username, email, passwd, form) {
    const params = {"username": username,
                    "passwd": passwd,
                    "email": email};
    const json_params = JSON.stringify(params)
    fetch(REQUEST_URL+USER_CREATE_USER, {method:HTTP_METHOD_POST, headers:HTTP_JSON_HEADERS, body:json_params})
    .then( response => {
      if(response.status !== 201){
        document.getElementById("message").classList.remove("display");
        return;
      }
      form.reset();
      document.getElementById("chk").checked = true;
      return response.json();
    })
}

window.globalLogin = (value) => {
    login(value[0].value, value[1].value);
}

window.globalSignUp = (value) => {
    signUp(value[0].value, value[1].value, value[2].value, value);
}
