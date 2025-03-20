import pandas as pd

from core import SessionLocal
from models.models import BuildingsOrm, OrganizationsOrm, ActivitiesOrm, OrganizationsActivitiesOrm

data_from_file = pd.read_excel("data.xlsx", sheet_name=None)

with SessionLocal() as session:
    for row_id, row_data in data_from_file['Buildings'].iterrows():
        item = BuildingsOrm(
            address=row_data["Address"],
            latitude=row_data["Latitude"],
            longitude=row_data["Longitude"]
        )
        session.add(item)

    session.commit()

    for row_id, row_data in data_from_file['Organizations'].iterrows():
        item = OrganizationsOrm(
            name=row_data["name"],
            phone=row_data["phone"],
            building_fk=row_data["building_fk"]
        )
        session.add(item)

    session.commit()

    for row_id, row_data in data_from_file['Activities'].iterrows():
        item = ActivitiesOrm(
            name=row_data["name"],
            parent_id=None if pd.isna(row_data["parent_id"]) else row_data["parent_id"]
        )
        session.add(item)

    session.commit()

    for row_id, row_data in data_from_file['Organizations_Activities'].iterrows():
        item = OrganizationsActivitiesOrm(
            organization_fk=int(row_data["org_fk"]),
            activity_fk=int(row_data["active_fk"])
        )
        session.add(item)

    session.commit()
