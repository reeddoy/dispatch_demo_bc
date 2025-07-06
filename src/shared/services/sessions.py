import time
from ...constants.config import LOGGER, SESSION_TIMEOUT
from ...shared.utils.commons import run_on_thread
from ...models import *
from ..utils.base import Child, SingletonManager
from ..utils.commons import get_timestamp, hash_data
from .mail.otp import OTP, ResetOTP


class Session(Child):
    def __init__(self, user: User):
        super().__init__(user.id)

        self.user = user
        self.client = Client(self, user)

    @property
    def valid(self) -> bool:
        return (
            self.alive
            and (get_timestamp() - self.modified_timestamp) <= SESSION_TIMEOUT
        )

    @property
    def online(self) -> bool:
        return self.client.online

    def attach_websocket(self, sid: str):
        self.client.set_sid(sid)

    def set_sid(self, sid: str):
        self.client.set_sid(sid)

    def remove_sid(self, sid: str):
        self.client.remove_sid(sid)

    def kill(self):
        self.client.kill()
        super().kill()

    def __str__(self):
        return f"Session(id={self.id}, sid={self.client.sid}, userId={self.user.id}, email={self.user.email}, username={self.user.user_name}, name={self.user.first_name} {self.user.last_name})"

    async def emit(self, *args):
        return await self.client.emit(*args)


class Client(Child):
    def __init__(
        self,
        session: Session,
        user: User,
    ):
        super().__init__()

        self.user = user
        self.session = session
        self.otp = OTP(user)

        self.sids: set[str] = set()

    @property
    def sid(self) -> str:
        return str(self.sids)

    @property
    def verified(self) -> bool:
        return self.user.verified

    @property
    def online(self) -> bool:
        return bool(self.sids)

    # @modifier
    def send_otp(self) -> bool:
        return self.otp.send_otp()

    def verify_otp(self, otp: int) -> bool:
        valid = self.otp.verify(otp)
        if valid:
            self.user.verified = True
            self.user.save()
        return valid

    def set_sid(self, sid: str):
        self.sids.add(sid)

    def remove_sid(self, sid: str):
        if sid in self.sids:
            self.sids.remove(sid)

    def kill(self):
        self.otp.kill()
        super().kill()

    async def emit(self, callback):
        for sid in self.sids:
            return await callback(sid)


class Sessions(SingletonManager):
    def __init__(self):
        super().__init__()

        self.session_emails: dict[str, Session] = {}
        self.session_users_ids: dict[str, Session] = {}
        self.reset_otps: dict[str, ResetOTP] = {}
        self.sids: dict[str, Session] = {}

        self.clearing_reset_passwords = False
        self.started = False

    def set_session_sid(self, sid: str, session: Session):
        session.set_sid(sid)
        self.sids[sid] = session

    def remove_session_sid(self, sid: str) -> Session:
        if session := self.sids.get(sid):
            session.remove_sid(sid)
            del self.sids[sid]
            return session

    def create_session(self, user: User) -> None | Session:
        session = self.get_by_user_id(user.id) or Session(user)
        child = self.add_child(session)
        if child:
            return session

    def add_child(self, session: Session) -> bool:
        if super().add_child(session):
            self.session_emails[session.user.email] = session
            self.session_users_ids[session.user.id] = session
            return session

    def remove_child(self, session: Child) -> bool:
        if super().remove_child(session):
            if session.user.email in self.session_emails:
                del self.session_emails[session.user.email]

            if session.user.id in self.session_users_ids:
                del self.session_users_ids[session.user.id]

    def get_by_email(self, email: str) -> None | Session:
        return self.session_emails.get(email)

    def get_by_user_id(self, user_id: str) -> None | Session:
        return self.session_users_ids.get(user_id)

    def get_by_customer_id(self, customer_id: str) -> None | Session:
        filtered = list(
            filter(
                lambda session: session.user.customer_id == customer_id,
                self.session_emails.values(),
            )
        )

        if filtered:
            return filtered[0]

    def set_reset_password(self, email: str) -> None | ResetOTP:
        user = Users.get_one("email", email)

        if user:
            reset_otp = ResetOTP(user)
            self.reset_otps[email.lower()] = reset_otp

            # if not self.clearing_reset_passwords:
            #     run_on_thread(self.clear_reset_passwords)

            return reset_otp

    def reset_password(
        self,
        email: str,
        password: str,
        otp: str,
    ) -> bool:
        if email in self.reset_otps:
            rpass = self.reset_otps[email]
            if rpass.reset(password, otp):
                del self.reset_otps[email]
                return True
        return False


    def clear_reset_passwords_once(self):
        reset_otps = list(self.reset_otps.values())
        for reset_otp in reset_otps:
            if not reset_otp.valid:
                del self.reset_otps[reset_otp.id]

    def start_periodic_reset_password_cleanup(self, interval=60):
        if self.clearing_reset_passwords:
            return
        self.clearing_reset_passwords = True
        def cleanup():
            while self.alive and self.clearing_reset_passwords:
                self.clear_reset_passwords_once()
                time.sleep(interval)
            self.clearing_reset_passwords = False
        run_on_thread(cleanup)

    def clear_sessions_once(self):
        sessions: list[Session] = self.values()
        for session in sessions:
            if not session.valid:
                session.kill()
                LOGGER.info(f"Session Timeout :: {session.user.email}")
                self.remove_child(session)

    def start_periodic_session_cleanup(self, interval=60):
        if self.started:
            return
        self.started = True
        LOGGER.info(f"Started periodic validating {self.__class__.__name__}")
        def cleanup():
            while self.alive and self.started:
                self.clear_sessions_once()
                time.sleep(interval)
            self.started = False
            LOGGER.info(f"Ended periodic validating {self.__class__.__name__}\n")
        run_on_thread(cleanup)

    def kill(self):
        reset_otps = self.reset_otps.values()
        for reset_otp in reset_otps:
            reset_otp.kill()

        sessions = self.children.values()
        for session in sessions:
            session.kill()
        return super().kill()


Sessions = Sessions()
