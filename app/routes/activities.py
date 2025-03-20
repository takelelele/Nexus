from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from databases.nexus_db import get_db
from services.services import add_activity

router = APIRouter()

@router.post("/add_activity")
async def new_activity(activity_name: str, parent_id: int = None, db: Session = Depends(get_db)):
    return await add_activity(activity_name, parent_id, db)