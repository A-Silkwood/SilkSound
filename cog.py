from discord.ext import commands
from stringcase import titlecase

import utils as u


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _fname(self):
        return f".{self.name}" if self.name is not None else ""

    def _fdata(self, data: dict = {}):
        # no data to format
        if len(data) == 0:
            return ""

        # add each key pair to string
        data_str = ": ["
        for key, val in data.items():
            data_str = f"{data_str} {titlecase(key)} ({val})"

        return data_str + " ]"

    def debug(self, msg: str, data: dict = {}):
        u.logger.debug(f"{self._fname()}: {msg}{self._fdata(data)}")

    def info(self, msg: str, data: dict = {}):
        u.logger.info(f"{self._fname()}: {msg}{self._fdata(data)}")

    def warning(self, msg: str, data: dict = {}):
        u.logger.warning(f"{self._fname()}: {msg}{self._fdata(data)}")

    def error(self, msg: str, data: dict = {}):
        u.logger.error(f"{self._fname()}: {msg}{self._fdata(data)}")

    def critical(self, msg: str, data: dict = {}):
        u.logger.critical(f"{self._fname()}: {msg}{self._fdata(data)}")
