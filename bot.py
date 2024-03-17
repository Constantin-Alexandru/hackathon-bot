import discord
from discord.ext import commands
from command import create_command, CommandType
from callbacks import callbacks


def create_client() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)
    client.add_command(ping)
    client.add_command(create)
    client.add_command(start)
    client.add_command(join)
    client.add_command(leave)

    return client


client = create_client()


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
async def start(ctx):
    user_id = ctx.author.id
    command = create_command(CommandType.COMMAND_START, user_id)


async def send_message(
    user_id: int,
    message: discord.Embed,
    buttons: discord.ui.View = discord.ui.View(),
    message_id: int | None = None,
) -> int:

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

        if message_id:
            msg = await dm_channel.fetch_message(message_id)

            await msg.edit(embed=message, view=buttons)

            return msg.id
        else:
            msg = await dm_channel.send(embed=message, view=buttons)
            return msg.id

    except (discord.HTTPException, ValueError) as e:

        print(f"Error sending DM: {e}")
        return -1


@client.event
async def on_button_click(interaction):
    if (
        interaction.type == discord.InteractionType.Button
        and interaction.message.author == client.user
    ):
        pass
