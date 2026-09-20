from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Hotel(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    users = relationship("User", back_populates="hotel")
    employees = relationship("Employee", back_populates="hotel")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(40), default="training_manager")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    hotel = relationship("Hotel", back_populates="users")

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    employee_code: Mapped[str] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(String(160))
    department: Mapped[str] = mapped_column(String(120), default="")
    role: Mapped[str] = mapped_column(String(120), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    hotel = relationship("Hotel", back_populates="employees")

class TrainingProgram(Base):
    __tablename__ = "training_programs"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    training_type: Mapped[str] = mapped_column(String(50), default="Off-Job")
    hours: Mapped[float] = mapped_column(Float, default=0)

class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    program_id: Mapped[int] = mapped_column(ForeignKey("training_programs.id"))
    date: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="Present")
    hours: Mapped[float] = mapped_column(Float, default=0)

class Evaluation(Base):
    __tablename__ = "evaluations"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    program_id: Mapped[int] = mapped_column(ForeignKey("training_programs.id"))
    reaction: Mapped[float] = mapped_column(Float, default=0)
    pre_score: Mapped[float] = mapped_column(Float, default=0)
    post_score: Mapped[float] = mapped_column(Float, default=0)

class Certificate(Base):
    __tablename__ = "certificates"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    program_id: Mapped[int] = mapped_column(ForeignKey("training_programs.id"))
    issue_date: Mapped[str] = mapped_column(String(20))
    expiry_date: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="Active")

class TrainingCost(Base):
    __tablename__ = "training_costs"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    item: Mapped[str] = mapped_column(String(180))
    department: Mapped[str] = mapped_column(String(120), default="")
    planned: Mapped[float] = mapped_column(Float, default=0)
    actual: Mapped[float] = mapped_column(Float, default=0)
