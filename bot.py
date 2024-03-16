import discord
from discord.ext import commands


@commands.command()
async def ping(ctx):
    await ctx.send("pong")


def create_client() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)
    client.add_command(ping)

    return client
