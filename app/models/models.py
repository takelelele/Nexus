from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class OrganizationsOrm(Base):
    __tablename__ = "Organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(20))
    building_fk: Mapped[int] = mapped_column(ForeignKey("Buildings.id"))
    building: Mapped["BuildingsOrm"] = relationship(back_populates="org", uselist=False)
    activities: Mapped[list["ActivitiesOrm"]] = relationship(back_populates="org", uselist=True, secondary="Organizations_Activities")


class BuildingsOrm(Base):
    __tablename__ = "Buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column()
    latitude: Mapped[DECIMAL] = mapped_column(DECIMAL(9, 6))
    longitude: Mapped[DECIMAL] = mapped_column(DECIMAL(9, 6))

    org: Mapped[list["OrganizationsOrm"]] = relationship(back_populates="building", uselist=True)


class ActivitiesOrm(Base):
    __tablename__ = "Activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    parent_id: Mapped[int] = mapped_column(ForeignKey("Activities.id"), nullable=True)

    children: Mapped[list["ActivitiesOrm"]] = relationship(back_populates="parent", remote_side=[parent_id])
    parent: Mapped["ActivitiesOrm"] = relationship(back_populates="children", remote_side=[id])
    org: Mapped["OrganizationsOrm"] = relationship(back_populates="activities", uselist=True, secondary="Organizations_Activities")

class OrganizationsActivitiesOrm(Base):
    __tablename__ = "Organizations_Activities"

    organization_fk: Mapped[int] = mapped_column(ForeignKey("Organizations.id"), primary_key=True)
    activity_fk: Mapped[int] = mapped_column(ForeignKey("Activities.id"), primary_key=True)