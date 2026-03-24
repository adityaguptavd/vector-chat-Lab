from app.core.utils.id_generator import IDGenerator


class Document:

    def __init__(
        self,
        id: str,
        user_id: str,
        filename: str,
        content_hash: str,
    ) -> None:
        self.__id = id
        self.__user_id = user_id
        self.__filename = filename
        self.__content_hash = content_hash

    @classmethod
    def create(
        cls,
        user_id: str,
        filename: str,
        content_hash: str,
    ) -> "Document":
        return cls(
            id=IDGenerator.generate(prefix="doc"),
            user_id=user_id,
            filename=filename,
            content_hash=content_hash,
        )

    @property
    def id(self) -> str:
        return self.__id

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def content_hash(self) -> str:
        return self.__content_hash

    def _set_id(self, id: str) -> None:
        self.__id = id

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.__id,
            "user_id": self.__user_id,
            "filename": self.__filename,
            "content_hash": self.__content_hash,
        }