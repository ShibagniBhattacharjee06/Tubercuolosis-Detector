from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from src.database import Base
from sqlalchemy import TypeDecorator, CHAR, Enum
import uuid


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Patient(Base):
    __tablename__ = "patients"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('male', 'female', 'other',
                    name='gender_types'), nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    doctor_id = Column(GUID(),
                       ForeignKey("users.id"), nullable=False)
    doctor = relationship("User", back_populates="patients")
    records = relationship("PatientRecord", back_populates="patient")

    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)


class PatientRecord(Base):
    __tablename__ = "patient_records"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    patient_id = Column(GUID(),
                        ForeignKey("patients.id"), nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    checkup_data = Column(Text, nullable=True)
    condition = Column(Text, nullable=True)
    patient = relationship("Patient", back_populates="records")
    image_path = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)


patients = Patient.__table__
records = PatientRecord.__table__
