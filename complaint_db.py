from database import cursor, mydb

cursor.execute("""
                CREATE TABLE waste_manage.complaint (
                  email VARCHAR(30),
                  complain VARCHAR(500)
                )
                """)
mydb.commit()
cursor.close()