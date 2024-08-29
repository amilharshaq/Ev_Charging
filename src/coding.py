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
    return render_template("Admin/home.html")


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


app.run(debug = True)