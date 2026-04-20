__version__ = (1, 0, 0)
# name: TestModule
# author: unnic
# meta developer: @HikkTutor
# meta banner: https://i.imgur.com/4M7IWwP.png  # необязательно, пример баннера

from .. import loader

@loader.tds
class TestTTTModule(loader.Module):
    """Тестовый модуль для проверки AutoPost"""

    @loader.command()
    async def testcmd(self, message):
        await message.reply("OK")
