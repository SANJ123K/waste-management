from functools import wraps
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from database import mydb
import serial

app = Flask(__name__)

app.secret_key = 'sanjeev@12345'


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/user1")
def user1():
    return render_template("user.html")


# after longin successfully use reach to the user page
@app.route("/user", methods=["POST", "GET"])
def user():
    if request.method == "POST":
        cursor = mydb.cursor()
        data = request.form
        sql = "select passwrd from waste_manage.user where email=%s"
        values = (data['email'],)
        cursor.execute(sql, values)
        res = cursor.fetchone()
        if res is not None and len(res) > 0:
            if res[0] == data['pwd']:
                session['email'] = data['email']
                return render_template("user.html", )
            else:
                return redirect("/login")
        else:
            return redirect('/login')
    else:
        return render_template("login.html")


# create a route for sign up page
@app.route("/sign-up")
def sign_up():
    return render_template("sign_up.html")


# after registration data add to the database
@app.route("/successfully", methods=["POST", "GET"])
def sucess():
    if request.method == "POST":
        cursor = mydb.cursor()
        data = request.form
        sql = "INSERT INTO waste_manage.user (first_name, last_name,email, passwrd, mobile, address, city) VALUES (" \
              "%s, %s, %s, %s, %s, %s, %s) "
        values = (
            data['first'], data['last'], data['email'], data['password'], data['mobile'], data['address'], data['city'])
        cursor.execute(sql, values)
        mydb.commit()
        return redirect('/login')

    else:
        return redirect("/sign-up")


# here we are created a complaint route
@app.route("/complaint")
def complain():
    return render_template("complain.html")


# # add new_complaint"
@app.route("/complain_succeed", methods=["POST", "GET"])
def succeed():
    try:
        if request.method == "POST":
            if 'email' in session:
                email = session['email']
                comp = request.form
                cursor = mydb.cursor()
                sql = " insert into waste_manage.complaint (email,complain) values (%s,%s)"
                values = (email, comp['complaint'])
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()
                return redirect("/complaint")  # Example usage: Displaying email
            else:
                return redirect("/login")  # Redirect if the user is not logged in
        else:
            return redirect("/complaint")
    except:
        return render_template("complain.html")


# show all user complaints
@app.route("/my-complaint")
def my_complain():
    email = session['email']
    cursor = mydb.cursor()
    sql = "SELECT complain FROM waste_manage.complaint where email= %s"
    value = (email,)
    cursor.execute(sql, value)
    complaints = cursor.fetchall()
    return render_template("my_complain.html", complaints=complaints)


# show user profile
@app.route("/user-profile")
def profile():
    email = session['email']
    cursor = mydb.cursor()
    query = "select * from waste_manage.user where email = %s"
    value = (email,)
    cursor.execute(query, value)
    data = cursor.fetchone()
    return render_template("user_profile.html", usr=data)


# admin login route
@app.route("/admin-login")
def admin_login():
    return render_template("admin_login.html")


# after longin successfully use reach to the user page
@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        cursor = mydb.cursor()
        data = request.form
        sql = "select password from waste_manage.admin where email=%s"
        values = (data['email'],)
        cursor.execute(sql, values)
        res = cursor.fetchone()
        if res is not None:
            if res[0] == data['pwd']:
                return render_template("admin.html", )
            else:
                return redirect("/admin-login")
        else:
            return redirect('/admin-login')
    else:
        return render_template("admin_login.html")


# create bin
@app.route("/create-bin")
def create_bin():
    return render_template("create_bin.html")


# add data into bin table
@app.route("/add-bin", methods=['POST', 'GET'])
def add_bin():
    if request.method == "POST":
        bin_id = request.form['bin_id']
        area = request.form['area']
        locality = request.form['locality']
        landmark = request.form['landmark']
        city = request.form['city']
        loadtype = request.form['loadtype']
        cycleperiod = request.form['cycleperiod']

        cursor = mydb.cursor()
        sql = "INSERT INTO waste_manage.bin (bin_id, area, locality, landmark, city, load_type, cycle_period) VALUES " \
              "(%s, %s, %s, %s, %s, %s, %s) "
        values = (bin_id, area, locality, landmark, city, loadtype, cycleperiod)
        cursor.execute(sql, values)
        mydb.commit()
        cursor.close()

        return redirect("/create-bin")
    else:
        return render_template("create_bin.html")


# update bin
@app.route("/update-bin", methods=['GET', 'POST'])
def update_bin():
    if request.method == "POST":
        bin_id = request.form['bin_id']
        area = request.form['area']
        locality = request.form['locality']
        landmark = request.form['landmark']
        city = request.form['city']
        loadtype = request.form['loadtype']
        cycleperiod = request.form['cycleperiod']

        cursor = mydb.cursor()
        sql = "UPDATE waste_manage.bin SET area=%s, locality=%s, landmark=%s, city=%s, load_type=%s, cycle_period=%s " \
              "WHERE bin_id=%s "
        values = (area, locality, landmark, city, loadtype, cycleperiod, bin_id)
        cursor.execute(sql, values)
        mydb.commit()
        cursor.close()

        return render_template("update_bin.html")
    else:
        return render_template("update_bin.html")


# add driver
@app.route("/register-driver", methods=['POST', 'GET'])
def register_driver():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        address = request.form['address']
        area = request.form['area']
        # Assuming you're storing ID card as a file path
        id_card = request.form['id_card']

        # Save the ID card file to a folder on your server

        # Insert the data into the database
        cursor = mydb.cursor()
        sql = "INSERT INTO waste_manage.driver (name, email, password, mobile, address, area, id_card) VALUES (%s, " \
              "%s, %s, %s, %s, %s, %s) "
        values = (name, email, password, mobile, address, area, id_card)
        cursor.execute(sql, values)
        mydb.commit()
        cursor.close()

        return redirect("/register-driver")
    else:
        return render_template("driver_registation.html")


@app.route("/view-details")
def driver_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM waste_manage.driver")
    drivers = cursor.fetchall()
    cursor.close()
    return render_template("view_details.html", drivers=drivers)


# update driver
@app.route("/update-driver", methods=["POST", "GET"])
def update_driver():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        address = request.form['address']
        area = request.form['area']
        id_card = request.form['id_card']

        cursor = mydb.cursor()
        sql = "UPDATE waste_manage.driver SET name=%s, email=%s, password=%s, mobile=%s, address=%s, area=%s, " \
              "id_card=%s WHERE email=%s "
        values = (name, email, password, mobile, address, area, id_card, email)
        cursor.execute(sql, values)
        mydb.commit()
        cursor.close()

        return render_template("update_driver.html")
    else:
        return render_template("update_driver.html")


# Delete driver
@app.route('/delete-driver', methods=['POST'])
def delete_driver():
    try:
        email = request.form.get('email')
        if not email:
            raise ValueError("Email is missing in the request form.")

        sql = "DELETE FROM waste_manage.driver WHERE email = %s"
        val = (email,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

        return redirect(url_for('driver_data'))
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred while deleting driver: {e}")
        return redirect(url_for("driver_data"))  # Redirect to driver data page with an error message


# view all complaints
@app.route("/view-complaints")
def view_complaints():
    cursor = mydb.cursor()
    cursor.execute("select email,complain from waste_manage.complaint")
    res = cursor.fetchall()
    cursor.close()
    return render_template("view_complaints.html", complaints=res)


# view user details
@app.route("/user-details")
def user_details():
    cursor = mydb.cursor()
    query = "select * from waste_manage.user"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("user_details.html", user=data)


def read_sensor_data():
    while True:
        try:
            # Replace 'COM7' with your actual COM port
            ser = serial.Serial('COM7', 9600, timeout=1)
            data = ser.readline().decode('utf-8').strip().split()
            ser.close()

            if len(data) != 2:
                print("Error: Invalid sensor data format")
                continue

            try:
                sensor_data = int(data[0])
                bin_id = int(data[1])
            except ValueError:
                print("Error: Invalid sensor data format")
                continue

            try:
                # Assuming `mydb` is defined and connected somewhere in your code
                cursor = mydb.cursor()
                sql = "SELECT ID FROM waste_manage.blevel WHERE id = %s"
                val = (bin_id,)
                cursor.execute(sql, val)
                res = cursor.fetchone()

                if res:
                    cursor.execute("UPDATE waste_manage.blevel SET level = %s WHERE id = %s", (sensor_data, bin_id))
                else:
                    cursor.execute("INSERT INTO waste_manage.blevel (id, level) VALUES (%s, %s)", (bin_id, sensor_data))

                mydb.commit()
                cursor.close()
                break
            except mydb.Error as db_err:
                print(f"Error: Database error - {db_err}")
            except Exception as e:
                print(f"An unexpected error occurred while interacting with the database: {e}")

        except serial.SerialException as e:
            print(f"Error: Could not open port: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# show bin-level
@app.route("/bin-level")
def bin_level():
    read_sensor_data()
    return render_template("bin_level.html")


@app.route('/data/<int:item_id>', methods=['GET'])
def get_data(item_id):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT id, level FROM waste_manage.blevel WHERE id = %s", (item_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return jsonify({"id": result[0], "level": result[1]}), 200
        else:
            return jsonify({"message": "Data not found"}), 404
    except mydb.connector.Error as err:
        return jsonify({"message": f"Database error: {err}"}), 500


# driver longin
@app.route("/driver-login")
def driver_login():
    return render_template("driver_login.html")


# successfully login
@app.route("/driver-field", methods=["POST", "GET"])
def driver_fun():
    try:
        if request.method == "POST":
            cursor = mydb.cursor()
            data = request.form

            # Use parameterized query to prevent SQL injection
            sql = "SELECT password ,address ,mobile FROM waste_manage.driver WHERE email = %s"
            values = (data['email'],)
            cursor.execute(sql, values)
            res = cursor.fetchone()
            cursor.close()

            if res:
                # Check if the password matches
                if res[0] == data['pwd']:
                    session['city'] = res[1]
                    session["mobile"] = res[2]
                    return render_template("driver_field.html")
                else:
                    return redirect("/driver-login")
            else:
                return redirect('/driver-login')
        else:
            return redirect('/driver-login')  # Handle GET requests by redirecting to login
    except Exception as e:
        # Log the exception if needed, for debugging
        # print(f"Error: {e}")
        return redirect("/driver-login")


# driver notification
@app.route("/driver-notification")
def driver_notification():
    try:
        cursor = mydb.cursor()
        sql = "SELECT id FROM waste_manage.blevel WHERE level < %s"
        lev = (3,)
        cursor.execute(sql, lev)
        ids = [row[0] for row in cursor.fetchall()]

        res = []
        driver_info = []
        if ids:
            for bin_id in ids:
                sql = "SELECT bin_id, area, locality, landmark, city FROM waste_manage.bin WHERE bin_id = %s"
                val = (bin_id,)
                cursor.execute(sql, val)
                result = cursor.fetchone()
                if result:
                    city = session['city']
                    # Get driver name and mobile number
                    sql = "SELECT name, mobile FROM waste_manage.driver WHERE address = %s"
                    city = (city,)
                    cursor.execute(sql, city)
                    driver = cursor.fetchone()
                    if driver:
                        result = result + driver
                    else:
                        result = result + ("No drive", "No driver")
                    res.append(result)

        cursor.close()
        return render_template("driver_notification.html", dustbin=res)
    except Exception as e:
        # Log the exception if needed, for debugging
        print(f"Error->: {e}")
        return redirect(url_for("driver_fun"))


@app.route("/collected", methods=['POST'])
def collected():
    try:
        if request.method == "POST":
            # Retrieve form data
            dustbin_id = request.form.get('dustbin_id')
            area = request.form.get('area')
            locality = request.form.get('locality')
            landmark = request.form.get('landmark')
            city = request.form.get('city')
            driver_name = request.form.get('driver_name')
            mobile_number = request.form.get('mobile_number')
            date = request.form.get('date')

            # Print the retrieved data for debugging purposes
            print("Received data:", dustbin_id, area, locality, landmark, city, driver_name, mobile_number, date)
            # delete data from bin database
            sql = """update waste_manage.blevel 
                      set level = %s
                      where id = %s"""
            value = (0, int(dustbin_id))
            cursor = mydb.cursor()
            cursor.execute(sql,value)
            cursor.close()
            mydb.commit()

            # Insert data into database
            sql = """INSERT INTO waste_manage.collect 
                     (bin_id, area, locality, landmark, city, d_name, mobile, dt) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (dustbin_id, area, locality, landmark, city, driver_name, mobile_number, date)
            cursor = mydb.cursor()
            cursor.execute(sql, values)
            mydb.commit()
            cursor.close()

            # Redirect to driver-notification page after successful insertion
            return redirect(url_for('driver_notification'))
        else:
            return redirect(url_for('driver_notification'))
    except Exception as e:
        # Log the exception (for debugging purposes)
        print(f"An error occurred: {e}")
        return redirect(url_for('driver_notification'))


# show collected trash can
@app.route("/view-dustbins")
def view_dustbin():
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM waste_manage.collect WHERE mobile = %s"
        value = (session['mobile'],)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        cursor.close()
        if result:
            return render_template("collected_dustbin.html", dustbin=result)
        else:
            return redirect("driver-field")
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect("driver-field")


if __name__ == "__main__":
    app.run(debug=True)
