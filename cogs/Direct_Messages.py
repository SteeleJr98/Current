import discord
from discord.ext import commands

class Direct_Messages(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def dm(self, ctx):
        await ctx.author.send('test message')

    






def setup(client):
    client.add_cog(Direct_Messages(client))
