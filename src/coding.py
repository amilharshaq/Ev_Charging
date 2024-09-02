from flask import *
from src.dbconnection import *

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
    qry = "SELECT `user`.`name`, `slots`.`from_time`,`to_time`, `booking`.* FROM `booking` JOIN `slots` ON `booking`.`sid`=`slots`.`lid` JOIN `user` ON `booking`.`lid` = `user`.`lid` WHERE `slots`.`lid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Station/view_bookings.html", val=res)


@app.route("/accept_booking")
def accept_booking():
    id = request.args.get("id")
    qry = "UPDATE `booking` SET `status`='station' WHERE `id`=%s"
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


app.run(debug=True)

