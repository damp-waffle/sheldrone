import os
from dotenv import load_dotenv
import discord
from discord import HTTPException, app_commands
import scraper, display, constants
from scraper import load_tokens
from scraper import queue_download
from scraper import queue_batch_download

load_dotenv()
GUILD = discord.Object(id=int(os.getenv('TEST_GUILD')))

class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        # self.tree.clear_commands(guild=None)
        await self.tree.sync()
        # self.tree.clear_commands(guild=GUILD)
        # await self.tree.sync(guild=GUILD)

TOKEN = os.getenv('DTOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
client = BotClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_interaction(itc: discord.Interaction):
    """The meat of this bot's functionality. Handles all button clicks, even from timed out views, so long as the bot is running."""
    cid = itc.data.get("custom_id")
    if cid:
        cid = cid.split(":")
        if cid[0]=="btn":
            await itc.response.defer(ephemeral=True)
            e = {'title':'Queuing for download...','description':f"# {constants.loadinganimation}"}
            e = discord.Embed.from_dict(e)
            msg = await itc.followup.send(embed=e, ephemeral=True)
            if cid[1]=="replay":
                tokens = await load_tokens(itc.user.id)
                if tokens:
                    result = await queue_download(tokens, cid[2])
                    if result:
                        if result["userErrors"]==None:
                            e = {'title':'Download Scheduled','description':'Downloaded battle replays can be viewed at the lobby terminal.'}
                            e = discord.Embed.from_dict(e)
                            await itc.followup.edit_message(message_id=msg.id, embed=e)
                        else:
                            e = {'title':'Error','description':'An unknown error occurred.'}
                            e = discord.Embed.from_dict(e)
                            await itc.followup.edit_message(message_id=msg.id, embed=e)
                    else:
                        e = {'title':'Error','description':'An unknown error occurred.'}
                        e = discord.Embed.from_dict(e)
                        await itc.followup.edit_message(message_id=msg.id, embed=e)
                else:
                    e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
                    e = discord.Embed.from_dict(e)
                    await itc.followup.edit_message(message_id=msg.id, embed=e)
            elif cid[1]=="batch":
                tokens = await load_tokens(itc.user.id)
                if tokens:
                    batch = await itc.message.attachments[0].read()
                    ids = scraper.read_batch_bin(batch)
                    result = await queue_batch_download(tokens, ids)
                    if result:
                        e = {'title':f'{result}/{len(ids)} replays queued','description':'Downloaded battle replays can be viewed at the lobby terminal.'}
                        e = discord.Embed.from_dict(e)
                        await itc.followup.edit_message(message_id=msg.id, embed=e)
                else:
                    e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
                    e = discord.Embed.from_dict(e)
                    await itc.followup.edit_message(message_id=msg.id, embed=e)


@client.tree.command()
async def help(interaction: discord.Interaction):
    """Lists command info"""
    e1 = discord.Embed.from_dict(constants.helpText1)
    e2 = discord.Embed.from_dict(constants.helpText2)
    e3 = discord.Embed.from_dict(constants.helpText3)
    await interaction.response.send_message(embeds=[e1,e2,e3], ephemeral=True)

@client.tree.command()
@app_commands.describe(replay_code='The replay code. Like what else would it be dude.')
async def getreplay(interaction: discord.Interaction, replay_code: str):
    """Loads replay data from a provided replay code."""
    await interaction.response.defer()
    tokens = await scraper.load_tokens(interaction.user.id)
    if tokens:
        replay = await scraper.get_replay(tokens, replay_code)
        if replay=="invalid replay code format":
            await interaction.followup.send(content="Invalid replay code format")
        elif replay:
            a = await scraper.get_cosmetic_user_info(tokens)
            try:
                e = discord.Embed.from_dict(display.genEmbed(replay["replay"], a))
                v = display.QueueDownload(replay_id=replay["replay"]["id"], url=replay["replay"]["replayCode"])
                await interaction.followup.send(embed=e, view=v, wait=True)
            except:
                e = {'title':'Error','description':'Invalid Replay Code.'}
                e = discord.Embed.from_dict(e)
                await interaction.followup.send(embed=e)
        else:
            e = {'title':'Error','description':'An unknown error occurred.'}
            e = discord.Embed.from_dict(e)
            await interaction.followup.send(embed=e)
    else:
        e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e)

@client.tree.command()
@app_commands.describe(replay_codes='Up to 30 different replay codes, each separated by spaces. OPTION: If the first value has quotation marks("") surrounding it, it is input as a title.')
async def getbatch(interaction: discord.Interaction, *, replay_codes: str):
    """Loads and creates a batch of replays from the given Replay Codes. Maximum is 30."""
    title=None
    if replay_codes[0]=='"':
        ind = replay_codes.rfind('"')
        title = replay_codes[1:ind]
        replay_codes = replay_codes[ind+2:]
    replay_codes = replay_codes.split()
    if(len(replay_codes) < 31):
        await interaction.response.defer()
        tokens = await scraper.load_tokens(interaction.user.id)
        replays = list()
        ids = list()
        failures = 0
        if tokens:
            for code in replay_codes:
                replay = await scraper.get_replay(tokens, code)
                if replay=="invalid replay code format":
                    replay = {'historyDetail':{'judgement':'----', 'knockout':'NEITHER','vsRule':{'id':'?='},'vsStage':{'name':'Invalid Replay Code Format'}}, 'replayCode':scraper.replay_code(code)}
                    replays.append(replay)
                    ids.append('--------')
                    failures = failures + 1
                elif replay['replay']:
                    replays.append(replay['replay'])
                    ids.append(replay['replay']['id'])
                else:
                    replay = {'historyDetail':{'judgement':'----', 'knockout':'NEITHER','vsRule':{'id':'?='},'vsStage':{'name':'Replay Code Invalid'}}, 'replayCode':scraper.replay_code(code)}
                    replays.append(replay)
                    ids.append('--------')
                    failures = failures + 1
            if failures == len(replays):
                e = {'title':'Error','description':'All provided replay codes were invalid.'}
                e = discord.Embed.from_dict(e)
                await interaction.followup.send(embed=e)
                return
            a = await scraper.get_cosmetic_user_info(tokens)
            e = display.genBatch(replays, a, title, opt=1)
            v = display.Batch(ids)
            b = scraper.create_batch_bin(ids)
            sfx = v.children[0].custom_id.split(':')[2]
            f = open(f'batch-{sfx}', 'bw+')
            f.write(b)
            f.seek(0)
            file = discord.File(f, f'batch-{sfx}')
            if len(e) > 1:
                try:
                    await interaction.followup.send(embeds=e, view=v, file=file)
                except:
                    e = {'title':'Error','description':'An unknown error occurred.'}
                    e = discord.Embed.from_dict(e)
                    await interaction.followup.send(embed=e)
            else:
                await interaction.followup.send(embed=e[0], view=v, file=file)
            f.close()
            if os.path.exists(f'batch-{sfx}'):
                os.remove(f'batch-{sfx}')
    else:
        e = {'title':'Error','description':'Only up to 30 replays per batch.'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e)

@client.tree.command()
@app_commands.describe(number="OPTIONAL. The number of replays to grab, always grabs the most recent ones first.")
async def getrecentreplays(interaction: discord.Interaction, number: int=30):
    """Loads data from the 30 most recently uploaded replays available in Splatnet. A number to fetch can be specified"""
    if number:
        if number > 30:
            e = {'title':'Error','description':'Only up to 30 replays can be loaded.'}
            e = discord.Embed.from_dict(e)
            await interaction.followup.send(embed=e)
            return
    await interaction.response.defer()
    tokens = await scraper.load_tokens(interaction.user.id)
    if tokens:
        replays = await scraper.get_replay_history(tokens)
        if replays:
            if len(replays) < number:
                number = len(replays)
            ids=list()
            try:
                for r in range(number):
                    ids.append(replays[r]['id'])
                a = await scraper.get_cosmetic_user_info(tokens)
                e = display.genBatch(replays, a, count=number)
                v = display.Batch(ids)
                b = scraper.create_batch_bin(ids)
                sfx = v.children[0].custom_id.split(':')[2]
                f = open(f'batch-{sfx}', 'bw+')
                f.write(b)
                f.seek(0)
                file = discord.File(f, f'batch-{sfx}')
                if len(e) > 1:
                    try:
                        await interaction.followup.send(embeds=e, view=v, file=file)
                    except HTTPException as response:
                        if response.code==50035:
                            e = {'title':'Error','description':'Replay Batch Embed too large. Try requesting a smaller number of replays, remember the default number requested is 30.'}
                            e = discord.Embed.from_dict(e)
                            await interaction.followup.send(embed=e)
                else:
                    await interaction.followup.send(embed=e[0], view=v, file=file)
                f.close()
                if os.path.exists(f'batch-{sfx}'):
                    os.remove(f'batch-{sfx}')
            except:
                e = {'title':'Error','description':'Something went wrong.'}
                e = discord.Embed.from_dict(e)
                await interaction.followup.send(embed=e)
    else:
        e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e)

@client.tree.command()
@app_commands.describe(number="OPTIONAL. The number of photos to grab, always grabs the most recent ones first.")
async def getalbum(interaction: discord.Interaction, number: int | None = None):
    """Loads and sends the photos available in the user's Splatnet3 album."""
    await interaction.response.defer()
    tokens = await scraper.load_tokens(interaction.user.id)
    if tokens:
        album = await scraper.get_album(tokens)
        if album:
            author = await scraper.get_cosmetic_user_info(tokens)
            embeds = display.genAlbum(album, author, number)
            print(embeds)
            for e in embeds:
                await interaction.followup.send(embeds=e)
        else:
            e = {'title':'Error','description':'An unknown error occurred.'}
            e = discord.Embed.from_dict(e)
            await interaction.followup.send(embed=e)
    else:
        e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e)

@client.tree.command()
async def register(interaction: discord.Interaction):
    """Registers a user's Discord UID and session token to SplReplayBot's database."""
    await interaction.response.defer(ephemeral=True)
    if(await load_tokens(interaction.user.id, 1)):
        e = {'title':'User already registered.','description':'If you need to refresh your session token, use the ``/newtoken`` command.'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(content="User already registered. If you need to refresh your session token, use the ``/newtoken`` command.", ephemeral=True)
    else:
        await interaction.followup.send(content=constants.auth_token_disclaimer, ephemeral=True, view=display.Confirm())

@client.tree.command()
async def newtoken(interaction: discord.Interaction):
    """Updates a user's session token in SplReplayBot's database. Uses the same flow as /register, except skipping the disclaimer message and a few other steps."""
    await interaction.response.defer(ephemeral=True)
    if(await load_tokens(interaction.user.id, 1)):
        e = {'title':'Updating Session Token','description':'Would you like to **automatically generate** or **manually input** your *new* session token?'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e, ephemeral=True, view=display.ChooseMethod())
    else:
        e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e,ephemeral=True)

@client.tree.command()
async def tokenstatus(interaction: discord.Interaction):
    """Displays info about the user's tokens, ephemerally and without actually giving token values for privacy reasons. Info includes token validity and creation time. 
    Does NOT attempt to perform token regeneration, only displays status information and recommends regeneration."""
    await interaction.response.defer(ephemeral=True)
    if(await load_tokens(interaction.user.id, 1)):
        e = await display.genStatus(interaction.user.id)
        await interaction.followup.send(embed=e,ephemeral=True)
    else:
        e = {'title':'Unregistered User','description':'You have not been registered with this bot yet. Run ``/register`` for more info!'}
        e = discord.Embed.from_dict(e)
        await interaction.followup.send(embed=e,ephemeral=True)

client.run(TOKEN)