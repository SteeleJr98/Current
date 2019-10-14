import discord
from discord.ext import commands




Version = discord.Game('SteeleHookv2.3.0')

class Information(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=Version)
        print(f'Bot is online running version {Version}')





    @commands.command() #Ping command that shows latency as well
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.client.latency * 1000)}ms.')

    # @commands.command()
    # async def ping2(self, ctx):
    #     await ctx.send('responding from a cog')





def setup(client):
    client.add_cog(Information(client))
