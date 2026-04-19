from typing import Type, TypeVar, Generic, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, update, exists
from sqlalchemy.sql import Select

T = TypeVar("T")  # SQLAlchemy Model


class BaseRepository(Generic[T]):

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    # ------------------------
    # 🟢 CREATE
    # ------------------------
    def create(self, instance: T) -> T:
        self.db.add(instance)
        self.db.flush()
        return instance

    # ------------------------
    # 🔍 GET BY ID (SAFE)
    # ------------------------
    def get_by_id(
        self,
        obj_id: str,
        include_deleted: bool = False
    ):
        stmt = select(self.model).where(self.model.id == obj_id)

        if not include_deleted:
            stmt = self._apply_not_deleted(stmt)

        return self._execute_one(stmt)

    # ------------------------
    # 📋 LIST (PAGINATED)
    # ------------------------
    def list(
        self,
        *,
        filters: Dict[str, Any] | None = None,
        page: int = 1,
        limit: int = 10,
        order_by: str | None = None,
    ):
        stmt = select(self.model)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        stmt = self._apply_not_deleted(stmt)
        stmt = self._apply_ordering(stmt, order_by)
        stmt = self._paginate(stmt, page, limit)

        return self._execute(stmt)

    # ------------------------
    # 🔢 COUNT
    # ------------------------
    def count(self, include_deleted: bool = False) -> int:
        stmt = select(func.count()).select_from(self.model)

        if not include_deleted:
            stmt = stmt.where(self.model.is_deleted.is_(False))

        return self.db.execute(stmt).scalar_one()

    # ------------------------
    # 🧼 SOFT DELETE
    # ------------------------
    def soft_delete(self, obj_id: str) -> None:
        obj = self.get_by_id(obj_id, include_deleted=True)

        if not obj:
            return

        obj.is_deleted = True
        obj.deleted_at = func.now()

        self.db.flush()

    # ------------------------
    # ♻️ RESTORE (BONUS)
    # ------------------------
    def restore(self, obj_id: str) -> None:
        obj = self.get_by_id(obj_id, include_deleted=True)

        if not obj:
            return

        obj.is_deleted = False
        obj.deleted_at = None

        self.db.flush()

        # ------------------------
    # 🧼 Apply Soft Delete Filter
    # ------------------------
    def _apply_not_deleted(self, stmt: Select) -> Select:
        return stmt.where(self.model.is_deleted.is_(False))

    # ------------------------
    # 📄 Pagination Helper
    # ------------------------
    def _paginate(self, stmt: Select, page: int, limit: int) -> Select:
        return stmt.offset((page - 1) * limit).limit(limit)

    # ------------------------
    # ⚡ Execute Helpers
    # ------------------------
    def _execute(self, stmt: Select):
        return self.db.execute(stmt).scalars().all()

    def _execute_one(self, stmt: Select):
        return self.db.execute(stmt).scalar_one_or_none()

    def _apply_filters(
        self,
        stmt: Select,
        filters: Dict[str, Any]
    ) -> Select:

        conditions = []

        for field, value in filters.items():
            column = getattr(self.model, field)

            if isinstance(value, list):
                conditions.append(column.in_(value))
            else:
                conditions.append(column == value)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        return stmt
    
    def _apply_ordering(
        self,
        stmt: Select,
        order_by: str | None
    ) -> Select:

        if not order_by:
            return stmt

        desc = order_by.startswith("-")
        field = order_by[1:] if desc else order_by

        column = getattr(self.model, field)

        return stmt.order_by(column.desc() if desc else column.asc())

    def update_fields(
        self,
        obj_id: str,
        updates: dict
    ) -> None:

        if not updates:
            return

        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**updates)
        )

        self.db.execute(stmt)


    def _exists(self, filters: dict) -> bool:
        stmt = select(self.model)

        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_not_deleted(stmt)

        exists_stmt = select(exists(stmt))

        return self.db.execute(exists_stmt).scalar()