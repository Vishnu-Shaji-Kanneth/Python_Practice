# Student Grading System

import sqlite3
DB = "academic_system_v17_final.db"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE,
        name TEXT,
        class TEXT,
        user_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        subject TEXT,
        class TEXT,
        is_coordinator INTEGER,
        user_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        student_id INTEGER,
        subject TEXT,
        marks INTEGER,
        grade TEXT,
        PRIMARY KEY(student_id, subject)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        student_id INTEGER,
        subject TEXT,
        percentage REAL,
        status TEXT,
        PRIMARY KEY(student_id, subject)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grievances(
        grievance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        message TEXT,
        status TEXT DEFAULT 'Pending',
        remarks TEXT
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO users(username,password,role)
    VALUES('admin','admin123','Admin')
    """)

    con.commit()
    con.close()

# ---------------- UTILITIES ----------------

def calculate_grade(m):
    if m >= 90: return "A+"
    elif m >= 80: return "A"
    elif m >= 70: return "B"
    elif m >= 60: return "C"
    elif m >= 50: return "D"
    else: return "F"

def attendance_status(p):
    return "Eligible" if p >= 75 else "Shortage"

def login():
    u = input("Username: ")
    p = input("Password: ")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT user_id, role FROM users WHERE username=? AND password=?", (u,p))
    res = cur.fetchone()
    con.close()
    return res

def change_password(uid):
    new = input("New Password: ")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("UPDATE users SET password=? WHERE user_id=?", (new,uid))
    con.commit()
    con.close()
    print("Password updated successfully")

# ---------------- ADMIN FUNCTIONS ----------------

def view_teachers():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    SELECT u.username, t.name, t.subject, t.class, t.is_coordinator
    FROM teachers t JOIN users u ON t.user_id=u.user_id
    """)
    print("\nUsername | Name | Subject | Class | Coordinator")
    for r in cur.fetchall(): print(r)
    con.close()

def view_students_admin():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT roll_no, name, class FROM students")
    print("\nRoll No | Name | Class")
    for r in cur.fetchall(): print(r)
    con.close()

def register_teacher():
    uname = input("Username: ")
    pwd = input("Password: ")
    name = input("Name: ")
    subject = input("Subject: ")
    cls = input("Class: ")
    coord = int(input("Class Coordinator? (1-Yes / 0-No): "))

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES(NULL,?,?,?)",(uname,pwd,"Teacher"))
    uid = cur.lastrowid
    cur.execute("""
    INSERT INTO teachers(name,subject,class,is_coordinator,user_id)
    VALUES(?,?,?,?,?)
    """,(name,subject,cls,coord,uid))
    con.commit()
    con.close()
    print("Teacher registered")

def edit_teacher():
    uname = input("Teacher username to edit: ")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    SELECT t.teacher_id, t.name, t.subject, t.class, t.is_coordinator
    FROM teachers t JOIN users u ON t.user_id=u.user_id
    WHERE u.username=?
    """,(uname,))
    t = cur.fetchone()
    if not t:
        print("Teacher not found")
        con.close()
        return

    name = input("New Name (Enter to keep same): ") or t[1]
    subject = input("New Subject (Enter to keep same): ") or t[2]
    cls = input("New Class (Enter to keep same): ") or t[3]
    coord = input("Coordinator 1/0 (Enter to keep same): ")
    coord = int(coord) if coord else t[4]

    cur.execute("""
    UPDATE teachers SET name=?, subject=?, class=?, is_coordinator=?
    WHERE teacher_id=?
    """,(name,subject,cls,coord,t[0]))
    con.commit()
    con.close()
    print("Teacher updated")

def delete_teacher():
    uname = input("Teacher username to delete: ")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT user_id FROM users WHERE username=? AND role='Teacher'",(uname,))
    r = cur.fetchone()
    if not r:
        print("Teacher not found")
        con.close()
        return
    uid = r[0]
    cur.execute("DELETE FROM teachers WHERE user_id=?", (uid,))
    cur.execute("DELETE FROM users WHERE user_id=?", (uid,))
    con.commit()
    con.close()
    print("Teacher deleted")

def register_student():
    uname = input("Username: ")
    pwd = input("Password: ")
    roll = input("Roll No: ")
    name = input("Name: ")
    cls = input("Class: ")

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES(NULL,?,?,?)",(uname,pwd,"Student"))
    uid = cur.lastrowid
    cur.execute("""
    INSERT INTO students(roll_no,name,class,user_id)
    VALUES(?,?,?,?)
    """,(roll,name,cls,uid))
    con.commit()
    con.close()
    print("Student registered")

def edit_student():
    roll = input("Roll No to edit: ")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT student_id, roll_no, name, class FROM students WHERE roll_no=?", (roll,))
    s = cur.fetchone()
    if not s:
        print("Student not found")
        con.close()
        return

    roll_no = input("New Roll (Enter to keep same): ") or s[1]
    name = input("New Name (Enter to keep same): ") or s[2]
    cls = input("New Class (Enter to keep same): ") or s[3]

    cur.execute("""
    UPDATE students SET roll_no=?, name=?, class=? WHERE student_id=?
    """,(roll_no,name,cls,s[0]))
    con.commit()
    con.close()
    print("Student updated")

def delete_student():
    roll = input("Roll No to delete: ")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT student_id,user_id FROM students WHERE roll_no=?", (roll,))
    s = cur.fetchone()
    if not s:
        print("Student not found")
        con.close()
        return

    sid, uid = s
    cur.execute("DELETE FROM marks WHERE student_id=?", (sid,))
    cur.execute("DELETE FROM attendance WHERE student_id=?", (sid,))
    cur.execute("DELETE FROM grievances WHERE student_id=?", (sid,))
    cur.execute("DELETE FROM students WHERE student_id=?", (sid,))
    cur.execute("DELETE FROM users WHERE user_id=?", (uid,))
    con.commit()
    con.close()
    print("Student deleted")

def admin_menu():
    while True:
        print("""
--- ADMIN MENU ---
1. Register Teacher
2. Edit Teacher
3. Delete Teacher
4. View Teachers
5. Register Student
6. Edit Student
7. Delete Student
8. View Students
9. Logout
""")
        ch = input("Choice: ")
        if ch=="1": register_teacher()
        elif ch=="2": edit_teacher()
        elif ch=="3": delete_teacher()
        elif ch=="4": view_teachers()
        elif ch=="5": register_student()
        elif ch=="6": edit_student()
        elif ch=="7": delete_student()
        elif ch=="8": view_students_admin()
        else: break

# ---------------- TEACHER FUNCTIONS ----------------

def view_students(cls):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT roll_no,name FROM students WHERE class=?", (cls,))
    for r in cur.fetchall(): print(r)
    con.close()

def view_marks_attendance(subject, cls):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    print("\n--- MARKS ---")
    cur.execute("""
    SELECT s.roll_no,s.name,m.marks,m.grade
    FROM marks m JOIN students s ON m.student_id=s.student_id
    WHERE m.subject=? AND s.class=?
    """,(subject,cls))
    for r in cur.fetchall(): print(r)

    print("\n--- ATTENDANCE ---")
    cur.execute("""
    SELECT s.roll_no,s.name,a.percentage,a.status
    FROM attendance a JOIN students s ON a.student_id=s.student_id
    WHERE a.subject=? AND s.class=?
    """,(subject,cls))
    for r in cur.fetchall(): print(r)

    con.close()

def coordinator_dashboard(cls):
    print("\n--- COORDINATOR DASHBOARD (READ ONLY) ---")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    SELECT s.roll_no,s.name,m.subject,m.marks,m.grade
    FROM marks m JOIN students s ON m.student_id=s.student_id
    WHERE s.class=?
    """,(cls,))
    for r in cur.fetchall(): print(r)
    con.close()

def teacher_menu(uid):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT subject,class,is_coordinator FROM teachers WHERE user_id=?", (uid,))
    t = cur.fetchone()
    con.close()

    while True:
        print("""
--- TEACHER MENU ---
1. View Students
2. View Marks & Attendance
3. Enter/Edit Marks
4. Enter/Edit Attendance
5. Handle Grievances
6. Coordinator Dashboard
7. Change Password
8. Logout
""")
        ch = input("Choice: ")

        if ch=="1":
            view_students(t[1])

        elif ch=="2":
            view_marks_attendance(t[0], t[1])


        elif ch == "3":
            roll = input("Student Roll No: ")
            try:
                m = int(input("Marks (0–100): "))
                if m < 0 or m > 100:
                    print("Invalid entry: Marks must be between 0 and 100")
                    continue
            except ValueError:
                print("Invalid input: Enter numeric marks only")
                continue
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute("SELECT student_id FROM students WHERE roll_no=?", (roll,))
            r = cur.fetchone()
            if not r:
                print("Error: Student not registered")
                con.close()
                continue
            g = calculate_grade(m)
            cur.execute("""
            INSERT OR REPLACE INTO marks(student_id,subject,marks,grade)
            VALUES(?,?,?,?)
            """, (r[0], t[0], m, g))
            con.commit()
            con.close()
            print("Marks saved / updated successfully")
        elif ch == "4":
            roll = input("Student Roll No: ")
            try:
                p = float(input("Attendance % (0–100): "))
                if p < 0 or p > 100:
                    print("Invalid entry: Attendance must be between 0 and 100")
                    continue
            except ValueError:
                print("Invalid input: Enter numeric attendance only")
                continue

            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute("SELECT student_id FROM students WHERE roll_no=?", (roll,))
            r = cur.fetchone()

            if not r:
                print("Error: Student not registered")
                con.close()
                continue

            st = attendance_status(p)
            cur.execute("""
            INSERT OR REPLACE INTO attendance(student_id,subject,percentage,status)
            VALUES(?,?,?,?)
            """, (r[0], t[0], p, st))
            con.commit()
            con.close()
            print("Attendance saved / updated successfully")


        elif ch=="5":
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute("""
            SELECT grievance_id,message FROM grievances
            WHERE subject=? AND status='Pending'
            """,(t[0],))
            for g in cur.fetchall():
                print(g)
                a = input("Approve(A)/Reject(R): ")
                if a=="A":
                    cur.execute("UPDATE grievances SET status='Approved' WHERE grievance_id=?", (g[0],))
                elif a=="R":
                    rem = input("Enter rejection remarks: ")
                    cur.execute("UPDATE grievances SET status='Rejected', remarks=? WHERE grievance_id=?",(rem,g[0]))
            con.commit()
            con.close()

        elif ch=="6" and t[2]==1:
            coordinator_dashboard(t[1])

        elif ch=="7":
            change_password(uid)
        else:
            break

# ---------------- STUDENT FUNCTIONS ----------------

def view_student_grievances(uid):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    SELECT subject, message, status, IFNULL(remarks,'-')
    FROM grievances
    WHERE student_id=(SELECT student_id FROM students WHERE user_id=?)
    """,(uid,))
    rows = cur.fetchall()
    if not rows:
        print("\nNo grievances submitted yet.")
    else:
        print("\nSubject | Message | Status | Remarks")
        for r in rows: print(r)
    con.close()

def student_menu(uid):
    while True:
        print("""
--- STUDENT MENU ---
1. View Profile
2. View Marks & Grades
3. View Attendance
4. Submit Grievance
5. View Grievance Status
6. Change Password
7. Logout
""")
        ch = input("Choice: ")
        con = sqlite3.connect(DB)
        cur = con.cursor()

        if ch=="1":
            cur.execute("SELECT roll_no,name,class FROM students WHERE user_id=?", (uid,))
            print(cur.fetchone())

        elif ch=="2":
            cur.execute("""
            SELECT subject,marks,grade FROM marks
            WHERE student_id=(SELECT student_id FROM students WHERE user_id=?)
            """,(uid,))
            for r in cur.fetchall(): print(r)

        elif ch=="3":
            cur.execute("""
            SELECT subject,percentage,status FROM attendance
            WHERE student_id=(SELECT student_id FROM students WHERE user_id=?)
            """,(uid,))
            for r in cur.fetchall(): print(r)

        elif ch=="4":
            sub = input("Subject: ")
            msg = input("Message: ")
            cur.execute("""
            INSERT INTO grievances(student_id,subject,message)
            VALUES((SELECT student_id FROM students WHERE user_id=?),?,?)
            """,(uid,sub,msg))
            con.commit()
            print("Grievance submitted")

        elif ch=="5":
            view_student_grievances(uid)

        elif ch=="6":
            change_password(uid)

        else:
            con.close()
            break

        con.close()

# ---------------- MAIN ----------------

def main():
    init_db()
    while True:
        print("\n--- LOGIN ---")
        res = login()
        if not res:
            print("Invalid credentials")
            continue

        uid, role = res
        if role=="Admin":
            admin_menu()
        elif role=="Teacher":
            teacher_menu(uid)
        elif role=="Student":
            student_menu(uid)

        end = input("\nExit program? (y/n): ")
        if end.lower() == 'y':
            print("\nProgram terminated successfully.")
            break

main()
