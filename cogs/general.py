""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import asyncio
import platform
import random
import datetime
from datetime import datetime, timedelta
import requests
from lxml import etree
import aiohttp
import subprocess
import re

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xE02B2B)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(name=i.capitalize(),
                            value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0xE02B2B
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="Krypton#7331",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="discordinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def discordinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0xE02B2B
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xE02B2B
        )
        # await context.send(embed=embed)
        await context.message.delete()
        bot_response = await context.send(embed=embed)
        await asyncio.sleep(2)
        await bot_response.delete()

    @commands.command(name="status", description="Check server status.")
    @checks.not_blacklisted()
    async def status(self, context: commands.Context):
        go_command = ['go', 'run', '.\\steamserverinfo.go', '103.152.197.191', '2303']
        result = subprocess.run(go_command, capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')
        server_info = {}
        for line in output_lines:
            match = re.search(r'(\w+): (.+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                server_info[key] = value

        name = server_info.get("NAME", "")
        players = server_info.get("PLAYERS", "")
        max_players = server_info.get("MAXPLAYERS", "")
        game_map = server_info.get("MAP", "")
        bots = server_info.get("BOTS", "")
        ping = server_info.get("PING", "")

        embed = discord.Embed(
            title='Server Info',
            description=f"Server {name}",
            color=0xE02B2B
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/755342613283864577/a_3441ffd239040b7def59d6f34e1a51d2.webp")
        embed.add_field(
            name="Players",
            value=f'[{players} / {max_players}](https://www.battlemetrics.com/servers/dayz/21395315)'
        )
        embed.add_field(
            name="Latency",
            value=f'Ping [{ping} ms](https://www.battlemetrics.com/servers/dayz/21395315)'
        )
        embed.add_field(
            name="Map",
            value=f'{game_map}'
        )
        embed.set_footer(
            text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} from ReadyIDC Co., Ltd. Server"
        )

        await context.message.delete()
        bot_response = await context.send(embed=embed)

        while True:
            await asyncio.sleep(2)
            result = subprocess.run(go_command, capture_output=True, text=True)
            output_lines = result.stdout.strip().split('\n')
            server_info = {}
            for line in output_lines:
                match = re.search(r'(\w+): (.+)', line)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    server_info[key] = value

            name = server_info.get("NAME", "")
            players = server_info.get("PLAYERS", "")
            max_players = server_info.get("MAXPLAYERS", "")
            game_map = server_info.get("MAP", "")
            bots = server_info.get("BOTS", "")
            ping = server_info.get("PING", "")

            embed.description = f"Server {name}"
            embed.set_field_at(index=0, name="PLayers", value=f'[{players} / {max_players}](https://www.battlemetrics.com/servers/dayz/21395315)')
            embed.set_field_at(index=1, name="Latency", value=f'Ping [{ping} ms](https://www.battlemetrics.com/servers/dayz/21395315)')
            embed.set_field_at(index=2, name="Map", value=f'{game_map}')
            embed.set_footer(
                text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} from ReadyIDC Co., Ltd. Server"
            )
            await bot_response.edit(embed=embed)

    @commands.hybrid_command(
        name="restart",
        description="Check Reaemed server restart time",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        embed = discord.Embed(
            title="Server Restarts",
            description=f"Server restarts occur every four hours on Rearmed, to improve server performance and player stability.",
            color=0xE02B2B
        )
        embed.add_field(
            name="Restart time",
            value="",
            inline=False
        )
        embed.add_field(
            name="",
            value="offline 00:58:00 | online 1:00:15 \u200B",
            inline=False
        )
        embed.add_field(
            name="",
            value="offline 04:58:00 | online 05:00:15 \u200B",
            inline=False
        )
        embed.add_field(
            name="",
            value="offline 08:58:00 | online 09:00:15 \u200B",
            inline=False
        )
        embed.add_field(
            name="",
            value="offline 12:58:00 | online 013:00:15 \u200B",
            inline=False
        )
        embed.add_field(
            name="",
            value="offline 16:58:00 | online 017:00:15 \u200B",
            inline=False
        )
        embed.add_field(
            name="",
            value="offline 20:58:00 | online 021:00:15 \u200B",
            inline=False
        )
        await context.message.delete()
        await context.send(embed=embed)

    @commands.command(
            name="time"
            )
    @checks.not_blacklisted()
    async def time(self, context: Context) -> None:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        embed = discord.Embed(
            title="Time",
            description=f"Bangkok time: {current_time}",
            color=0xE02B2B
        )
        await context.message.delete()
        bot_response = await context.send(embed=embed)
        await asyncio.sleep(2)
        await bot_response.delete()


    @commands.command(name="clear")
    @checks.not_blacklisted()
    async def clear_messages(self, context: Context):
        channel = context.channel
        await channel.purge()
        bot_response = await context.send("All messages have been cleared.")
        await asyncio.sleep(2)
        await bot_response.delete()
        

    @commands.hybrid_command(
        name="invitebot",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @checks.not_blacklisted()
    async def invitebot(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="codelock",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    @checks.not_blacklisted()
    async def codelock(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"-> 1!! -> root | a1! |",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            bot_response = await context.send("I sent you a private message!")
            await context.message.delete()
            await asyncio.sleep(2)
            await bot_response.delete()
        except discord.Forbidden:
            await context.message.delete()
            bot_response = await context.send(embed=embed)
            await asyncio.sleep(2)
            await bot_response.delete()

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    @checks.not_blacklisted()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Server invite [link](https://discord.gg/FTm5CJH7ZM).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            bot_response = await context.send("I sent you a private message!")
            await context.message.delete()
            await asyncio.sleep(2)
            await bot_response.delete()
        except discord.Forbidden:
            await context.message.delete()
            bot_response = await context.send(embed=embed)
            await asyncio.sleep(2)
            await bot_response.delete()

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @checks.not_blacklisted()
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xE02B2B
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0xE02B2B
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
