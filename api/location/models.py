from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class CountryModel(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(10), nullable=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationship: one country has many states
    states = relationship("StateModel", back_populates="country", cascade="all, delete")


class StateModel(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("country.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationship: one state belongs to one country
    country = relationship("CountryModel", back_populates="states")
    # Relationship: one state has many cities
    cities = relationship("CityModel", back_populates="state", cascade="all, delete")


class CityModel(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state_id = Column(Integer, ForeignKey("state.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationship: one city belongs to one state
    state = relationship("StateModel", back_populates="cities")
