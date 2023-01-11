import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from echo.settings import TELEGRAM_KEY
from aiogram import Bot, Dispatcher

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from api.models import Token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_KEY)

dp = Dispatcher(bot, storage=MemoryStorage())


class TokenState(StatesGroup):
    token = State()


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=["follow"])
async def get_follow(massage: types.Message):
    await TokenState.token.set()
    await massage.reply("Введите токен: ")


def get_token_model(token: str) -> Token | None:
    try:
        return Token.objects.get(token=token)
    except ObjectDoesNotExist:
        return None


def change_token(token: Token, user_id: int) -> None:
    token.telegram_id = user_id
    token.save()


@dp.message_handler(state=TokenState.token)
async def process_token(message: types.Message, state: FSMContext):
    token = await sync_to_async(get_token_model)(message.text)
    if token is None:
        return await message.reply(
            "Токен введен не правильно или срок действия истек(30дн)"
        )
    await sync_to_async(change_token)(token, message.from_id)
    await message.reply("Токен был подписан!.")
    await state.finish()


async def send_message(user_id: int, user_name, massage: str):
    msg = f"{user_name}, я получил от тебя сообщение:\n {massage}"
    await bot.send_message(user_id, msg)
