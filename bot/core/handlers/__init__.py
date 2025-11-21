from aiogram import Router

from .start import router as main_router

router = Router()
router.include_router(main_router)
