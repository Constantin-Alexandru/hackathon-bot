from viewbuilder import ViewBuilder
from discord.ui import View


class ViewFactory:

    def empty() -> View:
        return ViewBuilder().view()

    def start() -> View:
        return ViewBuilder().add_buton("Start", "start").view()
