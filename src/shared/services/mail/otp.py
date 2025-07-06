import random
from ...utils.commons import get_timestamp, hash_bcrypt, run_on_thread
from ...utils.base import Child, modifier
from ....constants.config import *
from ....models import User
from . import Mail
import time

class OTP(Child):
    def __init__(self, user: User):
        Child.__init__(self, id=user.email)
        self.user = user
        self.otp: int = 0
        self.last_otp_generated_time: int = 0

    @modifier
    def send_otp(self):
        if not self.otp:
            self.generate()
            sent = True
            # sent = Mail.send_otp(
            #     self.user.email,
            #     f"{self.user.first_name} {self.user.last_name}",
            #     self.generate(),
            # )
            LOGGER.info(f"{self.user}: VERIFY OTP generated :: {sent}")
            return sent

    @property
    def verified(self):
        return self.user.verified

    @property
    def valid(self) -> bool:
        return (
            self.verified != True
            and (get_timestamp() - self.modified_timestamp) <= OTP_TIMEOUT
        )

    @property
    def timeout(self) -> int:
        if self.valid:
            return OTP_TIMEOUT - get_timestamp() + self.last_otp_generated_time
        return 0

    @property
    def timeout_formated(self) -> str:
        minutes, seconds = divmod(self.timeout, 60)
        if self.valid:
            return f"{minutes} minutes, {seconds} seconds"
        return 0

    def verify(self, otp: int):
        if otp == self.otp:
            self.user.verified = True
            self.otp = 0
            return self.verified

    def generate(self) -> int:
        random.seed(get_timestamp())
        self.otp = random.randint(1_000, 9_999)

        self.modified()
        self.last_otp_generated_time = self.modified_timestamp

        run_on_thread(self.revoke_otp)
        return self.otp

    def revoke_otp(self):
        while self.alive and self.otp and not self.verified:
            if get_timestamp() - self.last_otp_generated_time >= OTP_TIMEOUT:
                self.otp = 0
                LOGGER.info(f"{self.user}: OTP revoked")
                break
            time.sleep(1)


class ResetOTP(OTP):
    # def __init__(self, user: User):
    #     OTP.__init__(self, user)
    #     self.verified = False

    @modifier
    def send_otp(self):
        if not self.otp:
            sent = True
            self.generate()

            # sent = Mail.send_reset_otp(
            #     self.user.email,
            #     f"{self.user.first_name} {self.user.last_name}",
            #     otp,
            # )
            LOGGER.info(f"{self.user}: RESET OTP generated :: {sent}")
            return sent

    def verify(self, otp: int):
        return otp == self.otp

    def reset(self, password: str, otp: int) -> bool:
        if self.verify(otp):
            self.user.password = hash_bcrypt(password)
            self.user.save()
            return True
