from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Hotel, User, Employee, TrainingProgram, Attendance, Evaluation, Certificate, TrainingCost
from .auth import hash_password, verify_password, create_token, current_user, require_roles

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Hospitality Academy SaaS API", version="1.0")

class RegisterIn(BaseModel):
    hotel_name: str
    full_name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class EmployeeIn(BaseModel):
    employee_code: str
    name: str
    department: str = ""
    role: str = ""

@app.get("/api/health")
def health():
    return {"ok": True, "service": "hospitality-academy"}

@app.post("/api/auth/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == data.email.lower())):
        raise HTTPException(409, "Email already registered")
    hotel = Hotel(name=data.hotel_name.strip())
    db.add(hotel); db.flush()
    user = User(hotel_id=hotel.id, full_name=data.full_name.strip(), email=data.email.lower(), password_hash=hash_password(data.password), role="owner")
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user), "token_type": "bearer", "hotel_id": hotel.id, "role": user.role}

@app.post("/api/auth/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user), "token_type": "bearer", "hotel_id": user.hotel_id, "role": user.role}

@app.get("/api/auth/me")
def me(user: User = Depends(current_user)):
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "hotel_id": user.hotel_id, "role": user.role}

@app.post("/api/seed")
def seed(db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == "admin@demo-hotel.com"))
    if user:
        return {"message": "Demo already exists", "email": user.email, "password": "Demo123!"}
    hotel = Hotel(name="Demo Grand Hotel")
    db.add(hotel); db.flush()
    user = User(hotel_id=hotel.id, full_name="Demo Training Manager", email="admin@demo-hotel.com", password_hash=hash_password("Demo123!"), role="owner")
    db.add(user); db.flush()
    emps = [Employee(hotel_id=hotel.id, employee_code="EMP-001", name="Ahmed Hassan", department="Front Office", role="Receptionist"),
            Employee(hotel_id=hotel.id, employee_code="EMP-002", name="Sarah Ali", department="F&B", role="Waiter"),
            Employee(hotel_id=hotel.id, employee_code="EMP-003", name="Omar Khaled", department="Housekeeping", role="Room Attendant")]
    db.add_all(emps); db.flush()
    p1=TrainingProgram(hotel_id=hotel.id,name="Guest Complaint Recovery",training_type="Development",hours=6)
    p2=TrainingProgram(hotel_id=hotel.id,name="Food Safety Essentials",training_type="Mandatory",hours=4)
    db.add_all([p1,p2]); db.flush()
    db.add_all([Attendance(hotel_id=hotel.id,employee_id=emps[0].id,program_id=p1.id,date="2026-09-08",status="Present",hours=6),
                Attendance(hotel_id=hotel.id,employee_id=emps[1].id,program_id=p2.id,date="2026-09-10",status="Present",hours=4),
                Evaluation(hotel_id=hotel.id,employee_id=emps[0].id,program_id=p1.id,reaction=4.6,pre_score=62,post_score=88),
                Certificate(hotel_id=hotel.id,employee_id=emps[1].id,program_id=p2.id,issue_date="2026-02-01",expiry_date="2027-02-01"),
                TrainingCost(hotel_id=hotel.id,item="Food Safety Essentials",department="F&B",planned=1800,actual=1800)])
    db.commit()
    return {"message":"Demo seeded","email":"admin@demo-hotel.com","password":"Demo123!"}

@app.get("/api/tenant/employees")
def employees(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = db.scalars(select(Employee).where(Employee.hotel_id == user.hotel_id).order_by(Employee.id)).all()
    return [{"id":x.id,"employee_code":x.employee_code,"name":x.name,"department":x.department,"role":x.role,"active":x.active} for x in rows]

@app.post("/api/tenant/employees")
def add_employee(data: EmployeeIn, db: Session = Depends(get_db), user: User = Depends(require_roles("owner","admin","hr","training_manager"))):
    row=Employee(hotel_id=user.hotel_id, **data.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"employee_code":row.employee_code,"name":row.name,"department":row.department,"role":row.role}

@app.get("/api/tenant/reporting/summary")
def reporting(db: Session = Depends(get_db), user: User = Depends(current_user)):
    attendance = db.scalars(select(Attendance).where(Attendance.hotel_id == user.hotel_id)).all()
    evaluations = db.scalars(select(Evaluation).where(Evaluation.hotel_id == user.hotel_id)).all()
    costs = db.scalars(select(TrainingCost).where(TrainingCost.hotel_id == user.hotel_id)).all()
    present = sum(1 for x in attendance if x.status == "Present")
    hours = sum(float(x.hours or 0) for x in attendance)
    avg_reaction = round(sum(float(x.reaction or 0) for x in evaluations) / len(evaluations), 2) if evaluations else 0
    planned = sum(float(x.planned or 0) for x in costs)
    actual = sum(float(x.actual or 0) for x in costs)
    return {"employees": db.scalar(select(func.count(Employee.id)).where(Employee.hotel_id == user.hotel_id)) or 0,
            "attendance_rate": round(present/len(attendance)*100,1) if attendance else 0,
            "training_hours": hours, "avg_reaction": avg_reaction, "planned_cost": planned, "actual_cost": actual,
            "remaining_budget": planned-actual}

@app.get("/api/tenant/reporting/export.csv")
def reporting_csv(db: Session = Depends(get_db), user: User = Depends(current_user)):
    from fastapi.responses import StreamingResponse
    import csv, io
    rows = db.execute(select(Employee.name, Employee.department, TrainingProgram.name, Attendance.date, Attendance.status, Attendance.hours)
                      .join(Attendance, Attendance.employee_id==Employee.id)
                      .join(TrainingProgram, TrainingProgram.id==Attendance.program_id)
                      .where(Employee.hotel_id==user.hotel_id).order_by(Attendance.date.desc())).all()
    out=io.StringIO(); w=csv.writer(out); w.writerow(["Employee","Department","Program","Date","Attendance","Hours"]); w.writerows(rows)
    return StreamingResponse(iter([out.getvalue()]), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=hospitality-academy-report.csv"})
