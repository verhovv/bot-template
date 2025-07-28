from aiogram import Router

from bot.core.middlewares import UserMiddleware
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

router = Router()
router.callback_query.outer_middleware(CallbackAnswerMiddleware())
router.callback_query.outer_middleware(UserMiddleware())
router.message.outer_middleware(UserMiddleware())
