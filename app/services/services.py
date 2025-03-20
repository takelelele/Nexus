from sqlalchemy import select, func
from sqlalchemy.orm import Session, aliased

from models.models import OrganizationsOrm, BuildingsOrm, ActivitiesOrm


async def get_orgs_by_build(building_id: int, db: Session):
    return db.query(OrganizationsOrm).filter(OrganizationsOrm.building_fk == building_id).all()


async def get_orgs_by_activity(activity_id: int, db: Session):
    query = (select(OrganizationsOrm).join(OrganizationsOrm.activities).where(ActivitiesOrm.id == activity_id))
    return db.execute(query).scalars().all()


async def get_org_by_id(org_id: int, db: Session):
    stmt = (
        select(
            OrganizationsOrm.id,
            OrganizationsOrm.name,
            OrganizationsOrm.phone,
            BuildingsOrm.address.label("address")
        )
        .join(OrganizationsOrm.building)
        .filter(OrganizationsOrm.id == org_id)
    )
    return db.execute(stmt).mappings().all()


async def get_org_by_activities_tree(activity_id: int, db: Session):
    activity_alias = aliased(ActivitiesOrm)

    cte = (
        select(
            ActivitiesOrm.id
        )
        .where(ActivitiesOrm.id == activity_id)
        .cte(recursive=True)
    )

    cte = cte.union_all(
        select(activity_alias.id)
        .where(activity_alias.parent_id == cte.c.id)
    )

    query = (
        select(
            OrganizationsOrm.name,
            OrganizationsOrm.phone,
            BuildingsOrm.address.label("address"),
            ActivitiesOrm.name.label("activity")
        )
        .join(OrganizationsOrm.activities)
        .join(OrganizationsOrm.building)
        .where(ActivitiesOrm.id.in_(select(cte.c.id)))
        .distinct()
    )

    return db.execute(query).mappings().all()


async def get_org_by_name(org_name: str, db: Session):
    return db.execute(select(OrganizationsOrm).where(OrganizationsOrm.name.ilike(f"%{org_name}%"))).scalars().all()


def get_nesting_level(parent_id, db: Session):
    if parent_id is None:
        return 0

    cte = (
        db.query(ActivitiesOrm.id, ActivitiesOrm.parent_id)
        .filter(ActivitiesOrm.id == parent_id)
        .cte(recursive=True)
    )

    cte = cte.union_all(
        db.query(ActivitiesOrm.id, ActivitiesOrm.parent_id)
        .filter(ActivitiesOrm.id == cte.c.parent_id)
    )

    return db.query(func.count()).select_from(cte).scalar() - 1


async def add_activity(name, parent_id, db: Session):
    if get_nesting_level(parent_id, db) >= 2:
        return "Невозможно создать деятельность с уровнем вложенности более 3"

    new_activity = ActivitiesOrm(name=name, parent_id=parent_id)
    db.add(new_activity)
    db.commit()
    return new_activity.id
