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


@app.route('/admin_home')
def admin_home():
    return render_template("Admin/home.html")


app.run(debug = True)