import discord
from discord.ext import commands, tasks
import asyncio
import serial
import time

import psutil
import platform
from datetime import datetime



uname = platform.uname()
SystemType = uname.system
if SystemType == 'Windows':
    Pi = False
    ServerName = 'Official SteeleHook Server'
    RoleName = 'Test Role'
else:
    Pi = True
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ServerName = 'The Floof Farm'
    RoleName = 'Member'





class ServerInfo(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check_members.start()









    @tasks.loop(seconds=5)
    async def check_members(self):

        server = discord.utils.get(self.client.guilds, name=ServerName)
        #print(server)
        specific_role = discord.utils.get(server.roles, name=RoleName)
        global member_count
        member_count = specific_role.members
        #print(len(member_count))
        number_to_send = str(len(member_count))
        if Pi:
            ser.write(number_to_send.encode())
        else:
            pass




    @check_members.before_loop
    async def before_checking(self):
        await self.client.wait_until_ready()






def setup(client):
    client.add_cog(ServerInfo(client))
