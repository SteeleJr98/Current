import discord
import json
from datetime import datetime, timedelta
import re
from discord.ext import commands

class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
        jandl_id[str(guild.id)] = 'Not Set'
        with open('jandl_id.json', 'w') as f:
            json.dump(jandl_id, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
        jandl_id.pop(str(guild.id))
        with open('jandl_id.json', 'w') as f:
            json.dump(jandl_id, f, indent=4)





    @commands.command(aliases=['changejandl'])
    @commands.has_permissions(manage_guild=True)
    async def changejoinleave(self, ctx, channel):


        if channel == 'Unset':
            with open('jandl_id.json', 'r') as f:
                jandl_id = json.load(f)
            jandl_id[str(ctx.guild.id)] = channel

            with open('jandl_id.json', 'w') as f:
                json.dump(jandl_id, f, indent=4)
            await ctx.send(f'Joins and leaves channel was unset')

        else:
            #channelid = (((channel.replace('#', '')).replace('<', '')).replace('>', ''))

            channel = re.sub('[<#>]', '', channel)

            with open('jandl_id.json', 'r') as f:
                jandl_id = json.load(f)
            jandl_id[str(ctx.guild.id)] = channel

            with open('jandl_id.json', 'w') as f:
                json.dump(jandl_id, f, indent=4)
            await ctx.send(f'Joins and leaves channel set to <#{channel}>')






    @commands.Cog.listener()
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
        channel = self.client.get_channel(int(channel2))
        if channel == None:
            pass



        else:
            embed = discord.Embed(title=' ',
                description=descrip,
                colour = discord.Colour.green(),
                timestamp=datetime.utcnow()
            )

            embed.set_author(name='Member Joined', icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'ID: {member.id}')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        with open('jandl_id.json', 'r') as f:
            jandl_id = json.load(f)
            channel2 = jandl_id[str(member.guild.id)]
        channel = self.client.get_channel(int(channel2))
        if channel == None:
            pass

        else:
            embed = discord.Embed(title=' ',
                description=f'<@{member.id}> {member}',
                colour = discord.Colour.red(),
                timestamp=datetime.utcnow()
            )

            embed.set_author(name='Member Left', icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'ID: {member.id}')
            await channel.send(embed=embed)






def setup(client):
    client.add_cog(Logging(client))
