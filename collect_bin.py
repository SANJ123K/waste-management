from database import mydb

cursor = mydb.cursor()

cursor.execute("""
                create table waste_manage.collect(
                bin_id varchar(10),
                area varchar(20),
                locality varchar(20),
                landmark varchar(20),
                city varchar(20),
                d_name varchar(20),
                mobile varchar(10),
                dt Date)          
                """)

cursor.close()
mydb.commit()
