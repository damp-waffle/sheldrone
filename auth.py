import os
import base64, hashlib, urllib
import requests
import aiohttp
import request_parts
from constants import SPLATNET_VERSION
from typing import Any

version = SPLATNET_VERSION

def generate_login_url():
    """Generates a url used to log in to a user's Nintendo Account. The first step of the session token generation process."""
    state = base64.urlsafe_b64encode(os.urandom(36))
    verifier = base64.urlsafe_b64encode(os.urandom(32)).replace(b"=", b"")
    hash_ = hashlib.sha256()
    hash_.update(verifier)
    challenge = base64.urlsafe_b64encode(hash_.digest()).replace(b"=", b"")
    body = request_parts.LOGIN_URLENCODE
    body["state"] = state
    body["session_token_code_challenge"] = challenge
    return f"https://accounts.nintendo.com/connect/1.0.0/authorize?{urllib.parse.urlencode(body)}", verifier

def get_session_token(uri, verifier):
    """Gets the session token by using the uri from the login page, which contains a session token code. The session token code combined with the verifier generated during creation of the login url is used to fetch the session token."""
    session = requests.session()
    session_token_code = uri.split("&")[0][uri.find("=")+1:]
    head = request_parts.SESSION_TOKEN_HEAD
    body = request_parts.SESSION_TOKEN_BODY
    head["User-Agent"] = f"OnlineLounge/{version} NASDKAPI Android"
    body["session_token_code"] = session_token_code
    body["session_token_code_verifier"] = verifier
    response = session.post(url="https://accounts.nintendo.com/connect/1.0.0/api/session_token", headers=head, data=body)
    response = response.json()
    return response["session_token"]

async def get_user_access_token(session_token):
    """Step 1 of the g token generation process. Using the session token, the id token and user info access token are obtained."""
    head = request_parts.USER_ACCESS_TOKEN_HEAD
    body = request_parts.USER_ACCESS_TOKEN_BODY
    body["session_token"] = session_token
    session = aiohttp.ClientSession()
    response = await session.post(url="https://accounts.nintendo.com/connect/1.0.0/api/token", headers=head, json=body)
    response = await response.json()
    id_token = response["id_token"]
    access_token = response["access_token"]
    await session.close()
    return {"id_token":id_token, "access_token":access_token}

async def get_user_info(access_token):
    """Step 2 of the g token generation process. Using user info access token obtained in the previous step, the user's Nintendo Account id, language, birthday, and country are obtained. Their nickname and icon are also obtained specifically for the /tokenstatus function of the bot, not for the g token generation process."""
    head = request_parts.USER_INFO_HEAD
    head["Authorization"] = f"Bearer {access_token}"
    session = aiohttp.ClientSession()
    response = await session.get(url="https://api.accounts.nintendo.com/2.0.0/users/me", headers=head)
    response = await response.json()
    user_info = {
        "nickname": response["nickname"],
        "icon": response["iconUri"],
        "na_id": response["id"],
        "lang": response["language"],
        "bday": response["birthday"],
        "natl": response["country"]
        }
    await session.close()
    return user_info

async def get_user_lang(session_token):
    """Similar to get_user_info(), this function just returns the user's language using their session token. A helper function for some scraper queries, as they require the user language and I felt weird hardcoding that..."""
    guat = await get_user_access_token(session_token)
    access_token = guat["access_token"]
    head = request_parts.USER_INFO_HEAD
    head["Authorization"] = f"Bearer {access_token}"
    session = aiohttp.ClientSession()
    response = await session.get(url="https://api.accounts.nintendo.com/2.0.0/users/me", headers=head)
    response = await response.json()
    await session.close()
    return response["language"]

async def get_f_step_1(id_token, na_id):
    """Step 3 of the g token generation process. Using the id token acquired in step 1 and the account id acquired in step 2, the f token is obtained."""
    head = request_parts.F_HEAD
    body = request_parts.F_BODY
    head["X-znca-Version"] = version
    head["X-znca-Client-Version"] = version
    body["token"] = id_token
    body["na_id"] = na_id
    session = aiohttp.ClientSession()
    response = await session.post(url="https://nxapi-znca-api.fancy.org.uk/api/znca/f", headers=head, json=body)
    response = await response.json()
    await session.close()
    return response

async def get_web_coral(f_token, id_token, user_info):
    """Step 4 of the g token generation process. Using the f token acquired in step 3, the id token acquired in step 1, and the user account info acquired in step 2, the web service access credential and coral id are obtained."""
    head = request_parts.WEB_SERVICE_HEAD
    body = request_parts.WEB_SERVICE_BODY
    head["X-ProductVersion"] = version
    head["Content-Length"] = str(990 + len(f_token["f"]))
    head["User-Agent"] = f"com.nintendo.znca/{version}(Android/14)"
    body["parameter"] = {
        "f": f_token["f"],
        "language": user_info["lang"],
        "naBirthday": user_info["bday"],
        "naCountry": user_info["natl"],
        "naIdToken": id_token,
        "requestId": f_token["request_id"],
        "timestamp": f_token["timestamp"]
    }
    session = requests.session()
    response = session.post(url="https://api-lp1.znc.srv.nintendo.net/v3/Account/Login", headers=head, json=body)
    response = response.json()
    wsat = response["result"]["webApiServerCredential"]["accessToken"]
    coral_id = str(response["result"]["user"]["id"])
    return {"webserv_access_token": wsat, "coral_id": coral_id}

async def get_f_step_2(na_id, web_service_access_token, coral_id):
    """Step 5 of the g token generation process. Using the web service access token and coral id acquired in the previous step and the Nintendo Account ID acquired in step 2, the second stage of the f token is obtained. The nxapi-znca-api is very inconsistent with this second step, with only about a 34% success rate, so the function attempts to obtain it up to 10 times before quitting."""
    head = request_parts.F_HEAD
    body = request_parts.F_BODY
    head["X-znca-Version"] = version
    head["X-znca-Client-Version"] = version
    body["token"] = web_service_access_token
    body["hash_method"] = "2"
    body["na_id"] = na_id
    body["coral_user_id"] = coral_id
    session = aiohttp.ClientSession()
    for i in range(10):
            response = await session.post(url="https://nxapi-znca-api.fancy.org.uk/api/znca/f", headers=head, json=body)
            response = await response.json()
            if "f" in response:
                    break
    await session.close()
    return response

async def get_gtoken_final(f_token, web_service_access_token):
    """The 6th and final step of the g token generation process (thank god!). Using the second stage f token, the web service access token, and the coral id, the g token is obtained."""
    head = request_parts.G_TOKEN_HEAD
    body = request_parts.G_TOKEN_BODY
    head["X-ProductVersion"] = version
    head["User-Agent"] = f"com.nintendo.znca/{version}(Android/14)"
    head["Authorization"] = f"Bearer {web_service_access_token}"
    body["parameter"]["f"] = f_token["f"]
    body["parameter"]["registrationToken"] = web_service_access_token
    body["parameter"]["requestId"] = f_token["request_id"]
    body["parameter"]["timestamp"] = f_token["timestamp"]
    session = requests.session()
    response = session.post(url="https://api-lp1.znc.srv.nintendo.net/v2/Game/GetWebServiceToken", headers=head, json=body)
    response = response.json()
    return response["result"]["accessToken"]

async def get_gtoken(session_token):
    """All steps of the g token generation process in one function!"""
    user_access = await get_user_access_token(session_token)
    user_info = await get_user_info(user_access["access_token"])
    f1 = await get_f_step_1(user_access["id_token"], user_info["na_id"])
    web_coral = await get_web_coral(f1, user_access["id_token"], user_info)
    f2 = await get_f_step_2(user_info["na_id"], web_coral["webserv_access_token"], web_coral["coral_id"])
    gtoken = await get_gtoken_final(f2, web_coral["webserv_access_token"])
    return {"gtoken": gtoken, "user_info": user_info}

def get_bullet_token(g_token, user_info: dict[str, str] | None=None, session_token: str | None=None):
    """Obtains the user's bullet token using their g token and user info."""
    # TODO: make it so that the token can be generated without user info by providing the user's session token to obtain it.
    head = request_parts.BULLET_TOKEN_HEAD
    body = request_parts.BULLET_TOKEN_COOKIES
    head["Accept-Language"] = user_info["lang"]
    head["X-Web-View-Ver"] = version
    head["X-NACOUNTRY"] = user_info["natl"]
    body["_gtoken"] = g_token
    session = requests.session()
    response = session.post(url="https://api.lp1.av5ja.srv.nintendo.net/api/bullet_tokens", headers=head, cookies=body)
    response = response.json()
    return response["bulletToken"]