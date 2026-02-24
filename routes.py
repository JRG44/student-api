from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection

router = APIRouter()


@router.get("/students")
def get_all_students():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    students = [dict(row) for row in rows]
    return {"students": students, "count": len(students)}


@router.get("/students/by-major")
def get_students_by_major(major: str):
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM students WHERE major = ?", (major,))
    rows = cursor.fetchall()
    conn.close()

    students = [dict(row) for row in rows]
    return {"students": students, "count": len(students), "major": major}


@router.get("/students/by-gpa")
def get_students_by_gpa(min_gpa: float):
    if min_gpa < 0.0 or min_gpa > 4.0:
        raise HTTPException(status_code=400, detail="min_gpa must be between 0.0 and 4.0")

    conn = get_connection()
    cursor = conn.execute("SELECT * FROM students WHERE gpa >= ?", (min_gpa,))
    rows = cursor.fetchall()
    conn.close()

    students = [dict(row) for row in rows]
    return {"students": students, "count": len(students), "min_gpa": min_gpa}


@router.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    return dict(row)


@router.post("/students", status_code=201)
def create_student(student: Student):
    if not student.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO students (name, email, major, gpa, enrollment_year) VALUES (?, ?, ?, ?, ?)",
        (student.name, student.email, student.major, student.gpa, student.enrollment_year)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {**student.dict(), "id": new_id}


@router.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if not student.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    conn = get_connection()
    cursor = conn.execute(
        "UPDATE students SET name = ?, email = ?, major = ?, gpa = ?, enrollment_year = ? WHERE id = ?",
        (student.name, student.email, student.major, student.gpa, student.enrollment_year, student_id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    return {**student.dict(), "id": student_id}


@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    return {"message": "Student deleted successfully"}