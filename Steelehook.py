import discord
import os
import json
import random
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]




client = commands.Bot(command_prefix = get_prefix, case_insensitive=True)
client.remove_command('help')





@client.command()
@commands.has_permissions(manage_guild=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(manage_guild=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(manage_guild=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Cog "{extension}" has been reloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f'Cog loaded: {filename[:-3]}')
        client.load_extension(f'cogs.{filename[:-3]}')



@client.command()
@commands.has_permissions(manage_guild=True)
async def shutdown(ctx):
    def check(m):
        return m.channel == ctx.message.channel and m.author == ctx.message.author
    await ctx.send('Are you Sure? y/n')
    msg = await client.wait_for('message', check=check)
    responce = msg.content.lower()
    if responce == 'y':
        await ctx.send('Shutting Down.')
        await client.logout()
    elif responce == 'n':
        await ctx.send('Not Shutting Down.')
    else:
        await ctx.send('Invalid Responce.')









@client.event #add server to prefix list json file
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '&'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event #remove server from prefix json file
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)



@client.event #print when users join a server
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event #print when users leave a server
async def on_member_remove(member):
    print(f'{member} has left a server.')





@client.event #error handling for missing arguments, invalid commands, missing permissions
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please include all required arguments.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to use this command!')
    #elif isinstance(error, discord.errors.Forbidden):
        #await ctx.send("I don't have the permissions to do that")
    #else:
        #await ctx.send('I can not do that. Check my permissions and role hierarchy')











client.run(TOKEN) #bot token (a secret)
