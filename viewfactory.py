from viewbuilder import ViewBuilder
from discord.ui import View


class ViewFactory:

    def empty() -> View:
        return ViewBuilder().view()

    def start(lobby_id: str) -> View:
        return ViewBuilder().add_buton("Start", f"start_{lobby_id}", _start).view()


async def _start(interaction):
    print("FUCK THIS SHIT I AM OUT")
