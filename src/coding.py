from flask import *
from src.dbconnection import *

import razorpay

app = Flask(__name__)

app.secret_key = "74745"


@app.route('/')
def login():
    return render_template("login_index.html")


@app.route('/login_code', methods=['post'])
def login_code():
    uname = request.form['textfield']
    pswd = request.form['textfield2']
    qry = "select * from login where username=%s and password=%s"
    val = (uname,pswd)
    res = selectone(qry, val)

    if res is None:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''
    elif res['type'] == "admin":
        session['lid'] = res['id']
        return '''<script>alert("Welcome admin");window.location="/admin_home"</script>'''
    elif res['type'] == "station":
        session['lid'] = res['id']
        return '''<script>alert("Welcome");window.location="/station_home"</script>'''
    elif res['type'] == "user":
        session['lid'] = res['id']
        return '''<script>alert("Welcome");window.location="/user_home"</script>'''
    else:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''


@app.route('/station_register')
def station_register():
    return render_template("station_register.html")


@app.route('/station_register_code', methods=['post'])
def station_register_code():

    try:

        print(request.form)

        name = request.form['textfield']
        place = request.form['textfield2']
        post = request.form['textfield3']
        pin = request.form['textfield4']
        email = request.form['textfield5']
        contact = request.form['textfield6']
        lati = request.form['lati']
        longi = request.form['longi']
        uname = request.form['textfield7']
        pswd = request.form['textfield8']

        qry = "select * from charging_station where email=%s"
        res = selectone(qry,email)

        if res is not None:
            return '''<script>alert("Email already exist");window.location="/#about"</script>'''
        else:
            qry = "insert into login values(null,%s,%s,'pending')"
            val = (uname,pswd)
            id = iud(qry,val)
            qry = "INSERT INTO `charging_station` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (id,name,place,post,pin,email,contact,lati,longi)
            iud(qry,val)

            return '''<script>alert("Registration success");window.location="/#about"</script>'''
    except:
        return '''<script>alert("Username already exist");window.location="/#about"</script>'''


@app.route('/user_register')
def user_register():
    return render_template("user_register.html")


@app.route('/user_register_code', methods=['post'])
def user_register_code():

    try:

        print(request.form)

        name = request.form['textfield']
        place = request.form['textfield2']
        post = request.form['textfield3']
        pin = request.form['textfield4']
        email = request.form['textfield5']
        contact = request.form['textfield6']

        uname = request.form['textfield7']
        pswd = request.form['textfield8']

        qry = "select * from user where email=%s"
        res = selectone(qry, email)

        if res is not None:
            return '''<script>alert("Email already exist");window.location="/#about"</script>'''
        else:
            qry = "insert into login values(null,%s,%s,'user')"
            val = (uname,pswd)
            id = iud(qry,val)
            qry = "INSERT INTO `user` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)"
            val = (id, name, place, post, pin, email, contact)
            iud(qry,val)

            return '''<script>alert("Registration success");window.location="/#about"</script>'''
    except:
        return '''<script>alert("Username already exist");window.location="/#about"</script>'''


@app.route('/admin_home')
def admin_home():
    return render_template("Admin/admin_index.html")


@app.route('/verify_charging_station')
def verify_charging_station():
    qry = 'SELECT * FROM `charging_station` JOIN `login` ON `charging_station`.`lid`=`login`.id WHERE `login`.type = "pending"'
    res = selectall(qry)
    return render_template("Admin/verify_charging_station.html", val=res)


@app.route("/accept_station")
def accept_station():
    id = request.args.get('id')
    qry = "update login set type = 'station' where id = %s"
    iud(qry, id)
    return '''<script>alert("Accepted");window.location="verify_charging_station"</script>'''


@app.route("/reject_station")
def reject_station():
    id = request.args.get('id')
    qry = "update login set type = 'rejected' where id = %s"
    iud(qry, id)
    return '''<script>alert("Rejected");window.location="verify_charging_station"</script>'''


@app.route('/block_charging_station')
def block_charging_station():
    qry = 'SELECT * FROM `charging_station` JOIN `login` ON `charging_station`.`lid`=`login`.id WHERE `login`.type = "station" or `login`.type = "blocked"'
    res = selectall(qry)
    return render_template("Admin/block_unblock_charging_station.html", val=res)


@app.route("/block_station")
def block_station():
    id = request.args.get('id')
    qry = "update login set type = 'blocked' where id = %s"
    iud(qry, id)
    return '''<script>alert("Blocked");window.location="block_charging_station"</script>'''


@app.route("/unblock_station")
def unblock_station():
    id = request.args.get('id')
    qry = "update login set type = 'station' where id = %s"
    iud(qry, id)
    return '''<script>alert("Unblocked");window.location="block_charging_station"</script>'''


@app.route('/view_complaint', methods=['get', 'post'])
def view_complaint():

    qry = "SELECT `user`.`name`,`complaints`.* FROM `complaints` JOIN `user` ON `complaints`.`lid`=`user`.`lid` where complaints.reply='pending'"
    res = selectall(qry)

    return render_template("Admin/view_complaint.html", val=res)


@app.route('/send_reply', methods=['get', 'post'])
def send_reply():
    id = request.args.get('id')
    session['cid'] = id
    return render_template("Admin/send_reply.html")


@app.route('/send_reply2', methods=['post'])
def send_reply2():
    reply = request.form['textfield']
    qry = "update complaints set reply=%s where id =%s"
    iud(qry,(reply,session['cid']))
    return '''<script>alert("Success");window.location="view_complaint"</script>'''


@app.route('/view_rating', methods=['get', 'post'])
def view_rating():

    qry = "SELECT `charging_station`.`name` AS sname,`user`.name,`rating_review`.* FROM `rating_review` JOIN `charging_station` ON `rating_review`.sid=`charging_station`.lid JOIN `user` ON `rating_review`.uid = `user`.lid"
    res = selectall(qry)

    return render_template("Admin/view_rating.html", val=res)


@app.route("/station_home")
def station_home():
    return render_template("Station/station_index.html")


@app.route("/view_booking")
def view_booking():
    qry = "SELECT `user`.`name`,phone, `slots`.`from_time`,`to_time`, `booking`.* FROM `booking` JOIN `slots` ON `booking`.`sid`=`slots`.`id` JOIN `user` ON `booking`.`lid` = `user`.`lid` WHERE `slots`.`lid`=%s and booking.status='pending'"
    res = selectall2(qry, session['lid'])
    return render_template("Station/view_bookings.html", val=res)


@app.route("/view_accepted_booking")
def view_accepted_booking():
    qry = "SELECT `user`.`name`,phone, `slots`.`from_time`,`to_time`, `booking`.* FROM `booking` JOIN `slots` ON `booking`.`sid`=`slots`.`id` JOIN `user` ON `booking`.`lid` = `user`.`lid` WHERE `slots`.`lid`=%s and booking.status='accepted'"
    res = selectall2(qry, session['lid'])
    return render_template("Station/view_accepted_bookings.html", val=res)


@app.route("/accept_booking")
def accept_booking():
    id = request.args.get("id")
    qry = "UPDATE `booking` SET `status`='accepted' WHERE `id`=%s"
    iud(qry, id)
    return '''<script>alert("Successfully accepted");window.location="view_booking"</script>'''


@app.route("/reject_booking")
def reject_booking():
    id = request.args.get("id")
    qry = "UPDATE `booking` SET `status`='rejected' WHERE `id`=%s"
    iud(qry, id)
    return '''<script>alert("Successfully accepted");window.location="view_booking"</script>'''


@app.route('/view_rating2', methods=['get', 'post'])
def view_rating2():

    qry = "SELECT `user`.`name`,`rating_review`.* FROM `rating_review` JOIN `user` ON `rating_review`.uid = `user`.`lid` WHERE `rating_review`.sid=%s"
    res = selectall2(qry, session['lid'])

    return render_template("Station/view_rating.html", val=res)


@app.route('/manage_slots', methods=['get', 'post'])
def manage_slots():

    qry = "SELECT * FROM `slots` WHERE `lid`=%s"
    res = selectall2(qry, session['lid'])

    return render_template("Station/manage_slots.html", val=res)


@app.route("/delete")
def delete():
    id = request.args.get('id')
    qry = "DELETE FROM `slots` WHERE id=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_slots"</script>'''


@app.route("/add_slots", methods=['post'])
def add_slots():
    return render_template("Station/add_slots.html")


@app.route("/insert_slots", methods=['post'])
def insert_slots():
    from_time = request.form['textfield']
    to_time = request.form['textfield2']
    no_of_slots = request.form['textfield3']

    qry = "INSERT INTO `slots` VALUES(NULL, %s, %s, %s, %s, CURDATE())"
    iud(qry, (session['lid'], from_time, to_time, no_of_slots))

    return '''<script>alert("Successfully Added");window.location="manage_slots"</script>'''


@app.route("/user_home")
def user_home():
    return render_template("User/user_index.html")


@app.route("/view_station")
def view_station():
    return render_template("User/view_station.html")


@app.route("/view_station2", methods=['post'])
def view_station2():
    loc = request.form['textfield']
    qry="SELECT * FROM `charging_station` JOIN `login` ON `charging_station`.lid=`login`.id WHERE `login`.type='station' AND `charging_station`.`place`=%s"
    res = selectall2(qry, loc)
    return render_template("User/view_station.html", val=res)


@app.route("/view_slots2")
def view_slots2():
    id = request.args.get('id')
    qry="SELECT * FROM `slots` WHERE lid=%s"
    res = selectall2(qry, id)
    return render_template("User/view_slots.html", val=res)


@app.route("/book_slots")
def book_slots():
    id = request.args.get('id')
    slots = request.args.get('slots')
    session['sid'] = id
    session['slots'] = slots
    slots = int(slots)
    return render_template("User/book_slots.html", s = slots)


@app.route("/book", methods=['post'])
def book():
    slots = request.form['select']
    qry = "INSERT INTO `booking` VALUES(NULL, %s, %s, CURDATE(), 'pending', %s)"
    iud(qry, (session['lid'], session['sid'], slots))

    qry = "UPDATE `slots` SET `no_of_charging_points`=`no_of_charging_points`-%s WHERE `id`=%s"
    iud(qry,(session['slots'], session['sid']))

    return '''<script>alert("Successfully booked"); window.location="view_station"</script>'''


@app.route("/user_view_complaint")
def user_view_complaint():
    qry = "SELECT * FROM `complaints` WHERE lid=%s"
    res = selectall2(qry, session['lid'])
    return render_template("User/send_complaint.html", val=res)


@app.route("/user_add_complaint", methods=['post'])
def user_add_complaint():
    return render_template("User/add_new_complaint.html")


@app.route("/insert_new_complaint", methods=['post'])
def insert_new_complaint():
    complaint = request.form['textfield']
    qry = "INSERT INTO `complaints` VALUES(NULL,%s,%s,CURDATE(),'pending')"
    iud(qry,(session['lid'], complaint))

    return '''<script>alert("Success"); window.location="user_view_complaint"</script>'''


@app.route('/view_booking_details')
def view_booking_details():
    qry = "SELECT `charging_station`.`name`,`email`,`phone`,`latitude`,`longitude`,charging_station.lid as clid, `slots`.`from_time`,`to_time`,`booking`.* FROM `booking` JOIN `slots` ON `booking`.sid=`slots`.id JOIN `charging_station` ON `slots`.lid=`charging_station`.`lid` WHERE `booking`.lid=%s"
    res = selectall2(qry, session['lid'])
    return render_template("User/view_booking.html", val=res)


@app.route("/report_charging_station")
def report_charging_station():
    id = request.args.get('id')
    session['rsid'] = id
    return render_template("User/report_station.html")


@app.route("/final_report", methods=['post'])
def final_report():
    details = request.form['textfield']
    qry = "INSERT INTO `report` VALUES(NULL, %s, %s, %s, CURDATE(), 'pending')"
    iud(qry, (session['lid'], session['rsid'], details))

    return '''<script>alert("Reported"); window.location="view_booking_details"</script>'''


@app.route("/payment_details")
def payment_details():
    id = request.args.get('id')
    session['booking_id'] = id
    qry = "SELECT * FROM `bill` WHERE bid=%s and status!='pending'"
    res = selectone(qry, id)

    if res is None:
        amount = "No payment yet"
    else:
        amount = res['amount']
        status = res['status']

    return render_template("Station/payment_details.html", amt = amount)


@app.route('/generate_bill', methods=['post'])
def generate_bill():
    qry = "SELECT * FROM `bill` WHERE bid=%s"
    res = selectone(qry, session['booking_id'])

    if res is None:
        amount = "No Bill Generated Yet"
    else:
        amount = res['amount']
    return render_template("Station/generate_bill.html", bill=amount)


@app.route("/generate_bill2", methods=['post'])
def generate_bill2():

    qry = "SELECT * FROM `bill` WHERE bid=%s"
    res = selectone(qry, session['booking_id'])

    if res is None:

        amount = request.form['textfield']
        qry = "INSERT INTO `bill` VALUES(NULL,%s,%s,CURDATE(),'pending')"
        iud(qry,(session['booking_id'], amount))

        return '''<script>alert("Success"); window.location="view_accepted_booking"</script>'''

    else:
        amount = request.form['textfield']
        qry = "UPDATE `bill` SET `amount`=`amount`+ %s WHERE bid=%s"
        iud(qry, (amount, session['booking_id']))

        return '''<script>alert("Success"); window.location="view_accepted_booking"</script>'''


@app.route("/payment_details2")
def payment_details2():
    id = request.args.get('id')

    qry = "SELECT * FROM `bill` WHERE bid=%s"
    res = selectone(qry,id)

    if res is not None:
        session['amt'] = int(res['amount']) * 100
        session['paying_req_id'] = res['id']
    return render_template("User/payment_details.html", val=res)


@app.route('/user_pay_proceed')
def user_pay_proceed():
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': session['amt'], 'currency': "INR", 'payment_capture': '1'})
    return render_template('UserPayProceed.html', p=payment)


@app.route('/user_pay_complete', methods=['post'])
def user_pay_complete():

    qry = "UPDATE `bill` SET STATUS = 'payed' WHERE id = %s"
    iud(qry, session['paying_req_id'])

    return '''<script>alert("payment successful");window.location="user_home"</script>'''


app.run(debug=True)

