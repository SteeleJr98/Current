import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client









    @commands.command(aliases=['j'])
    async def join(self, ctx):

        channel = ctx.message.author.voice.channel

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
            await ctx.send(f'Bot has been moved to {channel}')
        else:
            voice = await channel.connect()
            await ctx.send(f'Bot has joined {channel}')

    @commands.command(aliases=['l', 'dc'])
    async def leave(self, ctx):

        channel = ctx.message.author.voice.channel

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():

            await voice.disconnect()
            await ctx.send(f'Left {channel}')
        else:
            await ctx.send(f'I\'m not in a voice channel :thinking:')



    @commands.command()
    async def play(self, ctx, url: str):

        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                #print('removed old song')
        except PermissionError:
            #print('tried to delete song but is currently playing')
            await ctx.send('stahp the music before doing another one')
            return

        await ctx.send('Getting things ready now')


        async with ctx.typing():
            voice = get(self.client.voice_clients, guild=ctx.guild)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                #print("Downloading audio now\n")
                ydl.download([url])

            for file in os.listdir("././"):
                if file.endswith(".mp3"):
                    name = file
                    #print(f"Renamed File: {file}\n")
                    os.rename(file, "song.mp3")

            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.5

        await ctx.send('playing now')















def setup(client):
    client.add_cog(Music(client))
