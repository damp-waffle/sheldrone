"""This file of constants is made to be used programmatically and as a reference because requests are confusing."""

LOGIN_URLENCODE = {
        "state": "",
        "redirect_uri": "npf71b963c1b7b6d119://auth",
        "client_id": "71b963c1b7b6d119",
        "scope": "openid user user.birthday user.mii user.screenName",
        "response_type": "session_token_code",
        "session_token_code_challenge": "",
        "session_token_code_challenge_method": "S256",
        "theme": "login_form",
        }

SESSION_TOKEN_HEAD = {
        "User-Agent": "",
        "Accept-Language":"en-US",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "540",
        "Host": "accounts.nintendo.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
}
SESSION_TOKEN_BODY = {
        "client_id": "71b963c1b7b6d119",
        "session_token_code": "",
        "session_token_code_verifier": ""
}

USER_ACCESS_TOKEN_HEAD = {
        "Host": "accounts.nintendo.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; Pixel 7a Build/UQ1A.240105.004)"
}
USER_ACCESS_TOKEN_BODY = {
        "client_id": "71b963c1b7b6d119",
        "session_token": "",
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer-session-token"
}

USER_INFO_HEAD = {
        "User-Agent": "NASDKAPI; Android",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Host": "api.accounts.nintendo.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Authorization": ""
}

F_HEAD = {
        "User-Agent": "shel-drone/0.1.1 (+https://github.com/damp-waffle/sheldrone)",
        "Content-Type": "application/json; charset=utf-8",
        "X-znca-Platform": "Android",
        "X-znca-Version": "",
        "X-znca-Client-Version": ""
}
F_BODY = {
        "token": "",
        "hash_method": "1",
        "na_id": ""
}

WEB_SERVICE_HEAD = {
        "X-Platform": "Android",
        "X-ProductVersion": "",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": ""
}
WEB_SERVICE_BODY = {
        "parameter": {
            "f": "",
            "language": "",
            "naBirthday": "YYYY-MM-DD",
            "naCountry": "",
            "naIdToken": ""
        }
}

G_TOKEN_HEAD = {
        "X-Platform": "Android",
        "X-ProductVersion": "",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "391",
        "Accept-Encoding": "gzip",
        "User-Agent": ""
}
G_TOKEN_BODY = {
        "parameter": {
                "f": "",
                "id":4834290508791808,
                "registrationToken":"",
                "requestId":"",
                "timestamp":""
        }
}

BULLET_TOKEN_HEAD = {
    "Content-Length": "0",
    "Content-Type": "application/json",
    "Accept-Language": "",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 7a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "X-Web-View_Ver": "",
    "X-NACOUNTRY": "",
    "Accept": "*/*",
    "Origin": "https://api.lp1.av5ja.srv.nintendo.net",
    "X-Requested-With": "com.nintendo.znca"
}
BULLET_TOKEN_COOKIES = {
    "_gtoken": "",
    "_dnt": "1"
}

GRAPHQL_HEAD = {
        "Authorization": "",
        "Accept-Language": "",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 7a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
        "X-Web-View-Ver": "",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://api.lp1.av5ja.srv.nintendo.net",
        "X-Requested-With": "com.nintendo.znca",
        "Referer": "",
        "Accept-Encoding": "gzip, deflate",
}