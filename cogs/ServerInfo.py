import discord
from discord.ext import commands, tasks
import asyncio
import serial
import time

#ser = serial.Serial('COM4', 9600)





class ServerInfo(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check_members.start()




    # @commands.command()
    # async def check_members(self, ctx, *, member_role):
    #     print('gonna do the thing now')
    #     thing = discord.utils.get(ctx.author.guild.roles, name=member_role)
    #
    #     print(thing)
    #     thing2 = thing.members
    #     print(thing2)
    #     await ctx.send(len(thing2))





    @tasks.loop(seconds=5)
    async def check_members(self):
        #servers = self.client.guilds
        #print(servers)

        server = discord.utils.get(self.client.guilds, name='Official SteeleHook Server')
        #print(server)
        specific_role = discord.utils.get(server.roles, name='Test Role')
        global member_count
        member_count = specific_role.members
        #print(len(member_count))
        number_to_send = str(len(member_count))
        #ser.write(number_to_send.encode())





    @check_members.before_loop
    async def before_checking(self):
        await self.client.wait_until_ready()






def setup(client):
    client.add_cog(ServerInfo(client))
