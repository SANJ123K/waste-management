from database import mydb

cursor = mydb.cursor()
cursor.execute("""
                CREATE TABLE waste_manage.driver(
                name varchar(30),
                email varchar(30),
                password varchar(30),
                mobile varchar(10),
                address varchar(50),
                area varchar(30),
                id_card varchar(20))                
                """)
cursor.close()
mydb.commit()
