from fastapi import APIRouter
from .users import users_router
from .coupons import coupons_router
from .dashboard import dashboard_router
from .reports import reports_router
from .email import email_router

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
admin_router.include_router(users_router)
admin_router.include_router(coupons_router)
admin_router.include_router(dashboard_router)
admin_router.include_router(reports_router)
admin_router.include_router(email_router)
