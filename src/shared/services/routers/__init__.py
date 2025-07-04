from fastapi import APIRouter
from ....features.auth import auth_router
from ....features.affiliate import affiliates_router
from ....features.users import users_router
from ....features.reports import reports_router
from ....features.trucks import trucks_router
from ....features.load_referrals import load_referrals_router
from ....features.loads import loads_router
from ....features.admin import admin_router
from ....features.posts import posts_router
from ....features.payment import payment_router
from ....features.chat import chats_router
from ....features.reviews import reviews_router
from ....features.lounge import *
from ....features.lounge.old_init import *
from ....features.notifications import *

from ....features.user_bill_tos import *
from ....features.user_load_tos import *
from ....features.user_drivers import *
from ....features.user_receivers import *
from ....features.user_shippers import *
from ....features.user_trailers import *
from ....features.user_trucks import *


routers = APIRouter()

routers.include_router(auth_router)
# routers.include_router(affiliates_router)
routers.include_router(users_router)
routers.include_router(reports_router)
routers.include_router(trucks_router)
routers.include_router(load_referrals_router)
routers.include_router(loads_router)
routers.include_router(admin_router)
routers.include_router(posts_router)
routers.include_router(payment_router)
routers.include_router(chats_router)
routers.include_router(reviews_router)
routers.include_router(notifications_router)

routers.include_router(user_bill_tos_router)
routers.include_router(user_load_tos_router)
routers.include_router(user_drivers_router)
routers.include_router(user_receivers_router)
routers.include_router(user_shippers_router)
routers.include_router(user_trailers_router)
routers.include_router(user_trucks_router)

routers.include_router(lounge_router)


@routers.get("/")
def root():
    return "Server is Okay"
