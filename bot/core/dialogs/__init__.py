from aiogram import Router
from aiogram_dialog import setup_dialogs

from .main import router as main_router

router = Router()
router.include_router(main_router)

setup_dialogs(router=router)
