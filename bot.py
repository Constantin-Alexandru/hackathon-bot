import discord import DMChannel
from viewbuilder import ViewBuilder
from discord.ext import commands
from command import CreateCommand, JoinCommand, StartCommand, GameCommand
from lobbymanager import LobbyManager
from embedfactory import EmbedFactory
from viewfactory import ViewFactory


@commands.command()
async def ping(ctx):
    await ctx.send("pong")


@commands.command()
async def create(ctx):
    user_id = ctx.author.id

    lobby_id: str = await LobbyManager.process_command(CreateCommand(user_id))

    async def joinLobby(inter: discord.Interaction):
        await LobbyManager.process_command(JoinCommand(inter.member.user.id, lobby_id))
        await inter.message.edit(EmbedFactory.waitForStart(lobby_id, len(LobbyManager.__get_lobby(lobby_id).users.keys())),
            ViewBuilder().add_buton("Join Game", "join", joinLobby))

    if ctx.channel is not DMChannel:
        await ctx.send(
            EmbedFactory.waitForStart(lobby_id, len(LobbyManager.__get_lobby(lobby_id).users.keys())),
            ViewBuilder().add_buton("Join Game", "join", joinLobby)
        )

        

@commands.command()
async def join(ctx, session_id: str):
    user_id = ctx.author.id
    await LobbyManager.process_command(JoinCommand(user_id, session_id))


@join.error
async def join_error(ctx, error):
    user_id = ctx.author.id
    await send_message(
        user_id, EmbedFactory.error("", str(error)), ViewFactory.empty()
    )


def create_client() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)
    client.add_command(ping)
    client.add_command(create)
    client.add_command(join)

    return client


client = create_client()


async def send_message(
    user_id: int,
    message: discord.Embed,
    buttons: discord.ui.View,
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


LobbyManager.set_send_message(send_message)
LobbyManager.set_client(client)


async def add_button():
    res = await client.wait_for()
