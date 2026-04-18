from app.core.utils.id_generator import IDGenerator

class User:

    def __init__(self, id: str, email: str, password_hash: str, full_name: str | None = None) -> None:
        self.__id = id
        self.__email = email
        self.__full_name = full_name
        self.__password_hash = password_hash

    @classmethod
    def create(cls, email: str, password_hash: str, full_name: str | None = None) -> "User":
        return cls(
            id=IDGenerator.generate(prefix="usr"), 
            email=email, 
            full_name=full_name,
            password_hash=password_hash
        )

    @property
    def id(self) -> str:
        return self.__id

    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    def _set_id(self, id: str) -> None:
        self.__id = id

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.__id,
            "full_name": self.__full_name,
            "email": self.__email,
            "password_hash": self.__password_hash
        }