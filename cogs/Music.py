import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import asyncio



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}



ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client





    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))











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
    async def pause(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send('Music paused')
        else:
            await ctx.send('No music playing. Try the resume command.')

    @commands.command()
    async def resume(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send('Resuming music')
        else:
            await ctx.send('No music paused. Try the play command.')

    @commands.command()
    async def stop(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)


        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Music stopped')
            #await voice.disconnect()
        else:
            await ctx.send('No music playing.')









def setup(client):
    client.add_cog(Music(client))
