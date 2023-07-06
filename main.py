from disnake.ext import commands;
import disnake;
from disnake.ui import Button, View;
import youtubesearchpython;
import yt_dlp;
import random
import pyjokes;
import requests;
import datetime;
import bs4;
import asyncio;


class waifu: 
    def get(keyw): 
        return {'neko': 'neko', 'shinobu': 'shinobu', 'megumin': 'megumin', 'bully': 'bullied', 'cuddle': 'cuddled', 'cry': 'cried', 'hug': 'hugged', 'awoo': 'awoo', 'kiss': 'kissed', 'lick': 'licked', 'pat': 'pat', 'smug': 'smugged', 'bonk': 'bonked', 'yeet': 'yeeted', 'blush': 'blushed', 'smile': 'smiled', 'wave': 'waved', 'highfive': 'highfived', 'handhold': 'handhold', 'nom': 'nomed', 'bite': 'bit', 'glomp': 'glomped', 'slap': 'slapped', 'kill': 'killed', 'kick': 'kicked', 'happy': 'happy', 'waifu': 'waifu', 'wink': 'winked', 'poke': 'poke', 'dance': 'danced', 'cringe': 'cringed'}[keyw], requests.get(f"https://api.waifu.pics/sfw/{keyw}").json()["url"]

class ep:
    def get(url) -> list:
        html = requests.get(url).text
        end_point, dependent, independent = [], [".png",".jpg",".wav",".jpeg",".json",".js",".php",".xml"], ["http://","https://","file://","php://","ftp://","./","../","/"]
        for i in [idk.split("\\")[0] for idk in re.split(f"'|\"|,|\*|\n|[|]", html) if idk.split("\\")[0] != ""]:
            if i:
                for de in independent:
                    if i.startswith(de): end_point.append(i)
                for ind in dependent:
                    if i.endswith(ind): end_point.append(f"{url}{i}" if i[0] == "/" else f"{url}/{i}")
        return [f"{url}{idk}" if idk[0] == "/" else idk for idk in [item for item in end_point if item != []]]


prefix: str                             =       "$GAY "

token: str                              =       "ODIzOTgxMjQ0NDk2MzQ3MTY3.GK1Lak.pKIDUCbeuIdeI5WVp4wu5toZYnkCNUDBhbLxFQ"

FFMPEG_OPTIONS: dict                    =       {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

getAllMembers: list                     =       lambda client: list(set(sum([guild.members for guild in client.guilds], [])))

abc: dict                               =       {"music": {}}

intents                                 =       disnake.Intents().all()

client                                  =       commands.Bot(command_prefix=prefix, intents=intents)

youtube: list                           =       lambda keyword: youtubesearchpython.VideosSearch(keyword, limit = 10).result()['result']

spotify_search: list                    =       lambda link: [i for i in ep.get(link) if "/track/" in i]

name: str                               =       lambda link: bs4.BeautifulSoup(requests.get(link.split('?')[0]).text, 'html.parser').title.string.split(" | ")[0]

def yt_search(keyword: str) -> tuple:
    idk, YDL_OPTIONS = youtubesearchpython.VideosSearch(keyword, limit = 10).result()['result'][0], {'format': 'bestaudio/best', 'noplaylist':'True'}
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl: meta:dict = ydl.extract_info(idk["link"], download=False)
    return idk["link"], idk["title"][0:80], meta['url'], idk['thumbnails'][0]['url'].split('?')[0], idk['duration'], idk['viewCount']['short'], idk['descriptionSnippet'][0]['text'][0:2048]

def get(url) -> list:
    html = requests.get(url).text
    end_point, dependent, independent = [], [".png",".jpg",".wav",".jpeg",".json",".js",".php",".xml"], ["http://","https://","file://","php://","ftp://","./","../","/"]
    for i in [idk.split("\\")[0] for idk in re.split(f"'|\"|,|\*|\n|[|]", html) if idk.split("\\")[0] != ""]:
        if i:
            for de in independent:
                if i.startswith(de): end_point.append(i)
            for ind in dependent:
                if i.endswith(ind): end_point.append(f"{url}{i}" if i[0] == "/" else f"{url}/{i}")
    return [f"{url}{idk}" if idk[0] == "/" else idk for idk in [item for item in end_point if item != []]]

def print_board(board):
    formatted_board = ""
    for row in board:
        formatted_board += "-" * 9 + "\n"
        formatted_board += "|".join(row) + "\n"
    return formatted_board

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    await client.change_presence(activity=disnake.Streaming(name="💻VisualStudio Code", url="https://github.com/NacreousDawn596"))

@client.command(name="joke", description="Sends a coding joke")
async def joke(ctx):
    return await ctx.send(f"> {pyjokes.get_joke()}")

@client.command(name="test", description="To test if the bot is still working")
async def test(ctx):
    return await ctx.send("- tested")

@client.command(name="clear", description="To clear messages")
@commands.check_any(commands.is_owner(), commands.has_permissions(manage_channels=True))
async def clear(ctx, number: int):
    return await ctx.channel.purge(limit=int(number) + 1)

@client.command(name="tictactoe", description="just to have fun playing tictactoe with friends :)")
async def tictactoe(ctx, plyr):
    board = [[" ", " ", " "] for _ in range(3)]
    e = ["X", "O"]
    random.shuffle(e)
    players = {e[0]: ctx.author, e[1]: plyr}
    current_player = e[0]
    message = await ctx.send(f"## {players[current_player]}'s turn\n```\n{print_board(board)}\n```\n- play by sending coords, let's take as an example `1.2` for first row second column")
    def check(msg):
        return msg.author == players[current_player] and msg.channel == ctx.channel
    while True:
        try:
            e = await client.wait_for("message", check=check, timeout=60)
            if any([u in e.content for u in ["end", "finish", "leave", "quit"]]):
                return ctx.send("> Exiting...")
            row, col = [int(i) - 1 for i in e.content.split()[-1].split(".")]
            if 0 <= row <= 2 and 0 <= col <= 2:
                if board[row][col] == " ":
                    board[row][col] = current_player
                    winner = check_winner(board)
                    if winner:
                        await message.edit(content=f"```\n{print_board(board)}\n```\n# Player {players[winner]} wins!")
                        break
                    current_player = "O" if current_player == "X" else "X"
                else:
                    await ctx.send("Invalid move. Try again.")
            else:
                await ctx.send("Invalid input. Row and column should be in the range 1..3.")
            await message.edit(f"## {players[current_player]}'s turn\n```\n{print_board(board)}\n```\n- play by sending coords, let's take as an example `1.2` for first row second column")
        except ValueError:
            await ctx.send("Invalid input. Please enter a valid row and column.")
        except asyncio.TimeoutError:
            await ctx.send("> Game timed out. Exiting.")
            break

@client.command(name="urban", description="To get a definition from the urban dictionnary")
async def urban(ctx, times: int, *word):
    for index, definition in enumerate(requests.get(f"https://api.urbandictionary.com/v0/define?term={word}").json()["list"][0:times]):
        try:
            ctx.send(f"- {index}) {definition['definition']}")
        except:
            pass

@client.command(name="run", description = "execute a python code")
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def run(ctx, *, code):
    return await ctx.send(eval(code))

@client.command(name="git", description = "get someone's git infos")
async def git(ctx, user: str):
    data = requests.get(f"https://api.github.com/users/{user}").json()
    embed, button, view = disnake.Embed(title=f"{data['name']}'s profil", url=f"https://github.com/{data['name']}", color=disnake.Color.purple()), Button(label="Github", url=f"https://github.com/{data['name']}", emoji="<:github:879129561084870726>"), View()
    embed.set_image(url=data["avatar_url"])
    for key in ["name", "followers", "following", "bio", "public_repos", "created_at"]:
        embed.add_field(name=f"{key}:", value=data[key], inline=True)
    view.add_item(button)
    return await ctx.send(embed=embed, view=view)

@client.command(name="avatar", description = "get a discord user's pfp")
async def avatar(ctx, user: disnake.Member = None):
    embed = disnake.Embed(color=disnake.Color.teal())
    embed.set_image(user.avatar.url)
    return await ctx.send(embed=embed)

@client.command(name="ping", description = "get the bot latency")
async def ping(ctx):
    await ctx.send(f"> Pong! {int(datetime.datetime.timestamp(datetime.datetime.now()) - datetime.datetime.timestamp(ctx.message.created_at))}ms")

@client.slash_command(name="joke", description="Sends a coding joke")
async def joke(interaction):
    return await interaction.send(f"> {pyjokes.get_joke()}")

@client.slash_command(name="test", description="To test if the bot is still working")
async def test(interaction):
    return await interaction.send("- tested")

@client.slash_command(name="clear", description="To clear messages")
@commands.check_any(commands.is_owner(), commands.has_permissions(manage_channels=True))
async def clear(interaction, number: int):
    return await interaction.channel.purge(limit=int(number) + 1)

@client.slash_command(name="run", description = "execute a python code")
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def run(interaction, *, code):
    await interaction.response.defer()
    return await interaction.followup.send(eval(code))

@client.slash_command(name="git", description = "get someone's git infos")
async def git(interaction, user: str):
    await interaction.response.defer()
    data = requests.get(f"https://api.github.com/users/{user}").json()
    embed, button, view = disnake.Embed(title=f"{data['name']}'s profile", url=f"https://github.com/{data['name']}", color=disnake.Color.purple()), Button(label="Github", url=f"https://github.com/{data['name']}", emoji="<:github:879129561084870726>"), View()
    embed.set_image(url=data["avatar_url"])
    for key in ["name", "followers", "following", "bio", "public_repos", "created_at"]:
        embed.add_field(name=f"{key}:", value=data[key], inline=True)
    view.add_item(button)
    return await interaction.followup.send(embed=embed, view=view)

@client.slash_command(name="urban", description="To get a definition from the urban dictionnary")
async def urban(interaction, word:str, times: int = 3):
    e = []
    for index, definition in enumerate(requests.get(f"https://api.urbandictionary.com/v0/define?term={word}").json()["list"][0:times]):
        try:
            e.append(f"- {index}) {definition['definition']}")
        except:
            pass
    embed = disnake.Embed(title=f"Definition of {word}", description="\n".join(e), color=disnake.Color.teal())
    return await interaction.send(embed=embed)

@client.slash_command(name="avatar", description = "get a discord user's pfp")
async def avatar(interaction, user: disnake.Member = None):
    embed = disnake.Embed(color=disnake.Color.teal())
    embed.set_image(user.avatar.url)
    return await interaction.send(embed=embed)

@client.slash_command(name="cuddle")
async def cuddle(interaction, user: disnake.Member = ""):
    action, link = waifu.get("cuddle")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="cry")
async def cry(interaction, user: disnake.Member = ""):
    action, link = waifu.get("cry")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="hug")
async def hug(interaction, user: disnake.Member = ""):
    action, link = waifu.get("hug")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="pat")
async def pat(interaction, user: disnake.Member = ""):
    action, link = waifu.get("pat")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="blush")
async def blush(interaction, user: disnake.Member = ""):
    action, link = waifu.get("blush")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="smile")
async def smile(interaction, user: disnake.Member = ""):
    action, link = waifu.get("smile")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="wave")
async def wave(interaction, user: disnake.Member = ""):
    action, link = waifu.get("wave")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="bite")
async def bite(interaction, user: disnake.Member = ""):
    action, link = waifu.get("bite")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="slap")
async def slap(interaction, user: disnake.Member = ""):
    action, link = waifu.get("slap")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="kill")
async def kill(interaction, user: disnake.Member = ""):
    action, link = waifu.get("kill")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="kick")
async def kick(interaction, user: disnake.Member = ""):
    action, link = waifu.get("kick")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="happy")
async def happy(interaction, user: disnake.Member = ""):
    action, link = waifu.get("happy")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="wink")
async def wink(interaction, user: disnake.Member = ""):
    action, link = waifu.get("wink")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="dance")
async def dance(interaction, user: disnake.Member = ""):
    action, link = waifu.get("dance")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="cringe")
async def cringe(interaction, user: disnake.Member = ""):
    action, link = waifu.get("cringe")
    embed = disnake.Embed(title=f"{interaction.author} {action} {user}", color=disnake.Color.purple())
    embed.set_image(url=link)
    return await interaction.send(embed=embed)

@client.slash_command(name="play", description="To play music")
async def play(interaction, keyword:str):
    await interaction.response.defer()
    async def lis(interaction, _:str):
        url, name, music, pic, duration, vview, description = yt_search(_)
        resume, pause, skip, urlb = Button(label="resume", style=disnake.ButtonStyle.green), Button(label="pause", style=disnake.ButtonStyle.danger), Button(label="skip", style=disnake.ButtonStyle.primary), Button(label=name, url=url)
        async def resumef(interaction): 
            if interaction.author.voice and interaction.guild.voice_client.is_connected():
                interaction.guild.voice_client.resume()
                await interaction.send("> noice :D")
        async def pausef(interaction): 
            if interaction.author.voice and interaction.guild.voice_client.is_connected() and interaction.guild.voice_client.is_playing():
                interaction.guild.voice_client.pause()
                await interaction.send("> paused!")
        async def skipf(interaction): 
            if interaction.author.voice and interaction.guild.voice_client.is_connected() and interaction.guild.voice_client.is_playing():
                interaction.guild.voice_client.stop()
                await interaction.send("> stopped :/")
        resume.callback, pause.callback, skip.callback, view = resumef, pausef, skipf, View()
        for b in [resume, pause, skip, urlb]:
            view.add_item(b)
        embed = disnake.Embed(title=name, description=f"**{description}**\n{duration}\t|\t{vview}\n", color=disnake.Color.red(), url=url)
        embed.set_image(url=pic)
        await interaction.followup.send(embed=embed, view=view)
        interaction.guild.voice_client.play(await disnake.FFmpegOpusAudio.from_probe(music, **FFMPEG_OPTIONS))
        while interaction.guild.voice_client.is_playing(): 
            await asyncio.sleep(1)
        abc['music'][str(interaction.guild.id)].remove(_)
        if len(abc['music'][str(interaction.guild.id)]) != 0: 
            await lis(interaction, abc['music'][str(interaction.guild.id)][0])
    if not interaction.author.voice: 
        return await interaction.send("> could you please join a voc before playing music?")
    try: 
        x = interaction.guild.voice_client.is_connected()
    except: 
        await interaction.author.voice.channel.connect(); abc['music'][str(interaction.guild.id)] = []
    abc['music'][str(interaction.guild.id)].append(keyword)
    if interaction.guild.voice_client.is_playing(): 
        return await interaction.followup.send("> added to queue!")
    else: 
        return await lis(interaction, keyword)

@client.slash_command(name="join", description="join a vocale channel")
async def join(interaction):
    if interaction.author.voice:
        await interaction.author.voice.channel.connect()
        abc['music'][str(interaction.guild.id)] = []
        return await interaction.send("> joined", ephemeral=True)
    else: 
        return await interaction.send("> join a voc before executing this", ephemeral=True)

@client.slash_command(name="leave", description="leave a vocale channel")
async def leave(interaction):
    if interaction.author.voice and interaction.guild.voice_client.is_connected():
        await interaction.author.voice.channel.disconnect()
        return await interaction.send("> left", ephemeral=True)
    else: 
        return await interaction.send("> join a voc before executing this", ephemeral=True)

@client.slash_command(name="stop", description="stop the current music")
async def stop(interaction):
    if interaction.author.voice and interaction.guild.voice_client.is_connected() and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()
        return await interaction.send("> stopped :/")

@client.slash_command(name="resume", description="resume the stopped music")
async def resume(interaction):
    if interaction.author.voice and interaction.guild.voice_client.is_connected() and interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        return await interaction.reply("> noice :D")

@client.slash_command(name="spotify", description="play a playlist from spotify")
async def spotify(interaction, playlist: str, shuffle: bool = False):
    if interaction.author.voice and interaction.guild.voice_client.is_connected():
        spot_msg, event, songs = await interaction.send("> gimme 1sec"), asyncio.Event(), spotify_search(playlist)
        event.set()
        if not shuffle: random.shuffle(songs)
        spot_msg = await interaction.channel.send("Null")
        for _ in songs:
            await event.wait()
            event.clear()
            url, name, music, pic, duration, vview, description = yt_search(_)
            resume, pause, skip, urlb = Button(label="resume", style=disnake.ButtonStyle.green), Button(label="pause", style=disnake.ButtonStyle.danger), Button(label="skip", style=disnake.ButtonStyle.primary), Button(label=name, url=url)
            async def resumef(interaction): 
                if interaction.author.voice and interaction.guild.voice_client.is_connected():
                    interaction.guild.voice_client.resume()
                    await interaction.send("> noice :D")
            async def pausef(interaction): 
                if interaction.author.voice and interaction.guild.voice_client.is_connected() and interaction.guild.voice_client.is_playing():
                    interaction.guild.voice_client.pause()
                    await interaction.send("> paused!")
            async def skipf(interaction): 
                if interaction.author.voice and interaction.guild.voice_client.is_connected() and interaction.guild.voice_client.is_playing():
                    interaction.guild.voice_client.stop()
                    await interaction.send("> stopped :/")
            resume.callback, pause.callback, skip.callback, view = resumef, pausef, skipf, View()
            for b in [resume, pause, skip, urlb]:
                view.add_item(b)
            embed = disnake.Embed(title=name, description=f"**{description}**\n{duration}\t|\t{vview}\n", color=disnake.Color.red(), url=url)
            embed.set_image(url=pic)
            await interaction.followup.send(embed=embed, view=view)
            interaction.guild.voice_client.play(await disnake.FFmpegOpusAudio.from_probe(music, **FFMPEG_OPTIONS))

client.run("MTEyNjMyODA5NDU0MjgxMTE0Ng.GrZlnr.EYjREaT6DrFYgikho66rn-OLVPzX9Pgy2ZC3SA")
