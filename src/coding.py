from flask import *
from src.dbconnectionnew import *

app =Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login_code", methods=['POST'])
def login_code():
    username = request.form['textfield']
    password = request.form['textfield2']

    qry = "SELECT * FROM login WHERE username=%s AND password=%s"
    val = (username, password)
    res = selectone(qry, val)

    if res is None:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''
    elif res['type'] == "Admin":
        return '''<script>alert("Welcome Admin");window.location="/admin_home"</script>'''
    elif res['type'] == "User":
        return '''<script>alert("Welcome User");window.location="/user_home"</script>'''
    elif res['type'] == "Volunteer":
        return '''<script>alert("Welcome Volunteer");window.location="/volunteer_home"</script>'''
    else:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''

@app.route("/user_Registration")
def user_Registration():
    return render_template("User/user reg.html")

@app.route("/user_home")
def user_Home():
    return render_template("User/user home.html")

@app.route("/admin_home")
def admin_home():
    return render_template("Admin/admin home.html")

@app.route("/user_sendRequest")
def Send_Request():
    return render_template("User/send request.html")

@app.route("/user_sendRequestview")
def Send_RequestView():
    return render_template("User/send request view details.html")

@app.route("/user_sendRequestsend")
def Send_Requestsend ():
    return render_template("User/send request send details.html")


@app.route("/user_ViewRequest")
def View_Request():
    return render_template("User/view request status.html")

@app.route("/user_sendRequestsend")
def ViewRequestView():
    return render_template("User/view request status2.html")


@app.route("/user_SendComplaint")
def Send_Complaint():
    return render_template("User/send complaint and view reply.html")

@app.route("/user_SendComplaintaddview")
def Send_Complaintaddview():
    return render_template("User/send complaint and view reply 2.html")



@app.route("/user_SendRating")
def Send_Rating():
    return render_template("User/send rating and review 1.html")

@app.route("/user_SendRatingReview")
def Send_RatingReview():
    return render_template("User/send rating and review 2.html")

@app.route("/user_SendRatingAddview")
def Send_RatingAddview():
    return render_template("User/send rating and review 3.html")


@app.route("/Volunteer_Registration")
def Volunteer_Registration():
    return render_template("Volunteer/Volunteer reg.html")



app.run(debug = True)