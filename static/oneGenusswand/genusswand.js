import {getCookies, showErrorMsg} from "../util/utils.js";

import {
    GENUSSWAND_CREATE_NEW_GENUSSWAND,
    GENUSSWAND_CREATE_NEW_STRICH_V1,
    GENUSSWAND_DELETE_STRICH_V1,
    GENUSSWAND_GET_SPECIFIC_WAND,
    GENUSSWAND_GET_USER_WAENDE,
    HTTP_AUTH_HEADERS,
    HTTP_JSON_HEADERS_WITH_AUTH,
    HTTP_METHOD_DELETE,
    HTTP_METHOD_GET,
    HTTP_METHOD_POST,
    REQUEST_URL
} from "../constants.js";

const token = getCookies();
let uuid = "";

function fetchGenusswandOverview() {
    fetch(REQUEST_URL + GENUSSWAND_GET_USER_WAENDE, {
        method: HTTP_METHOD_GET, headers: HTTP_AUTH_HEADERS(token)
    })
        .then(response => response.json())
        .then(data => {
            buildTableOverviewGenusswaende(table, data)
        })
}

function buildTableOverviewGenusswaende(table, data) {
    let innerhtml = "<tr><th width='800px'>Genusswand</th></tr>";
    data.forEach(function (value) {
        innerhtml += buildRowOverviewGenusswand(value.name, value.uuid);
    })
    innerhtml += buildInputRowOverviewGenusswand();
    table.innerHTML = innerhtml;

    function buildInputRowOverviewGenusswand() {
        let neueGenusswand = "<td>" +
            "<input type='text' id='addGenusswand' name='addGenusswand' required> " +
            "<input type='button' name='button' Value='ADD' onclick='globalAddGenusswand()'>" +
            "</td>";
        return "<tr id='addRow'>" + neueGenusswand + "</tr>";
    }
}

function buildRowOverviewGenusswand(name, uuid) {
    let dataPart = "<td >" + name + "</td>"
    uuid = '"' + uuid + '"';
    name = '"' + name + '"';
    return "<tr class='hoverEffect' onclick='globalFetchSpecificGenusswand(" + uuid + "," + name + ")'>" + dataPart + "</tr>";
}

function addGenusswand(name) {
    const params = {"name": name};
    const json_params = JSON.stringify(params);
    fetch(REQUEST_URL + GENUSSWAND_CREATE_NEW_GENUSSWAND, {
        method: HTTP_METHOD_POST,
        headers: HTTP_JSON_HEADERS_WITH_AUTH(token),
        body: json_params
    })
        .then((response) => {
            if (response.ok) {
                fetchGenusswandOverview();
            }
        });
}

function fetchGenusswand(pUuid, nameGenusswand) {
    uuid = pUuid;
    fetch(REQUEST_URL + GENUSSWAND_GET_SPECIFIC_WAND + pUuid, {
        method: HTTP_METHOD_GET, headers: HTTP_AUTH_HEADERS(token)
    })
        .then(response => response.json())
        .then(data => {
            buildTableSpecificWand(table, data, nameGenusswand)
        })
}

function addStrich(mistaker) {
    let json = {
        "mistaker": mistaker, "uuid_genusswand": uuid
    }
    fetch(REQUEST_URL + GENUSSWAND_CREATE_NEW_STRICH_V1, {
        method: HTTP_METHOD_POST, headers: HTTP_JSON_HEADERS_WITH_AUTH(token), body: JSON.stringify(json)
    })
        .then((response) => {
            if (response.ok) {
                fetchGenusswand(uuid, document.getElementById("genusswandHeader").innerHTML);
            }
        });
}

function deleteStrich(mistaker) {
    let json = {
        "mistaker": mistaker, "uuid_genusswand": uuid
    }
    fetch(REQUEST_URL + GENUSSWAND_DELETE_STRICH_V1, {
        method: HTTP_METHOD_DELETE, headers: HTTP_JSON_HEADERS_WITH_AUTH(token), body: JSON.stringify(json)
    }).then((response) => {
        if (response.ok) {
            fetchGenusswand(uuid, document.getElementById("genusswandHeader").innerHTML);
        } else {
            showErrorMsg(response.text);
        }
    });
}

function buildTableSpecificWand(table, data, nameGenusswand) {
    document.getElementById("genusswandHeader").innerHTML = nameGenusswand;
    let innerhtml = "<tr><th width='20%'>Beschuldigter</th><th>Anzahl Vergehen</th><th width='10%'>EDIT</th></tr>";
    data.mistakers.forEach(function (value) {
        innerhtml += buildRowSpecificWand(value.mistaker, value.counter);
    })
    innerhtml += buildInputRowSpecificWand();
    table.innerHTML = innerhtml;

    function buildInputRowSpecificWand() {
        let mistaker = "<td> <input type='text' id='addMistaker' name='mistaker' required> </td><td></td>";
        let submit = "<td> <input type='button' name='button' Value='ADD' onclick='globalAddNewMistaker()'> </td>";
        return "<tr id='addRow'>" + mistaker + submit + "</tr>";
    }
}

function buildRowSpecificWand(mistaker, stricheCount) {
    let dataPart = "<td>" + mistaker + "</td> <td>" + buildCakeString(stricheCount) + "</td>";
    mistaker = '"' + mistaker + '"';
    let updateButton = "<button type='button' name='update' onclick='globalAddStrich(" + mistaker + ")'>ADD</button> ";
    let deleteButton = "<button type='button' name='delete' onclick='globaleDeleteStrich(" + mistaker + ")'>DEL</button> "
    let buttonPart = "<td>" + updateButton + deleteButton + "</td>";
    return "<tr>" + dataPart + buttonPart + "</tr>"

    function buildCakeString(stricheCount) {
        let dataPart = "";
        for (let i = 0; i < Math.trunc(stricheCount / 5); i++) {
            dataPart = dataPart + "<img src='./cakes/bigcake.svg' alt='big Cake' height=50>";
        }
        for (let i = 0; i < stricheCount % 5; i++) {
            dataPart = dataPart + "<img src='./cakes/shortcake.svg' alt='' height=40>";
        }
        return dataPart;
    }
}

let table = document.getElementById("genusswand");

window.globalAddStrich = (mistaker) => {
    addStrich(mistaker)
}

window.globalAddNewMistaker = () => {
    let mistaker = document.getElementById("addMistaker").value;
    if (mistaker !== undefined && mistaker !== "") {
        addStrich(mistaker)
    }
}

window.globaleDeleteStrich = (mistaker) => {
    deleteStrich(mistaker)
}

window.globalFetchSpecificGenusswand = (uuid, name) => {
    fetchGenusswand(uuid, name)
}

window.globalAddGenusswand = () => {
    let name = document.getElementById("addGenusswand").value;
    if (name !== undefined && name !== "") {
        addGenusswand(name)
    }
}

fetchGenusswandOverview()