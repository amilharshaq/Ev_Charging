from flask import *
from src.dbconnection import *

app = Flask(__name__)

app.secret_key = "74745"


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/login_code',methods=['post'])
def login_code():
    uname=request.form['textfield']
    pswd=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(uname,pswd)
    res=selectone(qry,val)

    if res is None:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''
    elif res['type'] == "admin":
        session['lid']=res['id']
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


app.run(debug = True)