# Student Management API

A REST API for managing student records built with FastAPI and SQLite.

---

## Setup Instructions

1. Clone the repository
2. Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv\bin\activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run the server:
    ```
    uvicorn main:app --reload
    ```
5. Open your browser to `http://localhost:8000`

---

## Endpoints

| Method | Endpoint                    | Description                    |
|--------|-----------------------------|--------------------------------|
| GET    | `/students`                 | Get all students               |
| GET    | `/students/{student_id}`    | Get a student by ID            |
| POST   | `/students`                 | Create a new student           |
| PUT    | `/students/{student_id}`    | Update a student by ID         |
| DELETE | `/students/{student_id}`    | Delete a student by ID         |
| GET    | `/students/by-major?major=` | Filter students by major       |
| GET    | `/students/by-gpa?min_gpa=` | Filter students by minimum GPA |

---

## Testing Instructions

1. Make sure the server is running with `uvicorn main:app --reload`
2. Open `http://localhost:8000/docs` in your browser
3. Use the interactive docs to test each endpoint:
    - Use **POST /students** to create a student first
    - Then test GET, PUT, and DELETE using the student's ID
    - Test filtering with **GET /students/by-major** and **GET /students/by-gpa**
4. To verify data persistence, create a student, restart the server, and confirm the student still exists

---

## Project Structure

```
student-api/
├── main.py          # App entry point
├── models.py        # Student data model
├── database.py      # Database connection helpers
├── routes.py        # API route handlers
├── requirements.txt # Dependencies
└── README.md        # Documentation
```
---

## Example Usage

### 1. Create a new student (POST)
```
POST http://localhost:8000/students
Content-Type: application/json

{
  "name": "Joey Grottola",
  "email": "jgrottola@mocs.flsouthern.edu",
  "major": "Computer Science",
  "gpa": 4.0,
  "enrollment_year": 2024
}
```

### 2. Get a student by ID (GET)
```
GET http://localhost:8000/students/1
```

Expected response:
```json
{
  "id": 1,
  "name": "Joey Grottola",
  "email": "jgrottola@mocs.flsouthern.edu",
  "major": "Computer Science",
  "gpa": 4.0,
  "enrollment_year": 2024
}
```

### 3. Filter students by GPA (GET)
```
GET http://localhost:8000/students/by-gpa?min_gpa=4.0
```

Expected response:
```json
{
  "students": [...],
  "count": 1,
  "min_gpa": 4.0
}
```
