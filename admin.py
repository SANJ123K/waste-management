from database import mydb

cursor = mydb.cursor()

cursor.execute("""
                create table waste_manage.admin(
                 email varchar(30),
                 password varchar(30))
                """)
cursor.close()
mydb.commit()