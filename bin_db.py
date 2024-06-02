from database import mydb
cursor = mydb.cursor()
cursor.execute("""
                CREATE TABLE waste_manage.bin(
                bin_id varchar(10),
                area varchar(30),
                locality varchar(30),
                landmark varchar(30),
                city varchar(30),
                load_type varchar(100),
                cycle_period varchar(100))
                """)
cursor.close()
mydb.commit()
