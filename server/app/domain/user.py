from app.core.utils.id_generator import IDGenerator

class User:

    def __init__(self, id: str, email: str, password_hash: str) -> None:
        self.__id = id
        self.__email = email
        self.__password_hash = password_hash

    @classmethod
    def create(cls, email: str, password_hash: str) -> "User":
        return cls(
            id=IDGenerator.generate(prefix="usr"), 
            email=email, 
            password_hash=password_hash
        )

    @property
    def id(self) -> str:
        return self.__id

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    def _set_id(self, id: str) -> None:
        self.__id = id

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.__id,
            "email": self.__email,
            "password_hash": self.__password_hash
        }