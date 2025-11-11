#!/usr/bin/env python3
"""
student_record_cassandra.py

Student Record Management using Cassandra NoSQL Database
SDG 4 – Quality Education
Technologies: Cassandra (Data Replication shown via keyspace settings), Python cassandra-driver

Requirements:
    pip install cassandra-driver

How to use:
    - Ensure Cassandra is running and accessible (default localhost:9042).
    - Update CONTACT_POINTS or AUTH if you connect to a different host or use authentication.
    - Run: python student_record_cassandra.py
"""

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import uuid
import sys

# ---------- Configuration ----------
CONTACT_POINTS = ['127.0.0.1']   # change to your node(s)
PORT = 9042
KEYSPACE = "student_mgmt"
REPLICATION_STRATEGY = {
    'class': 'SimpleStrategy',   # For multi-datacenter use 'NetworkTopologyStrategy'
    'replication_factor': 1     # set to 3 (or higher) for production clusters
}
# -----------------------------------

def connect(contact_points=CONTACT_POINTS, port=PORT):
    """Connects to Cassandra cluster and returns (cluster, session)."""
    cluster = Cluster(contact_points, port=port)
    session = cluster.connect()
    return cluster, session

def create_keyspace(session, keyspace=KEYSPACE, replication=REPLICATION_STRATEGY):
    """Creates keyspace with the given replication options if not exists."""
    # build replication map string
    if replication['class'] == 'SimpleStrategy':
        rf = replication.get('replication_factor', 1)
        repl_str = f"{{'class': 'SimpleStrategy', 'replication_factor': {rf}}}"
    else:
        # for NetworkTopologyStrategy user should give map; we keep a simple fallback
        repl_str = str(replication).replace("'", "\"")
    cql = f"""
    CREATE KEYSPACE IF NOT EXISTS {keyspace}
    WITH replication = {repl_str};
    """
    session.execute(cql)
    # switch to keyspace
    session.set_keyspace(keyspace)

def create_table(session):
    """Creates students table to store student records."""
    # Using student_id as primary key (UUID) — behaves like a key in a key-value store
    cql = """
    CREATE TABLE IF NOT EXISTS students (
        student_id uuid,
        student_roll text,
        first_name text,
        last_name text,
        email text,
        dob date,
        course text,
        year int,
        created_at timestamp,
        PRIMARY KEY (student_id)
    );
    """
    session.execute(cql)

def insert_student(session, student_roll, first_name, last_name, email, dob, course, year):
    """Insert a new student; returns generated uuid."""
    sid = uuid.uuid4()
    stmt = session.prepare("""
        INSERT INTO students (student_id, student_roll, first_name, last_name, email, dob, course, year, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, toTimestamp(now()));
    """)
    session.execute(stmt, (sid, student_roll, first_name, last_name, email, dob, course, year))
    return sid

def get_student(session, student_id):
    """Fetch a student by UUID (student_id)."""
    stmt = session.prepare("SELECT * FROM students WHERE student_id=?")
    row = session.execute(stmt, (student_id,)).one()
    return row

def get_student_by_roll(session, student_roll):
    """Fetch by roll using a simple query (requires ALLOW FILTERING or dedicated index/table in prod)."""
    # WARNING: ALLOW FILTERING is not recommended for production large tables.
    cql = "SELECT * FROM students WHERE student_roll = %s ALLOW FILTERING"
    row = session.execute(cql, (student_roll,)).one()
    return row

def update_student_email(session, student_id, new_email):
    """Update email of a student."""
    stmt = session.prepare("UPDATE students SET email = ? WHERE student_id = ?")
    session.execute(stmt, (new_email, student_id))

def delete_student(session, student_id):
    """Delete a student by UUID."""
    stmt = session.prepare("DELETE FROM students WHERE student_id = ?")
    session.execute(stmt, (student_id,))

def list_students(session, limit=50):
    """List students (simple scan)."""
    cql = SimpleStatement("SELECT * FROM students LIMIT %s" % limit, consistency_level=ConsistencyLevel.ONE)
    rows = session.execute(cql)
    return list(rows)

def print_row(row):
    if not row:
        print("No record found.")
        return
    print("student_id :", row.student_id)
    print("roll       :", getattr(row, 'student_roll', None))
    print("name       :", f"{getattr(row,'first_name', '')} {getattr(row,'last_name','')}")
    print("email      :", getattr(row, 'email', None))
    print("dob        :", getattr(row, 'dob', None))
    print("course     :", getattr(row, 'course', None))
    print("year       :", getattr(row, 'year', None))
    print("created_at :", getattr(row, 'created_at', None))

def interactive_cli(session):
    """Very small CLI to demo CRUD operations."""
    MENU = """
    Student Record Management - Cassandra (single-file demo)
    Choose an option:
      1) Insert student
      2) Get student by UUID
      3) Get student by roll (ALLOW FILTERING demo)
      4) Update student email
      5) Delete student
      6) List students
      7) Exit
    """
    while True:
        print(MENU)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            roll = input("Roll: ").strip()
            fn = input("First name: ").strip()
            ln = input("Last name: ").strip()
            email = input("Email: ").strip()
            dob = input("DOB (YYYY-MM-DD) or blank: ").strip() or None
            course = input("Course: ").strip()
            year = input("Year (int): ").strip()
            year = int(year) if year else None
            sid = insert_student(session, roll, fn, ln, email, dob, course, year)
            print("Inserted student with UUID:", sid)
        elif choice == '2':
            sid = input("Student UUID: ").strip()
            try:
                sid_uuid = uuid.UUID(sid)
            except Exception:
                print("Invalid UUID format.")
                continue
            row = get_student(session, sid_uuid)
            print_row(row)
        elif choice == '3':
            roll = input("Student roll: ").strip()
            row = get_student_by_roll(session, roll)
            print_row(row)
        elif choice == '4':
            sid = input("Student UUID: ").strip()
            new_email = input("New Email: ").strip()
            try:
                sid_uuid = uuid.UUID(sid)
            except Exception:
                print("Invalid UUID format.")
                continue
            update_student_email(session, sid_uuid, new_email)
            print("Updated email.")
        elif choice == '5':
            sid = input("Student UUID: ").strip()
            try:
                sid_uuid = uuid.UUID(sid)
            except Exception:
                print("Invalid UUID format.")
                continue
            delete_student(session, sid_uuid)
            print("Deleted (if existed).")
        elif choice == '6':
            rows = list_students(session, limit=100)
            for r in rows:
                print("------------------------------")
                print_row(r)
            print("Total shown:", len(rows))
        elif choice == '7' or choice.lower() in ('exit', 'q'):
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

def main():
    print("Connecting to Cassandra at", CONTACT_POINTS)
    try:
        cluster, session = connect()
    except Exception as e:
        print("Error connecting to Cassandra:", e)
        sys.exit(1)

    try:
        create_keyspace(session)
        create_table(session)
        print(f"Keyspace '{KEYSPACE}' and table 'students' are ready.")
        interactive_cli(session)
    finally:
        try:
            session.shutdown()
            cluster.shutdown()
        except Exception:
            pass

if __name__ == "__main__":
    main()

