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



@app.route("/admin_home")
def admin_home():
    return render_template("Admin/admin home.html")

@app.route("/Verify_volunteers")
def Verify_volunteers():

    qry = 'SELECT `volunteer`.* FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE TYPE="pending"'
    res = selectall(qry)

    return render_template("Admin/Verify volunteers.html", val = res)

@app.route("/Block_Unblock")
def Block_Unblock():
    return render_template("Admin/block unblock.html")


@app.route("/view_block_unblock_details", methods=['post'])
def view_block_unblock_details():

    type = request.form['select']

    if type == "User":
        qry = 'SELECT * FROM `user` JOIN `login` ON `user`.lid = `login`.id WHERE `login`.type != "pending"'
        res = selectall(qry)
    else:
        qry = 'SELECT * FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE `login`.type !="pending"'
        res = selectall(qry)
    print(res)
    return render_template("Admin/block unblock.html", val=res, type = type)


@app.route("/View_donation")
def View_donation():
    return render_template("Admin/View donation.html")

@app.route("/Complaint_reply")
def Complaint_reply():
    return render_template("Admin/complaint And reply.html")

@app.route("/Reply")
def Reply():
    return render_template("Admin/reply.html")

@app.route("/Rating_review")
def Rating_review():
    return render_template("Admin/rating and review.html")


@app.route("/user_Registration")
def user_Registration():
    return render_template("User/user reg.html")

@app.route("/user_register_code",methods=['post'])
def user_register_code():
    fname=request.form["textfield"]
    lname = request.form["textfield2"]
    phone = request.form["textfield3"]
    email = request.form["textfield4"]
    place = request.form["textfield5"]
    post = request.form["textfield6"]
    pin = request.form["textfield7"]
    username = request.form["textfield8"]
    password = request.form["textfield9"]

    qry="INSERT INTO `login` VALUES(NULL, %s, %s, 'User')"
    val= (username,password)
    id= iud(qry, val)

    qry="INSERT INTO `user` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    val= (id, fname, lname, phone, place, post, pin, email)

    iud(qry, val)

    return '''<script>alert("Registration successfull");window.location="/"</script>'''



@app.route("/user_home")
def user_Home():
    return render_template("User/user home.html")


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

@app.route("/user_viewRequestview")
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

@app.route("/Volunteer_register_code",methods=['post'])
def Volunteer_register_code():
    fname=request.form["textfield"]
    lname = request.form["textfield2"]
    phone = request.form["textfield22"]
    email = request.form["textfield23"]
    place = request.form["textfield24"]
    post = request.form["textfield25"]
    pin = request.form["textfield26"]
    location = request.form["textfield27"]
    username = request.form["textfield28"]
    password = request.form["textfield29"]

    qry="INSERT INTO `login` VALUES(NULL, %s, %s, 'pending')"
    val= (username,password)
    id= iud(qry, val)

    qry="INSERT INTO `volunteer` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val= (id, fname, lname, phone,email, place, post, pin,location)

    iud(qry, val)

    return '''<script>alert("Registration successfull");window.location="/"</script>'''




@app.route("/Volunteer_Home")
def Volunteer_Home():
    return render_template("Volunteer/volunteer home.html")

@app.route("/View_request_volunteer")
def View_request_volunteer():
    return render_template("Volunteer/View Request.html")

@app.route("/Manage_request_volunteer")
def Manage_request_volunteer():
    return render_template("Volunteer/manage request status.html")

@app.route("/Manage_requestdetails_volunteer")
def Manage_requestdetails_volunteer():
    return render_template("Volunteer/manage rqst status 2.html")


@app.route("/Sendcomplaint_viewreply_volunteer")
def Sendcomplaint_viewreply_volunteer():
    return render_template("Volunteer/Send compliant & view reply.html")


@app.route("/Viewrating_review_volunteer")
def Viewrating_review_volunteer():
    return render_template("Volunteer/View rating and review.html")

app.run(debug = True)