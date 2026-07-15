from sqlalchemy import (Column, Integer, String, Float, ForeignKey, Table, UniqueConstraint)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import VARCHAR

Base = declarative_base()

package_truck = Table(
    "package_truck",
    Base.metadata,
    Column("package_id", Integer, ForeignKey("packages.id"), primary_key=True),
    Column("truck_id", Integer, ForeignKey("trucks.id"), primary_key=True)
)

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)

    packages = relationship("Package", back_populates="warehouse")

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_code = Column(String(50), nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    warehouse = relationship("Warehouse", back_populates="packages")

    waybill = relationship("Waybill", back_populates="package", uselist=False)
    
    trucks = relationship(
        "Truck",
        secondary=package_truck,
        back_populates="packages"
    )

class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String(100), nullable=False)
    shipping_status = Column(String(50), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id"), unique=True, nullable=False)

    package = relationship("Package", back_populates="waybill")

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    license_plate = Column(String(20), nullable=False)

    packages = relationship(
        "Package",
        secondary=package_truck,
        back_populates="trucks"
    )
