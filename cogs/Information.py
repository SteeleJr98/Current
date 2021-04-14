import discord
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
import random

import psutil
import platform

from .Logging import *


uname = platform.uname()
SystemType = uname.system
if SystemType == 'Windows':
    status = (['Currently Testing'])
else:
    status = (['Generating Crash Log', 'Reticulating Splines',
            'Roasting Plumbers', 'Unfreezing, One Moment',
            'Please hang up and try your call again',
            'Watching You Masticate', 'Monching Leaves',
            'Laser + Dino = Perfection']) #list of statuses the bot will use

Version = 'Snapshot 4.0.0' #version number





class Information(commands.Cog):



    def __init__(self, client):
        self.client = client
        self.change_status.start()



    @tasks.loop(minutes=5) #update the status every 5 minutes
    async def change_status(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(status)))


    @change_status.before_loop #wait until the bot is ready before starting the change status loop
    async def before_changing(self):
        await self.client.wait_until_ready()



    @commands.Cog.listener() #when the bot is ready to act print the version number in the console
    async def on_ready(self):
        print(f'Bot is online running version {Version}')



    @commands.command() #Ping command that shows latency as well
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.client.latency * 1000)}ms.')
        #await ctx.send('test')


        await log_command(self, ctx, name = "ping")










    @commands.command() #replies with the version number
    async def version(self, ctx):
        await ctx.send(Version)

        await log_command(self, ctx, name = "version")



    @commands.command(aliases=['server']) #DMs the official server link to the command user
    async def helpserver(self, ctx):
        await ctx.author.send("https://discord.gg/ffwhQJu")
        await ctx.send('Sent you the link :3')



    @commands.command() #DMs the help list to the command user
    async def help(self, ctx):
        async with ctx.typing(): #appear as if typing in the channel the command is used in

            embed = discord.Embed(
                colour = discord.Colour.green()
            )


            embed.set_author(name='Fun')
            embed.add_field(name='8ball', value='Ask a question and a yes or no responce. Usage: 8ball (question)', inline=False)
            embed.add_field(name='coinflip', value='Heads or tails? Let the bot decide. Usage: coinflip', inline=False)
            embed.add_field(name='say', value='Make the bot say anything you like. Usage: say (message)', inline=False)
            embed.add_field(name='derp', value='Does a derp. Usage: derp')
            embed.add_field(name='cringe', value='Who posted cringe? Usage: cringe (user)', inline=False)
            embed.add_field(name='yeet', value='YEET. Usage yeet', inline=False)
            embed.add_field(name='yote', value='Yote... Usage yote', inline=False)

            await ctx.author.send(embed=embed)

            embed5 = discord.Embed(
                colour = discord.Colour.purple()
            )

            embed5.set_author(name='Music (Tempororily Disabled Until I Can Make It Good)')
            embed5.add_field(name='join', value='Connects the bot to the voice channel you\'re in. Usage: join', inline=False)
            embed5.add_field(name='leave', value='Disconnects the bot from the voice channel it\'s in. Usage: leave', inline=False)
            embed5.add_field(name='play', value='Bot plays the audio from a YouTube link sent with this command. Usage: play (YouTube link)', inline=False)
            embed5.add_field(name='pause', value='Pauses the audio the bot is playing. Usage: pause', inline=False)
            embed5.add_field(name='resume', value='Resumes the audio if it\'s paused. Usage: resume', inline=False)
            embed5.add_field(name='stop', value='Stops the audio playing and disconnects the bot from the voice channel. Usage: stop', inline=False)
            embed5.set_footer(text='Only works with YouTube at the moment.')

            await ctx.author.send(embed=embed5)

            embed2 = discord.Embed(
                colour = discord.Colour.orange()
            )

            embed2.set_author(name='Information')
            embed2.add_field(name='ping', value='Pong! but also shows the bot\'s latency. Usage: ping', inline=False)
            embed2.add_field(name='version', value='Shows the bot\'s current version. Usage: version', inline=False)

            await ctx.author.send(embed=embed2)


            embed3 = discord.Embed(
                colour = discord.Colour.red()
            )

            embed3.set_author(name='Moderation')
            embed3.add_field(name='ban', value='Bans a member from the server. Usage: ban (user) {reason}', inline=False)
            embed3.add_field(name='kick', value='Kicks a member from the server Usage: kick (user) {reason}', inline=False)
            embed3.add_field(name='unban', value='Unbans a memebr from the sevrer. Usage: unban (User\'s discord tag)', inline=False)
            embed3.add_field(name='clear', value='Removes a number of messages sent in a channel. Usage: clear/purge (Number of messages)', inline=False)
            embed3.add_field(name='changeprefix', value='Changes the bot\'s prefix for the server. Usage: changeprefix (new prefix)', inline=False)
            embed3.add_field(name='role', value='Adds/removes roles from a user. "+role" adds the role,"-role" removes the role, not specifying +/- toggles the role. Roles are to be separated by a ",". Usage: role (user) (role)', inline=False)
            embed3.add_field(name='changejoinleave', value='Change the channel that joins/leaves are logged. Usage: changejoinleave (channel) Note: Use "Unset" for (channel) to stop logging', inline=False)
            embed3.add_field(name='whois', value='Check information on a user. Usage: whois (user)', inline=False)
            embed3.add_field(name='setlogging', value='Set which commands are logged in the logging channel. Possible commands to log are: role, ban, kick, clear, unban, prefix. Usage: setlogging (command)', inline=False)
            await ctx.author.send(embed=embed3)


            embed4 = discord.Embed(
                colour = discord.Colour.blue()
            )

            embed4.set_author(name='Misc')
            embed4.add_field(name='help', value='sends you this message. Usage: help', inline=False)
            embed4.add_field(name='Support Server', value='Sends you a link to the official support server. Usage: server', inline=False)
            embed4.add_field(name='DM Support', value='To use bot commands within a direct message with the bot you must use the prefix "&"', inline=False)

            await ctx.author.send(embed=embed4)
            await ctx.send('Check your DMs <:SteeleWink:641527508453425152>')





def setup(client):
    client.add_cog(Information(client))
