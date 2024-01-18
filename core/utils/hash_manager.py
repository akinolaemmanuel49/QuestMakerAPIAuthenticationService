from typing import Optional
from passlib.context import CryptContext

from core.config.env import Env


class HashManager:
    env = Env()
    ENCRYPTION_SCHEMES = env.ENCRYPTION_SCHEMES
    context = CryptContext(ENCRYPTION_SCHEMES)

    def hash_password(self, password: str) -> Optional[str]:
        return self.context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)
