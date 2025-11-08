"""Command-line utility that performs CRUD operations on the students table."""
import argparse
from datetime import date
from typing import Iterable, Optional, Sequence
import uuid

from database import DatabaseError, execute_query


def getAllStudents() -> Iterable:
    rows = execute_query(
        """
        SELECT student_id, first_name, last_name, email, enrollment_date
        FROM students
        ORDER BY student_id
        """,
        fetch=True,
    ) or []
    _print_students(rows)
    return rows


def addStudent(first_name: str, last_name: str, email: str, enrollment_date: date) -> Optional[int]:
    rows = execute_query(
        """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id
        """,
        (first_name, last_name, email, enrollment_date),
        fetch=True,
    )
    if rows:
        student_id = rows[0][0]
        print(f"Added student #{student_id}: {first_name} {last_name}")
        return student_id
    print("Student insertion did not return an id.")
    return None


def updateStudentEmail(student_id: int, new_email: str) -> bool:
    rows = execute_query(
        """
        UPDATE students
        SET email = %s
        WHERE student_id = %s
        RETURNING student_id
        """,
        (new_email, student_id),
        fetch=True,
    )
    updated = bool(rows)
    message = "Updated" if updated else "No student found to update"
    print(f"{message} for id {student_id}.")
    return updated


def deleteStudent(student_id: int) -> bool:
    rows = execute_query(
        """
        DELETE FROM students
        WHERE student_id = %s
        RETURNING student_id
        """,
        (student_id,),
        fetch=True,
    )
    deleted = bool(rows)
    message = "Deleted" if deleted else "No student found to delete"
    print(f"{message} for id {student_id}.")
    return deleted


def _print_students(rows: Sequence[Sequence]) -> None:
    """Print the current contents of the students table."""
    if not rows:
        print("No students found.\n")
        return

    print("student_id | first_name | last_name | email | enrollment_date")
    for student_id, first_name, last_name, email, enrollment_date in rows:
        print(f"{student_id:>10} | {first_name:<10} | {last_name:<10} | {email:<30} | {enrollment_date}")
    print()


def _pause(enabled: bool) -> None:
    """Pause execution until Enter is pressed."""
    if not enabled:
        return
    input("Press Enter to continue...")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CRUD demo against the students table.")
    parser.add_argument(
        "--step",
        action="store_true",
        help="Pause after every CRUD operation so you can refresh pgAdmin before continuing.",
    )
    return parser.parse_args()


def main() -> None:
    """Demonstration of each helper"""
    args = _parse_args()
    stepping_enabled = args.step

    try:
        print("=== Initial Students ===")
        getAllStudents()
        _pause(stepping_enabled)

        print("=== Adding a Student ===")
        new_email = f"new.student.{uuid.uuid4().hex[:6]}@example.com"
        new_student_id = addStudent(
            first_name="Alice",
            last_name="Wonder",
            email=new_email,
            enrollment_date=date.today(),
        )
        getAllStudents()
        _pause(stepping_enabled)

        if new_student_id is None:
            print("Cannot continue demo without a new student id.")
            return

        print("=== Updating the Student Email ===")
        updateStudentEmail(new_student_id, f"updated.{new_email}")
        getAllStudents()
        _pause(stepping_enabled)

        print("=== Deleting the Student ===")
        deleteStudent(new_student_id)
        getAllStudents()
        _pause(stepping_enabled)
    except DatabaseError as error:
        print(error)


if __name__ == "__main__":
    main()
