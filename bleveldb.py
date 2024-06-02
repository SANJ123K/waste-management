from database import mydb
cursor = mydb.cursor()

cursor.execute("""
                create table waste_manage.blevel(
                id INT  PRIMARY KEY,
                level FLOAT NOT NULL )
                """)

cursor.close()
mydb.commit()
