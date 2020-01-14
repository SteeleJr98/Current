import discord
import random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball']) #short random choice example with question/response
    async def _8ball(self, ctx, *, question):
        responses = [ 'It is certain.', 'It is decidedly so.',
                    'Without a doubt.', 'Yes - definitely.',
                    'You may rely on it.', 'As I see it, yes.',
                    'Most likely.', 'Outlook good.',
                    'Yes.', 'Signs point to yes.',
                    'Reply hazy, try again.', 'Ask again later.',
                    'Better not tell you now.', 'Cannot predict now.',
                    'Concentrate and ask again.', 'Don\'t count on it.',
                    'My reply is no.', 'My sources say no.',
                    'Outlook not so good.', 'Very doubtful.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')



    @commands.command(aliases=['coin']) #short random choice example with no question
    async def coinflip(self, ctx):
        responses = ['Heads', 'Tails']
        await ctx.send(f'Flipping a coin!\nResult: {random.choice(responses)}')


    @commands.command() #deletes the command message and sends what the user said
    async def say(self, ctx, *, content):

        if '@everyone' in content:
            print('Everyone pinged')
            await ctx.send('I can\'t ping everyone')

        elif '@here' in content:
            print('Here pinged')
            await ctx.send('I can\'t ping here')

        else:
            await ctx.message.delete()
            await ctx.send(f'{content}')



    @commands.command() #send the derp emote
    async def derp(self, ctx):
        await ctx.send('<:SteeleDerp:641527755040620554>')


    @commands.command() #str(member)[:-5] says the user mentioned removing the descriminator (always 5 characters)
    async def cringe(self, ctx, member : discord.Member):
        await ctx.send(f'**{str(member)[:-5]}** just posted cringe. They will lose subscriber.')

    @commands.command() #just a reply message
    async def yeet(self, ctx):
        await ctx.send('(╯°□°）╯︵ ┻━┻')


    @commands.command()
    async def test(self, ctx):
        user = self.client.get_user(555470319998074886)
        await user.send('test')
        await ctx.send(f'message sent to {user}')






def setup(client):
    client.add_cog(Fun(client))
