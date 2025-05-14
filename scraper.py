import requests, json, mysql.connector, os
from dotenv import load_dotenv
from typing import Any
import auth, constants, request_parts
import time

version = constants.SPLATNET_VERSION

async def login(uri: str, verifier:str, uid: str):
    """Generates a session token based on the given Nintendo Online URI."""
    try:
        SESSION_TOKEN = auth.get_session_token(uri, verifier) 
        print("session token successfully generated: ")
        print(SESSION_TOKEN)
        await insert_tokens(uid=uid, session_token={"value": SESSION_TOKEN, "timestamp": time.time()})
        return "Successfully added user and token to database!"
    except:
        return "An error occurred."

async def insert_tokens(uid: str, db: mysql.connector.MySQLConnection | None=None, session_token: dict[str, Any] | None=None, gtoken: dict[str, Any] | None=None, bullet_token: dict[str, Any] | None=None):
    """Given any of the three tokens used for Splatnet authentication, updates a user's tokens based on the given Discord UID."""
    WHERE = f"WHERE uid = '{uid}'"
    if not db:
        load_dotenv()
        db = mysql.connector.connect(
        host=os.getenv('SERVER_NAME'),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME')
        )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tokens WHERE uid = {uid}")
    result = cursor.fetchall()
    if len(result):
        if session_token:
            cursor.execute(f"UPDATE tokens SET st_val = '{session_token["value"]}', st_ts = {session_token["timestamp"]} {WHERE};")
            db.commit()
        if gtoken:
            cursor.execute(f"UPDATE tokens SET gt_val = '{gtoken["value"]}', gt_ts = {gtoken["timestamp"]} {WHERE};")
            db.commit()
        if bullet_token:
            cursor.execute(f"UPDATE tokens SET bt_val = '{bullet_token["value"]}', bt_ts = {bullet_token["timestamp"]} {WHERE};")
            db.commit()
    else:
        cursor.execute(f"INSERT INTO tokens (uid, st_val, st_ts) VALUES ('{uid}','{session_token["value"]}',{session_token["timestamp"]});")
        db.commit()
        print(f"Registered user {uid}")
    cursor.close()

async def load_tokens(uid: str, opt=0) -> dict[str, Any] | None:
    """Given a Discord User ID, returns a dict of the 3 tokens belonging to said user."""
    load_dotenv()
    db = mysql.connector.connect(
    host=os.getenv('SERVER_NAME'),
    user=os.getenv('USER_NAME'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DB_NAME')
    )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tokens WHERE uid = {uid}")
    result = cursor.fetchall()
    if result:
        tokens = {
            "session_token": {
                "value": result[0][1],
                "timestamp": result[0][2]
            }
        }
        if result[0][3]:
            tokens["gtoken"] = {
                "value": result[0][3],
                "timestamp": result[0][4]
            }
        if result[0][5]:
            tokens["bullet_token"] = {
                "value": result[0][5],
                "timestamp": result[0][6]
            }
        if opt==0:
            stoken = tokens["session_token"]["value"]
            lang = await auth.get_user_lang(stoken)
            if prefetch_checks(tokens["gtoken"]["value"], tokens["bullet_token"]["value"], lang):
                g = await auth.get_gtoken(tokens["session_token"]["value"])
                # print(g)
                gtoken = g["gtoken"]
                user_info = g["user_info"]
                if prefetch_checks(gtoken, tokens["bullet_token"]["value"], lang):
                    bullet_token = {"value": auth.get_bullet_token(gtoken, user_info), "timestamp": time.time()}
                gtoken_ = {"value": gtoken, "timestamp": time.time()}
                await insert_tokens(uid, db, gtoken=gtoken_, bullet_token=bullet_token)
        db.close()
        return tokens
    else:
        return None

def prefetch_checks(g: str, b: str, lang: str = "en-US") -> bool:
        """Executes a simple query to the Splatnet API in order to verify that the g and bullet tokens are valid. Returns FALSE if the query is successful, returns TRUE if the query fails."""
        head = request_parts.GRAPHQL_HEAD
        head["Authorization"] = f"Bearer {b}"
        head["Accept-Language"] = lang
        head["X-Web-View-Ver"] = version
        head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={lang[:-2]}&na_lang={lang}"
        graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["HomeQuery"],"version": 1}},"variables":{"naCountry":lang[:-2]}}
        test = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
        return test.status_code!=200

async def get_replay(tokens: dict[str, Any], code: str):
    """Executes a query using a user's given tokens and a replay code and returns a dict consisting of replay data."""
    if len(code)!=16:
        code=replay_code(code)
        if code=="INVALID":
            return "invalid replay code format"
    g = tokens["gtoken"]["value"]
    b = tokens["bullet_token"]["value"]
    lang = await auth.get_user_lang(tokens["session_token"]["value"])
    country = lang[:-2]
    head = request_parts.GRAPHQL_HEAD
    head["Authorization"] = f"Bearer {b}"
    head["Accept-Language"] = lang
    head["X-Web-View-Ver"] = version
    head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={country}&na_lang={lang}"
    graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["DownloadSearchReplayQuery"],"version": 1}},"variables": { "code": code }}
    query = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
    if query.status_code == 200:
        response = json.loads(query.text)
        return response["data"]
    else:
        print(f'Error: {query.status_code}')
        print(query.headers)
        print(query.text)

async def get_replay_history(tokens: dict[str, Any]):
    """Executes multiple queries using a user's given tokens and a replay code and returns a dict consisting of data from multiple replays."""
    g = tokens["gtoken"]["value"]
    b = tokens["bullet_token"]["value"]
    lang = await auth.get_user_lang(tokens["session_token"]["value"])
    head = request_parts.GRAPHQL_HEAD
    head["Authorization"] = f"Bearer {b}"
    head["Accept-Language"] = lang
    head["X-Web-View-Ver"] = version
    head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={lang[:-2]}&na_lang={lang}"
    graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["ReplayQuery"],"version": 1}},"variables":{"naCountry":lang[:-2]}}
    query = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
    if query.status_code == 200:
        response = json.loads(query.text)
        return response['data']['replays']['nodes']
    else:
        print(f'Error: {query.status_code}')
        print(query.headers)

async def queue_download(tokens: dict[str, Any], replay_id: str):
    """Executes a query that queues a replay to be downloaded from the lobby terminal in-game from a given replay ID (only accessible by scraping replay data)."""
    g = tokens["gtoken"]["value"]
    b = tokens["bullet_token"]["value"]
    lang = await auth.get_user_lang(tokens["session_token"]["value"])
    head = request_parts.GRAPHQL_HEAD
    head["Authorization"] = f"Bearer {b}"
    head["Accept-Language"] = lang
    head["X-Web-View-Ver"] = version
    head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={lang[:-2]}&na_lang={lang}"
    graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["ReplayModalReserveReplayDownloadMutation"],"version": 1}},"variables": { "input": { "id": replay_id } }}
    query = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
    if query.status_code == 200:
        response = json.loads(query.text)
        return response["data"]["reserveReplayDownload"]
    else:
        return query
    
async def queue_batch_download(tokens: dict[str, Any], replay_ids: list[str]):
    """Executes multiple queries that queue all replays passed through via their IDs to be downloaded from the lobby terminal in-game."""
    g = tokens["gtoken"]["value"]
    b = tokens["bullet_token"]["value"]
    lang = await auth.get_user_lang(tokens["session_token"]["value"])
    head = request_parts.GRAPHQL_HEAD
    head["Authorization"] = f"Bearer {b}"
    head["Accept-Language"] = lang
    head["X-Web-View-Ver"] = version
    head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={lang[:-2]}&na_lang={lang}"
    success=0
    for id in replay_ids:
        graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["ReplayModalReserveReplayDownloadMutation"],"version": 1}},"variables": { "input": { "id": id } }}
        query = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
        if query.status_code==200:
            success+=1
    return success

async def get_album(tokens: dict[str, Any]):
    """Executes a query to get and display the photos recently shared to Splatnet. A number of photos to grab can be specified. If there is no number, all available photos are grabbed."""
    g = tokens["gtoken"]["value"]
    b = tokens["bullet_token"]["value"]
    lang = await auth.get_user_lang(tokens["session_token"]["value"])
    country = lang[:-2]
    head = request_parts.GRAPHQL_HEAD
    head["Authorization"] = f"Bearer {b}"
    head["Accept-Language"] = lang
    head["X-Web-View-Ver"] = version
    head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={country}&na_lang={lang}"
    graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["PhotoAlbumQuery"],"version": 1}},"variables":{"naCountry":lang[:-2]}}
    query = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
    if query.status_code == 200:
        response = json.loads(query.text)
        try:
            return response['data']['photoAlbum']['items']['nodes']
        except:
            return None
    else:
        return None
    


async def get_cosmetic_user_info(tokens: dict[str, Any]):
    """Executes a simple query to grab the name and user icon of the user initiating the command. This is to make replay embeds look even prettier."""
    g = tokens["gtoken"]["value"]
    b = tokens["bullet_token"]["value"]
    lang = await auth.get_user_lang(tokens["session_token"]["value"])
    country = lang[:-2]
    head = request_parts.GRAPHQL_HEAD
    head["Authorization"] = f"Bearer {b}"
    head["Accept-Language"] = lang
    head["X-Web-View-Ver"] = version
    head["Referer"] = f"{constants.SPLATNET_URL}?lang={lang}&na_country={country}&na_lang={lang}"
    graphql_body = {"extensions": {"persistedQuery": {"sha256Hash": constants.sha_keys["SettingQuery"],"version": 1}},"variables":{"naCountry":lang[:-2]}}
    query = requests.post(constants.SPLATNET_URL + "/api/graphql", data=json.dumps(graphql_body), headers=head, cookies=dict(_gtoken=g))
    response = json.loads(query.text)
    return (response["data"]["currentPlayer"]["name"], response["data"]["currentPlayer"]["userIcon"]["url"])

def replay_code(code: str) -> str:
    """Formats a given replay code between two formats; XXXX-XXXX-XXXX-XXXX and XXXXXXXXXXXXXXXX, while also correcting commonly typo'd characters. If the replay code is the incorrect length, returns 'INVALID'."""
    code = code.upper()
    trnsl = str.maketrans("IOZ","102") # replay codes CANNOT contain I, O, or Z since they can be easily mistaken for 1, 0, and 2. however, people still mistakingly type them in lol.
    code = code.translate(trnsl)
    if len(code)==19:
        code = code.split('-')
        short = ""
        for portion in code:
            short += portion
        return short
    elif len(code)==16:
        return code[:4] + '-' + code[4:8] + '-' + code[8:12] + '-' + code[12:]
    else:
        return "INVALID"
    
def create_batch_bin(ids: list[str]):
    """Creates a replay batch file to allow queue_batch_download() to have a list of replay IDs to use."""
    batch=bytearray()
    for replayID in ids:
        if replayID != '--------':
            batch.extend(replayID.encode(encoding="ascii"))
            batch.extend(">".encode(encoding="ascii"))
    return batch

def read_batch_bin(batch: bytes):
    """Helper function for queue_batch_download() that parses a binary replay batch file and returns a list of replay IDs to queue."""
    batch = batch.decode(encoding="ascii")
    batch = batch.split(">")
    batch.pop()
    return batch

if __name__ == "__main__":
    code = input("replay code:")
    print(replay_code(code))