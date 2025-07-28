from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.kbd import Button, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format

from bot.core.states import MainSG
from web.panel.models import User

router = Router()


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager, user: User):
    user.data['count'] = 1
    await user.asave()

    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)


async def get_data(dialog_manager: DialogManager, user: User, **kwargs):
    return {"user": user}


async def on_click(callback: CallbackQuery, button: Button, manager: DialogManager):
    user = manager.middleware_data['user']
    user.data['count'] += 1
    await user.asave()


dialog = Dialog(
    Window(
        Format('{user.data[count]}'),
        Button(text=Const('+1'), id='btn_plus', on_click=on_click),
        state=MainSG.main,
        getter=get_data
    ),
)

router.include_router(dialog)
