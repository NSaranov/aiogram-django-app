import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.apps.core.bot.handlers import router as core_router
from app.apps.core.data_bot import CORE_DATA_BOT
from app.config.bot import RUNNING_MODE, RunningMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dispatcher = Dispatcher()
bots = []


def _register_routers() -> None:
    dispatcher.include_router(core_router)


async def _set_bot_commands() -> None:
    global bots
    for _bot in bots:
        await _bot.set_my_commands(
            [
                BotCommand(command="/export", description="Экспорт данных в excel-файл"),
            ]
        )


@dispatcher.startup()
async def on_startup() -> None:
    # Register all routers
    _register_routers()

    # # Set default commands
    await _set_bot_commands()


def run_polling() -> None:
    global bots
    bots = []
    for _bot in CORE_DATA_BOT.get_bots_from_db():
        print(_bot)
        if _bot["bot_on"] is True:
            bots.append(Bot(_bot["id"], parse_mode="HTML"))
    dispatcher.run_polling(*bots)


def run_webhook() -> None:
    raise NotImplementedError("Webhook mode is not implemented yet")


if __name__ == "__main__":
    if RUNNING_MODE == RunningMode.LONG_POLLING:
        run_polling()

    elif RUNNING_MODE == RunningMode.WEBHOOK:
        run_webhook()
    else:
        raise RuntimeError(f"Unknown running mode: {RUNNING_MODE}")
