from discord.ext import commands

import utils as u


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_debug(self, message):
        u.logger.debug(f"{f'.{self.name}' if self.name is not None else ''}: {message}")

    def log_info(self, message):
        u.logger.info(f"{f'.{self.name}' if self.name is not None else ''}: {message}")

    def log_warning(self, message):
        u.logger.warning(
            f"{f'.{self.name}' if self.name is not None else ''}: {message}"
        )

    def log_error(self, message):
        u.logger.error(f"{f'.{self.name}' if self.name is not None else ''}: {message}")

    def log_critical(self, message):
        u.logger.critical(
            f"{f'.{self.name}' if self.name is not None else ''}: {message}"
        )
