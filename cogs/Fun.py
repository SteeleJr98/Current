import discord
import random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball']) #short random choice example with question/response
    async def _8ball(self, ctx, *, question):
        responses = ['Yes', 'No']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')



    @commands.command(aliases=['coin']) #short random choice example with no question
    async def coinflip(self, ctx):
        responses = ['Heads', 'Tails']
        await ctx.send(f'Flipping a coin!\nResult: {random.choice(responses)}')

    @commands.command() #deletes the command message and sends what the user said
    async def say(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{message}')

    @commands.command()
    async def MeasureVengefulsDick(self, ctx):
        await ctx.send('Error 404: Dick Not Found.')





def setup(client):
    client.add_cog(Fun(client))
