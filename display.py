import time, random, string
from datetime import datetime
import discord
import constants
import auth
from scraper import replay_code
from scraper import insert_tokens
from scraper import load_tokens
from scraper import login

def genEmbed(replay, author: tuple[str, str]):
    """Generates a Discord Embed json in order to display replay data prettily."""
    code = replay_code(replay["replayCode"])
    replay = replay["historyDetail"]
    time = datetime.fromisoformat(replay["playedTime"])
    modeSuffix = ""
    if replay['leagueMatch']:
        modeSuffix = f' \u2022 ***{replay['leagueMatch']['leagueMatchEvent']['name']}***'
    if replay['vsMode']['mode']=='BANKARA':
        if replay['vsMode']['id'][-2:]=="Ux":
            modeSuffix = " (Open)"
        elif replay['vsMode']['id'][-2:]=="I=":
            modeSuffix = " (Series)"
    elif replay['vsMode']['mode']=='FEST':
        if replay['vsMode']['id'][-2:]=="Y=":
            modeSuffix = " (Open)"
        elif replay['vsMode']['id'][-2:]=="c=":
            modeSuffix = " (Series)"
    fields=[{'name':'Replay Code:', 'value':f'`{code}`'}]
    result = ""
    if replay["judgement"]=="WIN":
        result='VICTORY'
    elif replay["judgement"]=="LOSE":
        result='DEFEAT'
    if replay['knockout'] !='NEITHER':
        result +=' - KNOCKOUT!'
    for award in replay["awards"]:
        fields.append({'name':' ','value': "**" + constants.medals[award["name"]] + award["name"] + "**",'inline':'True'})
    e = {
        'author':
        {
            'name': author[0],
            'icon_url': author[1]
        },
        'title': f"{replay["player"]["name"]}'s Battle Replay",
        'url': constants.REPLAY_URL + code,
        'description':f'*{time.strftime('%x %I:%M %p')}*\n# {constants.modeMoji[replay['vsMode']['mode']]} {replay['vsMode']['name']}{modeSuffix}\n# {constants.ruleMoji[replay['vsRule']['id'][-2]]} {replay['vsStage']['name']}\n### {result}'
    }
    e['fields'] = fields
    e['color'] = constants.modeColor[replay['vsMode']['mode']]
    e['footer'] = {'text':f'Game Version: {constants.SPLATOON_VERSION}'}
    return e

def genCompactEmbed(replay):
    """The same as genEmbed(), this time for lists of recent replays."""
    code = replay['replayCode']
    if replay['historyDetail']=='INVALID':
        return " "
    replay = replay["historyDetail"]
    if replay['vsRule']['id'][-2]=='?':
        e=f"**{constants.ruleMoji[replay['vsRule']['id'][-2]]} {replay['vsStage']['name']}**"
    else:
        e=f"**{constants.ruleMoji[replay['vsRule']['id'][-2]]} [{replay['vsStage']['name']}]({constants.REPLAY_URL}{replay_code(code)})**"
    return e

def genBatch(replays: list[dict], author: tuple[str, str], title: str | None=None, count: int | None=None, opt=0):
    """The same as genEmbed(), this time for lists of replays, otherwise known as a batch."""
    desc = f"# {author[0]}'s Recent Replay Batch"
    if opt==1:
        desc = ""
    if title:
        desc=f'# {title}'
    e = {
        'author':
        {
            'name': author[0],
            'icon_url': author[1]
        },
        'title':' ',
        'description': desc
    }
    fields = list()
    if count:
        for i in range(count):
            j = replays[i]['historyDetail']['judgement']
            if j == 'LOSE':
                j = 'LOSS'
            if replays[i]['historyDetail']['knockout']!="NEITHER":
                j+=" (KO)"
            fields.append({'name':' ', 'value':genCompactEmbed(replays[i]), 'inline':'True'})
            fields.append({'name':' ', 'value':j, 'inline':'True'})
            fields.append({'name':' ', 'value':f"`{replay_code(replays[i]['replayCode'])}`", 'inline':'True'})  
    else:
        for replay in replays:
            j = replay['historyDetail']['judgement']
            if j == 'LOSE':
                j = 'LOSS'
            if replay['historyDetail']['knockout']!="NEITHER":
                j+=" (KO)"
            fields.append({'name':' ', 'value':genCompactEmbed(replay), 'inline':'True'})
            fields.append({'name':' ', 'value':j, 'inline':'True'})
            fields.append({'name':' ', 'value':f"`{replay_code(replay['replayCode'])}`", 'inline':'True'})
    if len(fields)<25:
        e['fields']=fields
        es = list()
        em = discord.Embed.from_dict(e)
        es.append(em)
        return es
    else:
        es = list()
        e['fields']=fields[:24]
        for i in range(len(fields)//24):
            if len(fields)-((i+1)*24) > 0:
                ee = fields[24*i:24*(i+1)]
                eee = {'title':' '}
                eee['fields']=ee
                es.append(eee)
        for i in range(len(es)):
            es[i] = discord.Embed.from_dict(es[i])
        return es
    
def genAlbum(album: list[dict], author: tuple[str, str], number: int | None=None):
    """Generates an embed for displaying pictures from a user's Splatnet3 album."""
    es = list()
    embeds = list()
    j = 0
    if number:
        album = album[:number]
    for photo in album:
        url = photo['photo']['url']
        e = discord.Embed(title='',description='',url=f'https://join{j}.bot')
        e.set_image(url=url)
        if album.index(photo)==0:
            e.set_author(name=author[0], icon_url=author[1])
        es.append(e)
        if len(es)==4:
            embeds.append(es[:])
            es.clear()
            j += 1
        elif album.index(photo)==len(album)-1:
            embeds.append(es[:])
    return embeds

async def genStatus(uid: str):
    """Generates an embed that displays information about a user's NSO authentication tokens."""
    timestamp = time.time()
    tokens = await load_tokens(uid, 1)
    values=list()
    pfp = ""
    stoken = tokens["session_token"]["value"]
    uat = await auth.get_user_access_token(stoken)
    uat = uat['access_token']
    if (uat):
        values.append("\u2714 Valid") # values[0]
        uinfo = await auth.get_user_info(uat)
        nickname = uinfo['nickname']
        values.append(nickname) # values[1]
        pfp = uinfo["icon"]
        values.append("") # values[2]
    else:
        values.append("\u2716 Invalid") # values[0]
        values.append('???') # values[1]
        values.append("Generate or input a new session token. You can use /newtoken to do this.") # values[2]
    try:
        gt = tokens["gtoken"]
        values.append(f"*Generated <t:{int(gt["timestamp"])}:d><t:{int(gt["timestamp"])}:T>*") # values[3]
        if timestamp-gt["timestamp"] > 7200:
            values.append("\u2716 Expired") # values[4]
            values.append("") # values[5]
            if values[2]=="":
                values[2] = constants.token_rec
        else:
            values.append("\u2714 Valid") # values[4]
            values.append(f"\n*Expires at <t:{int(gt["timestamp"] + 7200)}:d><t:{int(gt["timestamp"] + 7200)}:T>*") # values[5]
    except ValueError:
        values.append("")
        values.append("\u2716 Nonexistant") # values[4]
        values.append("") # values[5]
        if values[2]=="":
            values[2] = constants.token_rec
    try:
        bt = tokens["bullet_token"]
        values.append(f"*Generated <t:{int(bt["timestamp"])}:d><t:{int(bt["timestamp"])}:T>*") # values[6]
        if timestamp-bt["timestamp"] > 1800:
            values.append("\u2716 Expired") # values[7]
            values.append("") # values[8]
            if values[2]=="":
                values[2] = constants.token_rec
        else:
            values.append("\u2714 Valid") # values[7]
            values.append(f"\n*Expires at <t:{int(bt["timestamp"] + 1800 )}:d><t:{int(bt["timestamp"] + 1800)}:T>*") # values[8]
    except ValueError:
        values.append("") # values[6]
        values.append("\u2716 Nonexistant") # values[7]
        values.append("") # values[8]
        if values[2]=="":
            values[2] = constants.token_rec
    if values[2]=="":
            values[2] = "None! All tokens are valid!"
    e = {
        'title': 'Token Status',
        'author': {
            'name': '---',
            'icon_url': pfp
        },
        'description': f'Connected to MyNintendo account with nickname: **{values[1]}**\n',
        'fields':[
            {'name':'','value':''},
            {'name':'Session Token','value':values[0]},
            {'name':'GToken','value':f'{values[4]}{values[5]}','inline':'True'},
            {'name':'','value':values[3],'inline':'True'},
            {'name':'','value':'','inline':'True'},
            {'name':'Bullet Token','value':f'{values[7]}{values[8]}','inline':'True'},
            {'name':'','value':values[6],'inline':'True'},
            {'name':'','value':'','inline':'True'},
            {'name':'','value':''},
            {'name':'','value':''},
            {'name':'Recommendation:','value':values[2]}
        ]
    }
    return discord.Embed.from_dict(e)

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfirmationButton())
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="nxapi Help", url="https://github.com/samuelthomas2774/nxapi-znca-api/blob/docs/docs/end-user-help.md"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="s3s Token Guide", url="https://github.com/frozenpandaman/s3s?tab=readme-ov-file#token-generation-"))
class ConfirmationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.success, label='Continue', emoji='\u2714')
    async def callback(self, interaction: discord.Interaction):
        self.disabled=True
        await interaction.response.defer()
        await interaction.followup.send(content="Would you like to **automatically generate** or **manually input** your session token?", ephemeral=True, view=ChooseMethod())
class ChooseMethod(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(AutoMan(style=discord.ButtonStyle.blurple,type='Auto'))
        self.add_item(AutoMan(style=discord.ButtonStyle.gray,type='Manual'))
    async def on_error(interaction: discord.Interaction, error, item):
        await interaction.response.send_message(content="An error occurred")
class AutoMan(discord.ui.Button):
    def __init__(self, type, style):
        super().__init__(style=style, label=type)
        self.method = type
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        self.view.children[1].disabled=True
        await interaction.response.defer(ephemeral=True)
        if self.method == 'Auto':
            url = await auth.generate_login_url()
            verifier = url[1]
            url= url[0]
            await interaction.followup.send(content=constants.auto_sesh_instr.format(url),view=Auto(url=url), ephemeral=True)
            t_end = time.time() + 3000
            msg = ""
            message = ""
            # print(url)
            state = url[url.find("state=")+6:url.find("&redirect_uri=")]
            # print(f"State to match is {state} with uid {str(interaction.user.id)}")
            while (time.time() < t_end) and (msg!=state):
                time.sleep(0.7)
                message_ = await listener(interaction=interaction)
                if message_!="":
                    message = message_.content
                    i1=message.find("&state=")+7
                    i2=message.find("&session_state=")
                    if i1 > 0 and i2> 0:
                        msg=message[i1:i2]
            if msg==state:
                await message_.delete()
                res = login(uri=message, verifier=verifier, uid=str(interaction.user.id))
                await interaction.followup.send(content=res, ephemeral=True)
        elif self.method == 'Manual':
            self.disabled=True
            self.view.children[0].disabled=True
            await interaction.followup.send(content="Please paste and send your session token below. Your next message will be **deleted** and **replace your current token**. Proceed carefully!", ephemeral=True)
            t_start = time.time()
            t_end = time.time() + 60 * 5
            message = ""
            while (time.time() < t_end) and (message==""):
                time.sleep(0.7)
                message_ = await listener(interaction=interaction)
                if message_.created_at.timestamp() > t_start:
                    message = message_.content
            await message_.delete()
            insert_tokens(uid=str(interaction.user.id),session_token={"value":message, "timestamp":t_start})
            await interaction.followup.send(content=f"Successfully updated session token to: ||{message}||", ephemeral=True)     

class Auto(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label='Open', url=url, style=discord.ButtonStyle.link))
    async def on_error(interaction: discord.Interaction, error, item):
        await interaction.response.send_message(content="An error occurred")

async def listener(interaction: discord.Interaction):
    msg = ""
    async for message in interaction.channel.history(limit=3):
        if message.author.id == interaction.user.id:
            return message
    return msg

class QueueDownload(discord.ui.View):
    def __init__(self, replay_id: str, url: str):
        super().__init__()
        rID=replay_id
        url= constants.REPLAY_URL + replay_code(url)
        self.button = DownloadButton(rID)
        self.add_item(self.button)
        self.add_item(discord.ui.Button(label='Download in Splatnet',url=url,style=discord.ButtonStyle.link))
    async def on_error(interaction: discord.Interaction, error, item):
        await interaction.response.send_message(content="An error occurred")
    async def on_timeout(self):
        item: discord.ui.Button
        for item in self.children:
            if not item.url:
                item.disabled=True
class DownloadButton(discord.ui.Button):
    def __init__(self, replay_id: str):
        super().__init__(style=discord.ButtonStyle.primary, label='Queue Download')
        self.rID = replay_id
        self.custom_id = f"btn:replay:{replay_id}"

class Batch(discord.ui.View):
    def __init__(self, ids: list[str], embeds: list[discord.Embed] | None=None):
        super().__init__()
        self.add_item(QueueBatch(ids))    
class QueueBatch(discord.ui.Button):
    def __init__(self, ids: list[str]):
        super().__init__(style=discord.ButtonStyle.primary, label='Queue Batch Download')
        self.custom_id=f"btn:batch:{str(''.join(random.choices((string.ascii_letters).join(string.digits), k=7)))}"