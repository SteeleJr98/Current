import discord
import json
from datetime import datetime, timedelta
import re
import asyncio
from discord.ext import commands

class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.Cog.listener() #when the bot joins a server put the server ID in the jandl_id file with the value "Not Set"
    async def on_guild_join(self, guild):
        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
        jandl_id[str(guild.id)] = None
        with open('jandl_id.json', 'w') as f:
            json.dump(jandl_id, f, indent=4)

    @commands.Cog.listener() #when the bot leaves a server remove the the server's ID from the jandl file
    async def on_guild_remove(self, guild):
        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
        jandl_id.pop(str(guild.id))
        with open('jandl_id.json', 'w') as f:
            json.dump(jandl_id, f, indent=4)





    @commands.command(aliases=['changejandl']) #change the value beside the server's ID to a specific channel in the jandl file
    @commands.has_permissions(manage_guild=True)
    async def changejoinleave(self, ctx, channel):


        if channel == 'Unset':
            with open('jandl_id.json', 'r') as f:
                jandl_id = json.load(f)
            jandl_id[str(ctx.guild.id)] = None

            with open('jandl_id.json', 'w') as f:
                json.dump(jandl_id, f, indent=4)
            await ctx.send(f'Joins and leaves channel was unset')

        else:
            #channelid = (((channel.replace('#', '')).replace('<', '')).replace('>', ''))

            channel = re.sub('[<#>]', '', channel) #remove the characters <, #, and > from the channel so to just get the channel ID

            with open('jandl_id.json', 'r') as f:
                jandl_id = json.load(f)
            jandl_id[str(ctx.guild.id)] = channel

            with open('jandl_id.json', 'w') as f:
                json.dump(jandl_id, f, indent=4) #change the value of linked to the server's ID in the jandl_id file

            await ctx.send(f'Joins and leaves channel set to <#{channel}>')






    @commands.Cog.listener() #say when a member joins the server send a mesage to the channel specified in the jandl_id file, if it's not set, do nothing
    async def on_member_join(self, member):

        account_age_seconds = ((datetime.utcnow()) - (member.created_at)).total_seconds()


        if account_age_seconds < 604800:


            days = int(account_age_seconds // (24 * 3600))
            account_age_seconds = account_age_seconds % (24 * 3600)
            hours = int(account_age_seconds // 3600)
            account_age_seconds %= 3600
            minutes = int(account_age_seconds // 60)
            account_age_seconds %= 60
            seconds = int(account_age_seconds)

            descrip = f'<@{member.id}> {member} \n Account Created {days} days, {hours} hours, {minutes} minutes, {seconds} seconds ago'

        else:
            descrip = f'<@{member.id}> {member}'




        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
            channel2 = jandl_id[str(member.guild.id)]


        if channel2 == None:
            pass
        else:
            channel = self.client.get_channel(int(channel2)) #get the channel ID from the jandl_id file
            if channel == None: #if no channel set for the server, do nothing
                pass



            else: #send this embed to the channel set in the jandl_id file
                embed = discord.Embed(title=' ',
                    description=descrip,
                    colour = discord.Colour.green(),
                    timestamp=datetime.utcnow()
                )

                embed.set_author(name='Member Joined', icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=f'ID: {member.id}')
                await channel.send(embed=embed)



    # @commands.Cog.listener()
    # async def on_member_ban(self, guild, member):
    #
    #     with open('jandl_id.json', 'r') as f:
    #         jandl_id = json.load(f)
    #         channel2 = jandl_id[str(member.guild.id)]
    #
    #     if channel2 == None:
    #         pass
    #     else:
    #         channel = self.client.get_channel(int(channel2)) #get the channel ID from the jandl_id file
    #         if channel == None: #if no channel set for the server, do nothing
    #             pass
    #
    #         else: #send this embed to the channel set in the jandl_id file
    #
    #             await channel.send('Aaaaaa')





    @commands.Cog.listener() #say when a member leaves the server send a mesage to the channel specified in the jandl_id file, if it's not set, do nothing
    async def on_member_remove(self, member):

        banned_users = await member.guild.bans()
        if len(banned_users) == 0:
            name = 'Member Left'
        else:
            for ban_entry in banned_users:
                user = ban_entry.user
                if member == user:
                    name = 'Member Banned'
                else:
                    name = 'Member Left'




        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
            channel2 = jandl_id[str(member.guild.id)]

        if channel2 == None:
            pass
        else:
            channel = self.client.get_channel(int(channel2)) #get the channel ID from the jandl_id file
            if channel == None: #if no channel set for the server, do nothing
                pass

            else: #send this embed to the channel set in the jandl_id file





                embed = discord.Embed(title=' ',
                    description=f'<@{member.id}> {member}',
                    colour = discord.Colour.red(),
                    timestamp=datetime.utcnow()
                )

                embed.set_author(name=name, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=f'ID: {member.id}')
                await channel.send(embed=embed)



    @commands.command()
    async def bans(self, ctx):
        banned_users = await ctx.guild.bans()
        await ctx.send(banned_users)






def setup(client):
    client.add_cog(Logging(client))
