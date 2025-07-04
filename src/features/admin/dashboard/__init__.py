from fastapi import APIRouter

from ....shared.services.routers.utils import *
from .api_models import *


dashboard_router = APIRouter(prefix="/dashboard", tags=["Admin"])


@dashboard_router.get(
    "/",
    name="Get dashboard statistics",
    responses={
        HTTP_200_OK: {
            "model": DashboardResponse,
            "description": "Dashboard statistics returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid token, login first.",
        },
    },
)
async def dashboard(_: Session = get_session) -> DashboardResponse:
    all_trucks = Trucks.count
    all_loads = Loads.count
    all_users = Users.count_documents({"active": True})

    # for user in Users.find():
    #     user: User
    #     if not user.membership:
    #         user.membership = "Normal"
    #         user.save()

    return DashboardResponse(
        detail="Dashboard statistics returned successfully.",
        dashboard=Dashboard(
            values=[
                Value(name="All users", value=all_users),
                Value(name="Active Users", value=len(Sessions.values())),
                Value(name="Available Trucks", value=all_trucks),
                Value(name="Available Loads", value=all_loads),
            ],
            membership=Membership(
                dispatchers=[
                    Member(
                        name="elite",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Elite",
                                user_type="dispatcher",
                            )
                        ),
                    ),
                    Member(
                        name="essential",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Essential",
                                user_type="dispatcher",
                            )
                        ),
                    ),
                    Member(
                        name="premium",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Premium",
                                user_type="dispatcher",
                            )
                        ),
                    ),
                    Member(
                        name="normal",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Normal",
                                user_type="dispatcher",
                            )
                        ),
                    ),
                ],
                owners=[
                    Member(
                        name="elite",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Elite",
                                user_type="owner",
                            )
                        ),
                    ),
                    Member(
                        name="essential",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Essential",
                                user_type="owner",
                            )
                        ),
                    ),
                    Member(
                        name="premium",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Premium",
                                user_type="owner",
                            )
                        ),
                    ),
                    Member(
                        name="normal",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Normal",
                                user_type="owner",
                            )
                        ),
                    ),
                ],
                carriers=[
                    Member(
                        name="elite",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Elite",
                                user_type="carrier",
                            )
                        ),
                    ),
                    Member(
                        name="essential",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Essential",
                                user_type="carrier",
                            )
                        ),
                    ),
                    Member(
                        name="premium",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Premium",
                                user_type="carrier",
                            )
                        ),
                    ),
                    Member(
                        name="normal",
                        value=Users.count_documents(
                            dict(
                                active = True,
                                membership="Normal",
                                user_type="carrier",
                            )
                        ),
                    ),
                ],
                # dispatchers=Dispatchers(
                #     elite=Users.count_documents(
                #         dict(
                #             membership="Elite",
                #             user_type="dispatcher",
                #         )
                #     ),
                #     essential=Users.count_documents(
                #         dict(
                #             membership="Essential",
                #             user_type="dispatcher",
                #         )
                #     ),
                #     premium=Users.count_documents(
                #         dict(
                #             membership="Premium",
                #             user_type="dispatcher",
                #         )
                #     ),
                #     normal=Users.count_documents(
                #         dict(
                #             membership="Normal",
                #             user_type="dispatcher",
                #         )
                #     ),
                # ),
                # owners=Owners(
                #     elite=Users.count_documents(
                #         dict(
                #             membership="Elite",
                #             user_type="owner",
                #         )
                #     ),
                #     essential=Users.count_documents(
                #         dict(
                #             membership="Essential",
                #             user_type="owner",
                #         )
                #     ),
                #     premium=Users.count_documents(
                #         dict(
                #             membership="Premium",
                #             user_type="owner",
                #         )
                #     ),
                #     normal=Users.count_documents(
                #         dict(
                #             membership="Normal",
                #             user_type="owner",
                #         )
                #     ),
                # ),
                # carriers=Carriers(
                #     elite=Users.count_documents(
                #         dict(
                #             membership="Elite",
                #             user_type="carrier",
                #         )
                #     ),
                #     essential=Users.count_documents(
                #         dict(
                #             membership="Essential",
                #             user_type="carrier",
                #         )
                #     ),
                #     premium=Users.count_documents(
                #         dict(
                #             membership="Premium",
                #             user_type="carrier",
                #         )
                #     ),
                #     normal=Users.count_documents(
                #         dict(
                #             membership="Normal",
                #             user_type="carrier",
                #         )
                #     ),
                # ),
            ),
        ),
    )
