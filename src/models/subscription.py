from .model import *


class Subscription(Model):
    def __init__(
        self,
        models: "Subscriptions",
        *,
        subcription_id: str,
        customer: str,
        user_id: str,
        package: str,
        currency: str,
        **kwargs,
    ) -> None:
        super().__init__(models, **kwargs)

        self.subcription_id = subcription_id
        self.customer = customer
        self.user_id = user_id
        self.package = package
        self.currency = currency


class Subscriptions(Models):
    model_class = Subscription


Subscriptions = Subscriptions()
