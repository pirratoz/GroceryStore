import bcrypt


class Password:
    @staticmethod
    def create(password: str) -> bytes:
        return bcrypt.hashpw(
            password=password.encode("utf-8"),
            salt=bcrypt.gensalt()
        )

    @staticmethod
    def verify(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password
        )
