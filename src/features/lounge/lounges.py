from ...models.user import User
from ...shared.utils.base import *


class Lounge(Child):
    def __init__(self, creator: User, creator_sid: str, title: str):
        super().__init__(id=creator.id)

        self.creator = creator
        self.creator_sid = creator_sid
        self.title = title

        self.participants: dict[str, User] = {creator.id: creator}
        self.participants_sids: dict[str, str] = {creator_sid: creator.id}
        self.hosts: set[str] = set(self.participants)

    @property
    def details(self) -> dict:
        return dict(
            id=self.id,
            title=self.title,
            participants=len(self.participants),
        )

    def promote_to_host(self, id: str):
        if id in self.participants and id not in self.hosts:
            self.hosts.add(id)

    def demote_to_member(self, id: str):
        if id in self.hosts:
            self.hosts.remove(id)

    def add_participant(self, user: User, sid: str):
        self.participants[user.id] = user
        self.participants_sids[sid] = user.id

    def remove_participant(self, sid: str) -> bool:
        if user_id := self.participants_sids.get(sid):
            del self.participants_sids[sid]
            del self.participants[user_id]
            return True
        return False


class Lounges(SingletonManager):
    def __init__(self):
        super().__init__()

        self.user_invites: dict[str, list[str]] = {}

    def create_lounge(self, user: User, creator_sid: str, title: str) -> Lounge:
        lounge = Lounge(user, creator_sid, title)
        self.add_child(lounge)
        return lounge

    def delete_lounge(self, lounge_id: str):
        if lounge_id in self.children:
            del self.children[lounge_id]


Lounges = Lounges()
