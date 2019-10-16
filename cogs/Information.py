import discord
from discord.ext import commands




Version = discord.Game('SteeleHookv2.4.1')

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


    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            colour = discord.Colour.green()
        )


        embed.set_author(name='Fun')
        embed.add_field(name='8ball', value='Ask a question and a yes or no responce. Usage: 8ball (question)', inline=False)
        embed.add_field(name='coinflip', value='Heads or tails? Let the bot decide. Usage: coinflip', inline=False)
        embed.add_field(name='say', value='Make the bot say anything you like. Usage: say (message)', inline=False)

        await ctx.author.send(embed=embed)


        embed2 = discord.Embed(
            colour = discord.Colour.orange()
        )

        embed2.set_author(name='Information')
        embed2.add_field(name='ping', value='Pong! but also shows the bot\'s latency. Usage: ping', inline=False)

        await ctx.author.send(embed=embed2)


        embed3 = discord.Embed(
            colour = discord.Colour.red()
        )

        embed3.set_author(name='Moderation')
        embed3.add_field(name='ban', value='Bans a member from the serevr. Usage: ban (member ID) {reason}', inline=False)
        embed3.add_field(name='kick', value='Kicks a member from the server Usage: kick (member ID) {reason}', inline=False)
        embed3.add_field(name='unban', value='Unbans a memebr from the sevrer. Usage: unban (Member\'s discord tag)', inline=False)
        embed3.add_field(name='clear', value='Removes a number of messages sent in a channel. Usage: clear (Number of message)', inline=False)
        embed3.add_field(name='changeprefix', value='Changes the bot\'s prefix for the server. Usage: changeprefix (new prefix)', inline=False)

        await ctx.author.send(embed=embed3)


        embed4 = discord.Embed(
            colour = discord.Colour.blue()
        )

        embed4.set_author(name='Help')
        embed4.add_field(name='help', value='sends you this message. Usage: help', inline=False)

        await ctx.author.send(embed=embed4)
        await ctx.send('Ckeck your DMs')






def setup(client):
    client.add_cog(Information(client))
