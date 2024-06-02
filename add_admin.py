from database import mydb

cursor = mydb.cursor()


def add_admin(emal, paswd):
    sql = "insert into waste_manage.admin (email, password) values (%s,%s)"
    values = (emal, paswd)
    cursor.execute(sql, values)
    cursor.close()
    mydb.commit()


email = "sanjeevlodhi642@gmail.com"
passwd = "sanjeev@123"
add_admin(email, passwd)
