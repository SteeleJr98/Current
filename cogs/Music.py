import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.command(aliases=['j', 'join'])
    async def connect(self, ctx):
        #print('Printing author channel')
        channel = ctx.message.author.voice.channel
        #print(channel)
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
            await ctx.send(f'Bot has been moved to {channel}.')
        else:
            voice = await channel.connect()
            await ctx.send(f'Bot has joined {channel}')

    @commands.command(aliases=['dc', 'l', 'leave'])
    async def disconnect(self, ctx):
        #print('Printing author channel')
        channel = ctx.message.author.voice.channel
        #print(channel)
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            #print('test')
            await voice.disconnect()
            await ctx.send(f'Bot has disconnected from {channel}')
        else:
            await ctx.send('I am not in a voice channel.')





    @commands.command(aliases=['p'])
    async def play(self, ctx, url: str):

        def check_queue():
            Queue_infile = os.path.isdir('././Queue')
            if Queue_infile:
                DIR = os.path.abspath(os.path.realpath('Queue'))
                length = len(os.listdir(DIR))
                still_q  =length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print('No more queued songs')
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
                if length != 0:
                    print('Song done, playing next song.')
                    print(f'Songs still in queue: {still_q}')
                    song_there = os.path.isfile('song.mp3')
                    if song_there:
                        os.remove('song.mp3')
                    shutil.move(song_path, main_location)
                    for file in os.listdir('././'):
                        if file.endswith('.mp3'):
                            os.rename(file, 'song.mp3')
                    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07

                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print('No songs in queue')

        song_there = os.path.isfile("song.mp3")
        #print('Stage One')
        try:
            if song_there:
                #print('Stage Two')
                os.remove('song.mp3')
                queues.clear()
                #print('Removed old song file')
        except PermissionError:
            #print('Trying to delete song file, but it\'s being played')
            await ctx.send('Music already playing. Use the stop command and try again.')
            return

        Queue_infile = os.path.isdir('././Queue')
        try:
            Queue_folder = '././Queue'
            if Queue_infile:
                print('Removed old queue folder')
                shutil.rmtree(Queue_folder)
        except:
            print('No queue old folder')

        await ctx.send('Prepping the jams. Please hold tight.')

        voice = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #print('Downloading audio now')
            ydl.download([url])




        for file in os.listdir('././'):
            if file.endswith('.mp3'):
                name = file
                #print(f"Renamed File: {file}\n")
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-")
        await ctx.send(f'Playing: {nname[0]}-{nname[1]}')
        #print('playing')



    @commands.command(aliases=['pa'])
    async def pause(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send('Music paused')
        else:
            await ctx.send('No music playing. Try the resume command.')

    @commands.command(aliases=['r', 'res'])
    async def resume(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send('Resuming music')
        else:
            await ctx.send('No music paused. Try the play command.')

    @commands.command(aliases=['st'])
    async def stop(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Music stopped')
        else:
            await ctx.send('No music playing. Cannot stop.')

    queues = []

    @commands.command(aliases=['q'])
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir('././Queue')
        if Queue_infile is False:
            os.mkdir('Queue')
        DIR = os.path.abspath(os.path.realpath('Queue'))
        q_num = length(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num
        queue_path = os.path.abspath(os.path.realpath('Queue') + f'\song{q_num}.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #print('Downloading audio now')
            ydl.download([url])
        await ctx.send('Adding some ' + str(q_num) + ' ' ' to the queue')

def setup(client):
    client.add_cog(Music(client))
