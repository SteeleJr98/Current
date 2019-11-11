import discord
import json
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client






    @commands.command() #command to purge a number of messages in a channel
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount+1)

    @commands.command() #command to kick user with response of user and reason
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} was kicked with reason: {reason}')





    # @commands.command() #Adding removing roles from a User
    # @commands.has_permissions(manage_roles=True)
    # async def role(self, ctx, member : discord.Member, *, roles):
    #     await ctx.send(f'Changed roles for {member}')
    #     await ctx.send(f'{roles}')







    @commands.command() #command to ban user with response of user and reason
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} was banned with reason: {reason}')

    @commands.command() #unban command that requires full discord user name 'Example#1234'
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'User {member} was unbanned')
                return

    # @commands.command() #this does not work to unban
    # @commands.has_permissions(ban_members=True)
    # async def unban2(self, ctx, member : discord.Member):
    #     await ctx.guild.unban(member)
    #     await ctx.send (f'User {member} was unbanned')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def changeprefix(self, ctx, prefix):
        #print('Attempting Change')
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        #print('Atempting Change2')
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'Prefix changed to: {prefix}')



def setup(client):
    client.add_cog(Moderation(client))
