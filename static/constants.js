const REQUEST_URL = location.protocol + '//' + location.host,
    USER_TOKEN_URL = "/token",
    USER_URL = "/user",
    USER_CREATE_USER = USER_URL + "/create",
    USER_GET_USER_INFORMATION = USER_CREATE_USER + "/me",
    TOKEN_EXPIRE_HOURS = 10,
    USER_INFO_URL = USER_URL+"/me",
    GENUSSWAND_URL = "/genusswand",
    GENUSSWAND_CREATE_NEW_GENUSSWAND = GENUSSWAND_URL + "/create/genusswand",
    GENUSSWAND_CREATE_NEW_STRICH_V1 = GENUSSWAND_URL + "/create/strich_v1",
    GENUSSWAND_CREATE_NEW_STRICH_V2 = GENUSSWAND_URL + "/create/strich_v2",
    GENUSSWAND_DELETE_STRICH_V1 = GENUSSWAND_URL + "/delete/strich_v1",
    GENUSSWAND_DELETE_STRICH_V2 = GENUSSWAND_URL + "/delete/strich_v2",
    GENUSSWAND_GET_USER_WAENDE = GENUSSWAND_URL + "/get/genusswaende",
    GENUSSWAND_GET_SPECIFIC_WAND = GENUSSWAND_URL + "/get/genusswand/"

const HTTP_STATUS_OK = 200,
HTTP_STATUS_CREATED = 201,
HTTP_METHOD_POST = "POST",
HTTP_METHOD_PUT = "PUT",
HTTP_METHOD_GET = "GET",
HTTP_METHOD_DELETE = "DELETE";

const HTTP_JSON_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};

const HTTP_JSON_HEADERS_WITH_AUTH = auth_token => {
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    };
};

const HTTP_AUTH_HEADERS = auth_token => {
    return {
        'Authorization': 'Bearer ' + auth_token
    };
}

export {
    REQUEST_URL,
    USER_TOKEN_URL,
    TOKEN_EXPIRE_HOURS,
    USER_INFO_URL,
    USER_CREATE_USER,
    USER_GET_USER_INFORMATION,
    GENUSSWAND_CREATE_NEW_GENUSSWAND,
    GENUSSWAND_CREATE_NEW_STRICH_V1,
    GENUSSWAND_CREATE_NEW_STRICH_V2,
    GENUSSWAND_DELETE_STRICH_V1,
    GENUSSWAND_DELETE_STRICH_V2,
    GENUSSWAND_GET_USER_WAENDE,
    GENUSSWAND_GET_SPECIFIC_WAND,
    HTTP_STATUS_OK,
    HTTP_STATUS_CREATED,
    HTTP_METHOD_GET,
    HTTP_METHOD_POST,
    HTTP_METHOD_PUT,
    HTTP_METHOD_DELETE,
    HTTP_JSON_HEADERS,
    HTTP_JSON_HEADERS_WITH_AUTH,
    HTTP_AUTH_HEADERS
}