from aiogram import Router
from aiogram.enums import ChatType
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot.core.filters import ChatTypeFilter
from bot.core.middlewares import UserMiddleware

router = Router()
router.callback_query.outer_middleware(CallbackAnswerMiddleware())
router.callback_query.outer_middleware(UserMiddleware())
router.message.outer_middleware(UserMiddleware())
router.message.filter(ChatTypeFilter(ChatType.PRIVATE))
