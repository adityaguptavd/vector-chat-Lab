from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.deps import get_uow
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "users router working"}

@router.get("/debug")
def debug(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> Dict[str, Any]:
    with uow:
        users = uow.user_repo.get_by_email("debug@example.com")
    return { "count": len(users) if users else 0 }