from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def encrypt(password: str) -> str:
        """
        Hash the given password using bcrypt.
        """
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a hashed password.
        """
        return pwd_cxt.verify(plain_password, hashed_password)
