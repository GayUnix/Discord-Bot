from disnake.ext import commands;
import disnake;
from disnake.ui import Button, View;
import youtubesearchpython;
import yt_dlp;
import datetime;
import random
import pyjokes;
import requests;
import re;
import datetime;
from PIL import Image, ImageDraw, ImageFont;
import io;
import json;
import bs4;
import asyncio;


class waifu: 
    def get(keyw): 
        return {'neko': 'neko', 'shinobu': 'shinobu', 'megumin': 'megumin', 'bully': 'bullied', 'cuddle': 'cuddled', 'cry': 'cried', 'hug': 'hugged', 'awoo': 'awoo', 'kiss': 'kissed', 'lick': 'licked', 'pat': 'pat', 'smug': 'smugged', 'bonk': 'bonked', 'yeet': 'yeeted', 'blush': 'blushed', 'smile': 'smiled', 'wave': 'waved', 'highfive': 'highfived', 'handhold': 'handhold', 'nom': 'nomed', 'bite': 'bit', 'glomp': 'glomped', 'slap': 'slapped', 'kill': 'killed', 'kick': 'kicked', 'happy': 'happy', 'waifu': 'waifu', 'wink': 'winked', 'poke': 'poke', 'dance': 'danced', 'cringe': 'cringed'}[keyw], requests.get(f"https://api.waifu.pics/sfw/{keyw}").json()["url"]

prefix: str                             =       "$GAY "

token: str                              =       "MTEyNjMyODA5NDU0MjgxMTE0Ng.GrZlnr.EYjREaT6DrFYgikho66rn-OLVPzX9Pgy2ZC3SA"

FFMPEG_OPTIONS: dict                    =       {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

abc: dict                               =       {"music": {}}

intents                                 =       disnake.Intents().all()

client                                  =       commands.Bot(command_prefix=prefix, intents=intents)

darkjokes                               =       json.loads(open("darkjokes.json", "r").read())["jokes"]

def distrowatch(distro):
    soup = bs4.BeautifulSoup(requests.get(f"https://distrowatch.com/table.php?distribution={distro}").text, "html.parser")
    titles = soup.find("td", {"class": "TablesTitle"})
    data = {j.find("a").text: j.find("b").text for j in titles.find("ul").find_all("li")}
    return {data[i]: i for i in list(set(data))[::-1]}, titles.text.splitlines()[-3]

def yt_search(keyword: str) -> tuple:
    idk, YDL_OPTIONS = youtubesearchpython.VideosSearch(keyword, limit = 10).result()['result'][0], {'format': 'bestaudio/best', 'noplaylist':'True'}
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl: meta:dict = ydl.extract_info(idk["link"], download=False)
    return idk["link"], idk["title"][0:80], meta['url'], idk['thumbnails'][0]['url'].split('?')[0], idk['duration'], idk['viewCount']['short'], idk['descriptionSnippet'][0]['text'][0:2048]

def apply_circular_mask(image):
    width, height = image.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    result = Image.new('RGBA', (width, height))
    result.paste(image, mask=mask)
    return result

def create_welcome_image(background, profile, text, username):
    background = background.convert('RGBA').resize((int(1280*1), int(800*1)), resample=Image.LANCZOS)
    profile_picture = profile.convert('RGBA')
    profile_picture.thumbnail((profile_picture.width/2, profile_picture.height/2), resample=Image.LANCZOS)
    profile_picture = apply_circular_mask(profile_picture)
    profile_picture = profile_picture.resize((170, 170), Image.LANCZOS)
    x = (background.width - profile_picture.width) // 2
    y = (background.height - profile_picture.height) // 2
    background.paste(profile_picture, (x, y - 70), profile_picture)
    max_username_width = background.width - 20
    username_font_size = 40
    username_font = ImageFont.truetype("./Poppins-Light.ttf", username_font_size)
    max_welcome_width = background.width - 20
    welcome_font_size = 70
    welcome_font = ImageFont.truetype("./Poppins-Bold.ttf", welcome_font_size)
    draw = ImageDraw.Draw(background)
    neg_color = tuple(255 - value for value in background.getpixel((0, 0)))
    welcome_text_width, welcome_text_height = draw.textsize(text, font=welcome_font)
    welcome_text_x = background.width // 2
    welcome_text_y = y + profile_picture.height + 20
    while draw.textsize(text, font=welcome_font)[0] > max_welcome_width:
        welcome_font_size -= 1
        welcome_font = ImageFont.truetype("./Poppins-Bold.ttf", welcome_font_size)
    draw.text((welcome_text_x, welcome_text_y), text, fill=neg_color, font=welcome_font, anchor="mm")
    username_text_x = background.width // 2
    username_text_y = y + profile_picture.height + 120
    while draw.textsize(username, font=username_font)[0] > max_username_width:
        username_font_size -= 1
        username_font = ImageFont.truetype("./Poppins-Light.ttf", min(welcome_font_size - 30, username_font_size))
    draw.text((username_text_x, username_text_y), username, fill=neg_color, font=username_font, anchor="mm")
    return background

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

def I_hate_when_I_am_coding(url) -> list:
    html = requests.get(url).text
    end_point, dependent, independent = [], [".png",".jpg",".wav",".jpeg",".json",".js",".php",".xml"], ["http://","https://","file://","php://","ftp://","./","../","/"]
    for i in [idk.split("\\")[0] for idk in re.split(f"'|\"|,|\*|\n|[|]", html) if idk.split("\\")[0] != ""]:
        if i:
            for de in independent:
                if i.startswith(de): end_point.append(i)
            for ind in dependent:
                if i.endswith(ind): end_point.append(f"{url}{i}" if i[0] == "/" else f"{url}/{i}")
    return [item for item in end_point if item != []]

def e():
    r = random.choice([f for f in I_hate_when_I_am_coding(f"https://programmerhumor.io/page/{str(random.randint(1, 1960))}/") if f.endswith(".jpg") and "icon" not in f])
    return r if requests.get(r).status_code == 200 else e()

def distrowatch(distro):
    soup = bs4.BeautifulSoup(requests.get(f"https://distrowatch.com/table.php?distribution={distro}").text, "html.parser")
    titles = soup.find("td", {"class": "TablesTitle"})
    data = {j.find("a").text: j.find("b").text for j in titles.find("ul").find_all("li")}
    return {data[i]: i for i in list(set(data))[::-1]}, titles.text.splitlines()[-3]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    await client.change_presence(activity=disnake.Streaming(name="💻VisualStudio Code", url="https://github.com/NacreousDawn596"))
    meme_channels = sum([[channel for channel in guild.text_channels if "meme" in channel.name] for guild in client.guilds], [])
    while True:
        memee = e()
        embed = disnake.Embed(title="meme time lol", color=disnake.Color.random())
        embed.set_image(memee)
        newmeme = Button(label="new one! :3", style=disnake.ButtonStyle.green)
        async def newmemef(interaction): 
            await interaction.response.defer()
            memee = e()
            embed = disnake.Embed(title="meme time lol", color=disnake.Color.random())
            embed.set_footer(text=f"requested by {interaction.author.name}")
            embed.set_image(memee)
            newmeme = Button(label="new one! :3", style=disnake.ButtonStyle.green)
            newmeme.callback = newmemef
            view = View()
            view.add_item(newmeme)
            return await interaction.send(embed=embed, view=view)
        newmeme.callback = newmemef
        view = View()
        view.add_item(newmeme)
        for channel in meme_channels:
            await channel.send(embed=embed, view=view)
        await asyncio.sleep(60*60)


@client.command(name="joke", description="Sends a coding joke")
async def joke(ctx):
    return await ctx.send(f"> {pyjokes.get_joke()}")

@client.command(name="darkjoke", description="to get a really darkjoke")
async def darkjoke(ctx):
    data = random.choice(darkjokes)
    embed = disnake.Embed(title="a darkjoke :skull:", description="\u200b", color=disnake.Color.random())
    embed.add_field(name=data["buildup"] + "?", value=data["punchline"], inline=False)
    newdj = Button(label="more >:)", style=disnake.ButtonStyle.green)
    view = View()
    view.add_item(newdj)
    async def darkjokef(interaction): 
        await interaction.response.defer()
        data = random.choice(darkjokes)
        embed = disnake.Embed(title="a darkjoke :skull:", description="\u200b", color=disnake.Color.random())
        embed.add_field(name=data["buildup"] + "?", value=data["punchline"], inline=False)
        view = View()
        newdj = Button(label="more >:)", style=disnake.ButtonStyle.green)
        view.add_item(newdj)
        newdj.callback = darkjokef
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    newdj.callback = darkjokef
    await ctx.send(embed=embed, view=view, ephemeral=True)
    
@client.command(name="distro", description="get distrowatch info")
async def distro(ctx, os):
    data, description = distrowatch(os)
    embed = disnake.Embed(title=f'{os} according to distrowatch', description=description, url=f"https://distrowatch.com/table.php?distribution={os}")
    for i in data:
        embed.add_field(name=i, value=data[i], inline=False)
    view = View()
    redirect = Button(label="See it on distrowatch :)", url=f"https://distrowatch.com/table.php?distribution={os}")
    view.add_item(redirect)
    await ctx.send(embed=embed, view=view)

@client.command(name="meme", description="Sends a coding meme")
async def meme(ctx):
    memee = e()
    embed = disnake.Embed(title="meme time lol", color=disnake.Color.random())
    embed.set_image(memee)
    newmeme = Button(label="new one! :3", style=disnake.ButtonStyle.green)
    async def newmemef(interaction): 
        await interaction.response.defer()
        memee = e()
        embed = disnake.Embed(title="meme time lol", color=disnake.Color.random())
        embed.set_image(memee)
        embed.set_footer(text=f"requested by {interaction.author.name}")
        newmeme = Button(label="new one! :3", style=disnake.ButtonStyle.green)
        newmeme.callback = newmemef
        view = View()
        view.add_item(newmeme)
        embed.set_footer()
        return await interaction.send(embed=embed, view=view)
    newmeme.callback = newmemef
    view = View()
    view.add_item(newmeme)
    return await ctx.send(embed=embed, view=view)

@client.command(name="useless", description="to get some useless fact about something very random")
async def useless(ctx, lang="en"):
    data = requests.get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}').json()
    embed = disnake.Embed(title="Useless Fact lmao", description="**" + data["text"] + "**", color=disnake.Color.random())
    newuseless = Button(label="again ^^", style=disnake.ButtonStyle.green)
    view = View()
    view.add_item(newuseless)
    async def uselessf(interaction): 
        await interaction.response.defer()
        data = requests.get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}').json()
        embed = disnake.Embed(title="Useless Fact lmao", description="**" + data["text"] + "**", color=disnake.Color.random())
        view = View()
        newuseless = Button(label="again ^^", style=disnake.ButtonStyle.green)
        view.add_item(newuseless)
        newuseless.callback = uselessf
        await interaction.followup.send(embed=embed, view=view)
    newuseless.callback = uselessf
    await ctx.send(embed=embed, view=view)

@client.command(name="test", description="To test if the bot is still working")
async def test(ctx):
    return await ctx.send("- tested")

@client.command(name="clear", description="To clear messages")
@commands.check_any(commands.is_owner(), commands.has_permissions(manage_channels=True))
async def clear(ctx, number: int):
    return await ctx.channel.purge(limit=int(number) + 1)

@client.command(name="guess", description="guessing game :3")
async def guess(ctx, max: int = 100):
    def check(msg):
        return msg.channel == ctx.channel and msg.content.isnumeric()

    n = random.randint(0, max)
    await ctx.send(f"## starting the guessing (min: 0, max: {max})")
    while True:
        try:
            e = await client.wait_for("message", check=check, timeout=60)
            if any([u in e.content for u in ["leave", "quit"]]):
                return ctx.send("> Exiting...")
            if int(e.content) == n:
                return await e.reply(f"# {e.author} wins!!")

            await ctx.send(("- more" if int(e.content) < n else "- less") + " than " + e.content)
        except asyncio.TimeoutError:
            await ctx.send("> Game timed out. Exiting.")
            break

@client.command(name="tictactoe", description="just to have fun playing tictactoe with friends :)")
async def tictactoe(ctx, plyr: disnake.Member):
    board = [[" ", " ", " "] for _ in range(3)]
    e = ["X", "O"]
    random.shuffle(e)
    players = {e[0]: ctx.author, e[1]: plyr}
    current_player = e[0]
    message = await ctx.send(f"## {players[current_player]}'s turn\n```\n{print_board(board)}\n```\n- play by sending coords, let's take as an example `1.2` for first row second column")
    def check(msg):
        return msg.member == players[current_player] and msg.channel == ctx.channel
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

@client.slash_command(name="meme", description="Sends a coding meme")
async def meme(interaction):
    await interaction.response.defer()
    memee = e()
    embed = disnake.Embed(title="meme time lol", color=disnake.Color.random())
    embed.set_image(memee)
    newmeme = Button(label="new one! :3", style=disnake.ButtonStyle.green)
    async def newmemef(interaction): 
        await interaction.response.defer()
        memee = e()
        embed = disnake.Embed(title="meme time lol", color=disnake.Color.random())
        embed.set_image(memee)
        embed.set_footer(text=f"requested by {interaction.author.name}")
        newmeme = Button(label="new one! :3", style=disnake.ButtonStyle.green)
        newmeme.callback = newmemef
        view = View()
        view.add_item(newmeme)
        return await interaction.send(embed=embed, view=view)
    newmeme.callback = newmemef
    view = View()
    view.add_item(newmeme)
    return await interaction.send(embed=embed, view=view)

@client.slash_command(name="test", description="To test if the bot is still working")
async def test(interaction):
    return await interaction.send("- tested")

@client.slash_command(name="useless", description="to get some useless fact about something very random")
async def useless(interaction, lang="en"):
    await interaction.response.defer()
    data = requests.get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}').json()
    embed = disnake.Embed(title="Useless Fact lmao", description="**" + data["text"] + "**", color=disnake.Color.random())
    newuseless = Button(label="again ^^", style=disnake.ButtonStyle.green)
    view = View()
    view.add_item(newuseless)
    async def uselessf(interaction): 
        await interaction.response.defer()
        data = requests.get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}').json()
        embed = disnake.Embed(title="Useless Fact lmao", description="**" + data["text"] + "**", color=disnake.Color.random())
        view = View()
        newuseless = Button(label="again ^^", style=disnake.ButtonStyle.green)
        view.add_item(newuseless)
        newuseless.callback = uselessf
        await interaction.followup.send(embed=embed, view=view)
    newuseless.callback = uselessf
    await interaction.followup.send(embed=embed, view=view)

@client.slash_command(name="darkjoke", description="to get a really darkjoke")
async def darkjoke(interaction):
    await interaction.response.defer()
    data = random.choice(darkjokes)
    embed = disnake.Embed(title="a darkjoke :skull:", description="\u200b", color=disnake.Color.random())
    embed.add_field(name=data["buildup"] + "?", value=data["punchline"], inline=False)
    newdj = Button(label="more >:)", style=disnake.ButtonStyle.green)
    view = View()
    view.add_item(newdj)
    async def darkjokef(interaction): 
        await interaction.response.defer()
        data = random.choice(darkjokes)
        embed = disnake.Embed(title="a darkjoke :skull:", description="\u200b", color=disnake.Color.random())
        embed.add_field(name=data["buildup"] + "?", value=data["punchline"], inline=False)
        view = View()
        newdj = Button(label="more >:)", style=disnake.ButtonStyle.green)
        view.add_item(newdj)
        newdj.callback = darkjokef
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    newdj.callback = darkjokef
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@client.slash_command(name="clear", description="To clear messages")
@commands.check_any(commands.is_owner(), commands.has_permissions(manage_channels=True))
async def clear(interaction, number: int):
    return await interaction.channel.purge(limit=int(number))

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

@client.slash_command(name="distro", description="get distrowatch info")
async def distro(interaction, os):
    await interaction.response.defer()
    data, description = distrowatch(os)
    embed = disnake.Embed(title=f'{os} according to distrowatch', description=description, url=f"https://distrowatch.com/table.php?distribution={os}")
    for i in data:
        embed.add_field(name= i, value= data[i], inline=False)
    view = View()
    redirect = Button(label="See it on distrowatch :)", url=f"https://distrowatch.com/table.php?distribution={os}")
    view.add_item(redirect)
    await interaction.followup.send(embed=embed, view=view)

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
        await interaction.guild.voice_client.disconnect()
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

@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    wallpapers = json.loads(open("wallpapers.json", 'r').read())
    def get_valid_wallpaper():
        wallpaper = random.choice(wallpapers)
        response = requests.get(wallpaper)
        return wallpaper if response.status_code == 200 else get_valid_wallpaper()
    wallpaper_url = get_valid_wallpaper()
    back_response = requests.get(wallpaper_url, stream=True)
    back_response.raise_for_status()
    profile_response = requests.get(str(member.avatar.url), stream=True)
    profile_response.raise_for_status()
    background = create_welcome_image(
        Image.open(io.BytesIO(back_response.content)),
        Image.open(io.BytesIO(profile_response.content)),
        f"Welcome To {member.guild.name}!!",
        str(member.name)
    )
    file_bytes = io.BytesIO()
    background.save(file_bytes, format='PNG')
    file_bytes.seek(0)
    file = disnake.File(fp=file_bytes, filename="welcome.png")
    embed = disnake.Embed(
        title=f"Welcome {member.name}!!",
        description=f"I hope you feel the radiance in the `{member.guild.name}` server :3",
        color=disnake.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text=pyjokes.get_joke())
    embed.set_image(url=f"attachment://welcome.png")
    await channel.send(embed=embed, file=file)


client.run(token)
