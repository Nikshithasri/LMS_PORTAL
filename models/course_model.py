def add_course(cursor, name, code):
    cursor.execute("""
        INSERT INTO courses(course_name, course_code)
        VALUES(%s,%s)
    """, (name, code))
