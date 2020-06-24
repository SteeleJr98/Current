import discord
import json
from datetime import datetime, timedelta
import re
import asyncio
from discord.ext import commands




async def log_command(self, ctx, name):

    with open('serverlogsettings.json', 'r') as f:
        logchannel = json.load(f)
        #print('json loaded')
        settings = logchannel[str(ctx.guild.id)]
    #print(f'settings loaded: {settings}')




    #print(f'command name {name}')


    if name not in settings:
        #print('command not set')
        return


    else:
        with open('command_logging.json', 'r') as f:
            logcnl = json.load(f)
            channel2 = logcnl[str(ctx.guild.id)]

        if channel2 == None:
            pass
        else:
            channel = self.client.get_channel(int(channel2)) #get the channel ID from the jandl_id file
            if channel == None: #if no channel set for the server, do nothing
                pass
            else:
                await channel.send(f'Command {name} was used')

async def change_log_specified(self, server, setting):
    print('in function')
    print(setting)

    #list_trimmed = [s.strip() for s in setting.split(',')]


    with open('serverlogsettings.json', 'r') as f:
        guildsettings = json.load(f)
        print(f'settings for {server}: {guildsettings[str(server.id)]}')
    #guildsettings[str(server.id)] = setting

    trimmed_settings = [guildsettings[str(server.id)]]
    print(f'trimmed settings: {trimmed_settings} with length of {len(trimmed_settings)} and type {type(trimmed_settings)}')
    list_trimmed = [s.strip("[']") for s in str(trimmed_settings).split(',')]
    new_list_trimmed = [s.strip( ) for s in list_trimmed]
    print(f'new list trimmed: {new_list_trimmed}')
    if None in trimmed_settings:
        print(f'None found in list')
        trimmed_settings = []
        print(f'empty trimmed setting {trimmed_settings}')

    # check_string = ' '
    # check_string = check_string.join(trimmed_settings)
    # print(f'check string: {check_string}')
    #
    # #setting = re.sub('[","]', '', setting)
    # #print(f'setting string: {setting}')
    #
    # converted_setting = str(setting)
    # converted_setting = (((converted_setting.replace('[', '')).replace(',', '')).replace(']', '')).replace("'", '')
    # print(f'converted_setting: {converted_setting}')

    # if converted_setting in check_string:
    #
    #     print('setting in settings already')
    #     trimmed_settings.remove(trimmed_settings[setting])

    #if setting in guildsettings[str(server.id)]:
    if setting in new_list_trimmed:
        print('setting in settings already')

        # print(f'location {trimmed_settings[1]}')
        # trimmed_settings.replace('ban', '')
        #guildsettings[str(server.id)] = (guildsettings[str(server.id)]).replace(str(setting), '')
        string_setting = str(setting)
        # print(type(string_setting))
        # print(type(guildsettings[str(server.id)]))
        print(string_setting)
        print(guildsettings[str(server.id)])
        guild_list = [s.strip() for s in (guildsettings[str(server.id)]).split(',')]
        print(f'guild list: {guild_list}')
        guild_list.remove(string_setting)
        print(f'guild list after remove: {guild_list}')

        guildsettings[str(server.id)] = (str(guild_list)).strip("[']")




    else:
        print('setting being added to list')
        trimmed_settings.append(setting)

        print(f'new trimmed: {trimmed_settings}')

        setting_string = ', '
        print(setting_string)
        setting_string = setting_string.join(trimmed_settings)
        print(f'string: {setting_string}')

        guildsettings[str(server.id)] = setting_string

    print(f'new settings {guildsettings}')
    with open('serverlogsettings.json', 'w') as f:
        json.dump(guildsettings, f, indent=4)





















class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client








    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setlogging(self, ctx, *, settings):
        possible_logs = ['role', 'ban', 'kick', 'clear', 'unban', 'prefix', 'ping']

        #print(settings)

        trimmed_settings = [s.strip() for s in settings.split(',')]
        #print(trimmed_settings)

        error_settings = []
        pass_settings = []

        for setting in trimmed_settings:
            if setting in possible_logs:
                pass_settings.append(setting)
                #await ctx.send('in settings')
                #await change_log_specified(self, ctx.guild, setting)
            else:
                error_settings.append(setting)
                #await ctx.send('invalid setting')
        if error_settings:
            await ctx.send(f'{error_settings} not in possible settings')

        if pass_settings:
            print(f'TEST: {pass_settings[0]}')

            for i in pass_settings:
                print(f'Setting: {i}')
                await change_log_specified(self, ctx.guild, i)











    @commands.command()
    async def test(self, ctx):
        name = ctx.author.id
        await log_command(self, ctx, name)


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


        if channel.lower() == 'unset':
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
    async def changelogging(self, ctx, channel):
        #do stuff

        if channel.lower() == 'unset':
            with open('command_logging.json', 'r') as f:
                jandl_id = json.load(f)
            jandl_id[str(ctx.guild.id)] = None

            with open('command_logging.json', 'w') as f:
                json.dump(jandl_id, f, indent=4)
            await ctx.send(f'Command logging channel was unset')

        else:
            #channelid = (((channel.replace('#', '')).replace('<', '')).replace('>', ''))

            channel = re.sub('[<#>]', '', channel) #remove the characters <, #, and > from the channel so to just get the channel ID

            with open('command_logging.json', 'r') as f:
                jandl_id = json.load(f)
            jandl_id[str(ctx.guild.id)] = channel

            with open('command_logging.json', 'w') as f:
                json.dump(jandl_id, f, indent=4) #change the value of linked to the server's ID in the jandl_id file

            await ctx.send(f'Command logging channel set to <#{channel}>')








    @commands.command()
    async def bans(self, ctx):
        banned_users = await ctx.guild.bans()
        await ctx.send(banned_users)






def setup(client):
    client.add_cog(Logging(client))
