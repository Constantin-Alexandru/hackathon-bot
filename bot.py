import discord
from discord.ext import commands
from command import create_command, CommandType


@commands.command()
async def ping(ctx):
    await ctx.send("pong")


@commands.command()
async def create(ctx):
    user_id = ctx.author.id
    command = create_command(CommandType.COMMAND_CREATE, user_id)


@commands.command()
async def join(ctx, session_id: str):
    user_id = ctx.author.id
    command = create_command(CommandType.COMMAND_JOIN, user_id, session_id)


@commands.command()
async def leave(ctx):
    user_id = ctx.author.id
    command = create_command(CommandType.COMMAND_LEAVE, user_id)


@commands.command()
async def join(ctx):
    user_id = ctx.author.id
    command = create_command(CommandType.COMMAND_START, user_id)


async def send_message(user_id: int, message: str) -> None:
    try:
        user = await client.fetch_user(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        if not user.dm_channel:
            try:
                dm_channel = await user.create_dm()
            except discord.HTTPException:
                raise discord.HTTPException(
                    f"Failed to create DM channel for user {user.name}"
                )
        else:
            dm_channel = user.dm_channel

        await dm_channel.send(message)

    except (discord.HTTPException, ValueError) as e:
        print(f"Error sending DM: {e}")


def create_client() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)
    client.add_command(ping)

    return client


client = create_client()
