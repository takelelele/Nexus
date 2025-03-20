from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from databases.nexus_db import get_db
from services.services import get_orgs_by_build, get_orgs_by_activity, get_org_by_id, get_org_by_activities_tree, \
    get_org_by_name, add_activity

router = APIRouter()

@router.get("/by_building/{building_id}")
async def org_by_building(building_id: int, db: Session = Depends(get_db)):
    return await get_orgs_by_build(building_id, db)

@router.get("/by_activity/{activity_id}")
async def org_by_activity(activity_id: int, db: Session = Depends(get_db)):
    return await get_orgs_by_activity(activity_id, db)

@router.get("/by_id/{org_id}")
async def org_by_id(org_id: int, db: Session = Depends(get_db)):
    return await get_org_by_id(org_id, db)

@router.get("/by_activity_in_tree/{root_activity_id}")
async def org_by_activity_in_tree(root_activity_id: int, db: Session = Depends(get_db)):
    return await get_org_by_activities_tree(root_activity_id, db)

@router.get("/by_name/{org_name}")
async def org_by_name(org_name: str, db: Session = Depends(get_db)):
    return await get_org_by_name(org_name, db)