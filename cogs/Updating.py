import discord
import random
from discord.ext import commands
import json

class Updating(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def updatetest(self, ctx):
        await ctx.send("From update cog")


    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx):
        serverlist = []
        print('printing servers')
        for server in self.client.guilds:
            print(f'Name: {server.name} ID: {server.id}')
            serverlist.append(f'{server.name} {server.id}')
        await ctx.send(serverlist)





    @commands.command()
    @commands.is_owner()
    async def makenewfile(self, ctx, file_name):

        base_string = {}

        with open(f'{file_name}.json', 'w') as f: #make the file and add brackets
            json.dump(base_string, f, indent=0)

        for server in self.client.guilds:



            with open(f'{file_name}.json', 'r') as f:
                serverids = json.load(f)
                print('json loaded')

            serverids[str(server.id)] = None
            print('set channels to none')

            with open(f'{file_name}.json', 'w') as f:
                json.dump(serverids, f, indent=4)


        await ctx.send(f'File {file_name}.json has been created')









def setup(client):
    client.add_cog(Updating(client))
