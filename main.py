import discord
from discord.ext import commands
import random
import requests
import os
from keep_alive import keep_alive
from typing import Optional

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

# Disable default help command
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# 🔒 Word detection lists
ABUSIVE_WORDS = [
    "fuck", "fck", "f*ck", "shit", "bitch", "asshole", "nigga", "slut", "dick",
    "cunt", "whore", "retard", "gay", "faggot", "porn", "nsfw", "18+", "nude",
    "onlyfans", "rape", "suck", "kill yourself", "die", "btch", "bastard"
]

SUSPICIOUS_LINKS = ["discordapp.com/invite", "discord.gg", "tinyurl", "bit.ly", "invite"]

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")  
    # Set status to Watching
    activity = discord.Activity(type=discord.ActivityType.watching, name="Minecraft Slayer | Managing Server | 24/7")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    msg = message.content.lower()

    # 🚨 Detect bad words or links
    if any(word in msg for word in ABUSIVE_WORDS + SUSPICIOUS_LINKS):
        try:
            await message.delete()
            await message.channel.send(
                f"🚫 {message.author.mention}, your message violated the server rules."
            )
            await message.guild.ban(message.author, reason="NSFW or abusive content")
            log_channel = discord.utils.get(message.guild.text_channels, name="mod-log")
            if log_channel:
                await log_channel.send(
                    f"⚠️ User {message.author} banned for message: `{message.content}`"
                )
        except Exception as e:
            print(f"Error: {e}")

    # Bot mention basic response
    if bot.user and bot.user.mention in message.content:
        await message.channel.send("Yes, Did you mentioned me! How can I help you.....?")

    await bot.process_commands(message)

# 🔧 Custom Help Command
@bot.command(name="help")
async def custom_help(ctx):
    help_text = """
📚 **Bot Command List**

👑 Creator:
`!god`, `!bow`, `!respect`, `!creator`, `!legend`

🧱 Minecraft Tools:
`!mcserver <ip>` - Show Minecraft server status  
`!mcadvise` - Get a Minecraft tip  
`!mcversion` - Show latest Minecraft version  
`!mcrecipe <item>` - Show crafting recipe  
`!mcitem <name>` - Search Minecraft Wiki

🛡️ Moderation (auto):
- Blocks abusive or NSFW messages
- Deletes and bans users on violations
- Alerts mods in `#mod-log` if exists

💬 Mention me with `@Minecraft Slayer` to talk!
"""
    await ctx.send(help_text)

# 💬 Fun & Creator Commands
@bot.command()
async def god(ctx):
    await ctx.send("My creator is **Ansh** 👑")

@bot.command()
async def bow(ctx):
    await ctx.send("🛐 Bow before the legend — **Ansh** has entered.")

@bot.command()
async def respect(ctx):
    await ctx.send("Respect isn't given, it's earned. Ansh owns it.")

@bot.command()
async def creator(ctx):
    await ctx.send("My creator? None other than **Ansh** 🧠")

@bot.command()
async def legend(ctx):
    await ctx.send("Stories are told about **Ansh** in the binary realm.")

# 🧱 Minecraft Tools
@bot.command()
async def mcserver(ctx, ip: str):
    try:
        r = requests.get(f"https://api.mcsrvstat.us/2/{ip}")
        data = r.json()
        if data["online"]:
            players = data["players"]["online"]
            max_players = data["players"]["max"]
            version = data["version"]
            motd = '\n'.join(data["motd"]["clean"])
            await ctx.send(
                f"✅ **{ip}** is online!\n"
                f"🧍 Players: {players}/{max_players}\n"
                f"🌐 Version: {version}\n"
                f"📢 MOTD: {motd}"
            )
        else:
            await ctx.send(f"❌ Server `{ip}` is offline.")
    except requests.exceptions.RequestException:
        await ctx.send("⚠️ Failed to fetch server info.")

@bot.command()
async def mcadvise(ctx):
    tips = [
        "Always carry a water bucket — it's life-saving in lava or heights!",
        "Use F3+B to show hitboxes — perfect for precise mob farms.",
        "Wearing a carved pumpkin lets you look at endermen safely.",
        "Use torches under gravel/sand for fast mining.",
        "Ender chests + shulker boxes = unlimited inventory freedom!"
    ]
    await ctx.send(f"📘 Minecraft Tip: {random.choice(tips)}")

@bot.command()
async def mcversion(ctx):
    await ctx.send("🧱 Latest Minecraft Java Version: **1.20.6** (as of July 2025)")

@bot.command()
async def mcrecipe(ctx, item: Optional[str] = None):
    if item is None:
        await ctx.send("🔍 Example: `!mcrecipe diamond_sword`")
        return
    recipes = {
        "diamond_sword": "🗡️ Diamond Sword: 2 Diamonds + 1 Stick",
        "crafting_table": "🛠️ Crafting Table: 4 Wooden Planks",
        "torch": "🔥 Torch: 1 Stick + 1 Coal",
        "furnace": "🔥 Furnace: 8 Cobblestone",
        "pickaxe": "⛏️ Pickaxe: 3 Material (Wood/Stone/Iron/etc) + 2 Sticks"
    }
    item = item.lower()
    if item in recipes:
        await ctx.send(f"{recipes[item]}")
    else:
        await ctx.send("❌ Recipe not found. Try `diamond_sword`, `torch`, `crafting_table`, etc.")

@bot.command()
async def mcitem(ctx, name: str):
    if not name:
        await ctx.send("🔍 Usage: `!mcitem diamond_sword`")
        return
    await ctx.send(f"🔎 Looking for info about `{name}`? Check: https://minecraft.wiki/search?search={name.replace(' ', '%20')}")

# 🔁 Keep the bot alive on Replit
keep_alive()

# 🔑 Run the bot
token = os.getenv("TOKEN")
if token is None:
    raise ValueError("TOKEN environment variable not set!")
bot.run(token)
