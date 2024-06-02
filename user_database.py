from database import cursor, mydb
cursor.execute(""" 
           create table waste_manage.user(
            first_name varchar(20),
            last_name varchar(20),
            email    varchar(30),
            passwrd varchar(20),
            mobile varchar(10),
            address varchar(50),
            city varchar(50))
""")
mydb.commit()
cursor.close()