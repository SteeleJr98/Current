import discord
import json
from discord.ext import commands
from discord.utils import get

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

        if member == ctx.author:
            await ctx.send('You can\'t kick yourself') #if the user mentioned is the same as the command user then don't kick


        else:
            if member.top_role >= ctx.author.top_role:
                await ctx.send('That user is at or above your top role. You can\'t kick them') #if the user mentioned has a top role above the highest role of the command user, don't kick

            else:
                await member.kick(reason=reason)
                await ctx.send(f'User {member} was kicked with reason: {reason}')





    @commands.command() #Adding removing roles from a User
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member : discord.Member, *, roles):


        roles_specified = roles.lower() #gather the roles specified
        roles_split = [r.strip() for r in roles_specified.split(',')] #remove spaces from the beginning of roles and spit the roles separated by ','




        roles_to_add = [r[1:] for r in roles_split if r.startswith('+')] #get all the roles that start with a '+'
        roles_to_remove = [r[1:] for r in roles_split if r.startswith('-')] #get all the roles that start with a '-'
        roles_to_toggle = [r[0:] for r in roles_split if not r.startswith('+') and not r.startswith('-')] #get all the roles that don't start with a '+' or a '-'
        #all_roles = [r[1:] for r in roles_split if r.startswith('+') or r.startswith('-')]


        #set our lists for messages stating changes
        role_errors_adding = []
        role_errors_removing = []
        roles_not_found = []
        roles_missing_permissions = []
        roles_changed = []



        for role in roles_to_add:
            role_to_add = discord.utils.find(lambda m: m.name.lower() == role, member.guild.roles) #get the actual role from the server and assign it to the role mentioned
            #print(role_to_add)
            if role_to_add == None: #if the role doesn't exist add the role from the command to the list of errored role list
                roles_not_found.append(role)
            else:
                if role_to_add < ctx.author.top_role: #check if a role is above the highest role from the command user, if it is, add it to the forbidden list
                    try:
                        if role_to_add not in member.roles: #check if the user mentioned has the role if no, give the user the role and add it to the added roles list
                            await member.add_roles(role_to_add)
                            roles_changed.append('+'+role)
                        else:
                            role_errors_adding.append(role) #if the bot can't change the role because of permissions, add the role to the missing permissions list
                    except discord.errors.Forbidden:
                        roles_missing_permissions.append(role)

                else:
                    roles_missing_permissions.append(role)

        #the comments for the other roles are close to the same and I'm too lazy to add those comments o3o

        for role in roles_to_remove:
            role_to_remove = discord.utils.find(lambda m: m.name.lower() == role, member.guild.roles)
            #print(role_to_remove)
            if role_to_remove == None:
                roles_not_found.append(role)
            else:
                if role_to_remove < ctx.author.top_role:
                    try:
                        if role_to_remove in member.roles:
                            await member.remove_roles(role_to_remove)
                            roles_changed.append('-'+role)
                        else:
                            role_errors_removing.append(role)
                    except discord.errors.Forbidden:
                        roles_missing_permissions.append(role)

                else:
                    roles_missing_permissions.append(role)


        for role in roles_to_toggle:
            role_to_toggle = discord.utils.find(lambda m: m.name.lower() == role, member.guild.roles)
            #print(role_to_toggle)
            if role_to_toggle == None:
                roles_not_found.append(role)
            else:
                if role_to_toggle < ctx.author.top_role:
                    try:
                        if role_to_toggle in member.roles:
                            await member.remove_roles(role_to_toggle)
                            roles_changed.append('-'+role)
                        else:
                            await member.add_roles(role_to_toggle)
                            roles_changed.append('+'+role)
                    except discord.errors.Forbidden:
                        roles_missing_permissions.append(role)

                else:
                    roles_missing_permissions.append(role)







        #setting the strings for the messages we send using the lists from before

        roles_changed2 = ', '
        role_errors_adding2 = ', '
        role_errors_removing2 = ', '
        roles_not_found2 = ', '
        roles_missing_permissions2 = ', '


        if roles_changed:
            await ctx.send(f'Changed roles for {member}: {roles_changed2.join(roles_changed)}')

        if roles_not_found:
            await ctx.send(f'I couldn\'t find role(s): {roles_not_found2.join(roles_not_found)}')

        if roles_missing_permissions:
            await ctx.send(f'I can\'t change the role(s): {roles_missing_permissions2.join(roles_missing_permissions)}')







    @commands.command() #command to ban user with response of user and reason
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):


        if member == ctx.author:
            await ctx.send('You can\'t ban yourself') #if the user mentioned is the same as the command user then don't ban

        else:
            if member.top_role >= ctx.author.top_role:
                await ctx.send('That user is at or above your top role. You can\'t ban them') #if the user mentioned has a top role above the highest role of the command user, don't ban


            else:
                await member.ban(reason=reason, delete_message_days=0) #ban the user and don't delete any messages from the user
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
