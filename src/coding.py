from flask import *
from src.dbconnectionnew import *
from flask_mail import *
import random

app =Flask(__name__)
app.secret_key ="657349885734895"


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use the server for your mail service
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'foodforlifedonation@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'jnjd eqxp ajlp dyoc'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = ('Food For Life-Donation And Distribution Management System', 'foodforlifedonation@gmail.com')

mail = Mail(app)


@app.route("/")
def login():
    return render_template("login_index.html")

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
        session['lid'] = res['id']
        return '''<script>alert("Welcome Admin");window.location="/admin_home"</script>'''
    elif res['type'] == "User":
        session['lid'] = res['id']
        return '''<script>alert("Welcome User");window.location="/user_home"</script>'''
    elif res['type'] == "Volunteer":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Volunteer");window.location="/Volunteer_Home"</script>'''
    else:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''



@app.route("/admin_home")
def admin_home():
    return render_template("Admin/admin_index.html")

@app.route("/Verify_volunteers")
def Verify_volunteers():

    qry = 'SELECT `volunteer`.* FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE TYPE="pending"'
    res  = selectall(qry)

    return render_template("Admin/Verify volunteers.html", val = res)


@app.route("/accept_volunteer")
def accept_volunteer():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="Volunteer" WHERE `id`=%s'
    iud(qry, id)

    qry = "SELECT * FROM `volunteer` WHERE lid = %s"
    res = selectone(qry, id)


    gmail = res['email']

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been successfully accepted by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'regionalmails@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(gmail)



    return '''<script>alert("Successfully Accepted");window.location="/Verify_volunteers"</script>'''


@app.route("/reject_volunteer")
def reject_volunteer():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="rejected" WHERE `id`=%s'
    iud(qry, id)

    qry = "SELECT * FROM `volunteer` WHERE lid = %s"
    res = selectone(qry, id)

    gmail = res['email']

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been rejected by admin")
        print(msg)
        msg['Subject'] = 'Hey there'
        msg['To'] = email
        msg['From'] = 'regionalmails@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(gmail)


    return '''<script>alert("Rejected");window.location="/Verify_volunteers"</script>'''


@app.route("/Block_Unblock")
def Block_Unblock():
    return render_template("Admin/block unblock.html")


@app.route("/view_block_unblock_details", methods=['post'])
def view_block_unblock_details():

    type = request.form['select']

    if type == "User":
        qry = 'SELECT * FROM `user` JOIN `login` ON `user`.lid = `login`.id WHERE `login`.type = "User" or `login`.type="blocked"'
        res = selectall(qry)
    else:
        qry = 'SELECT * FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE `login`.type ="Volunteer" or `login`.type="blocked"'
        res = selectall(qry)
    return render_template("Admin/block unblock.html", val=res, type = type)


@app.route("/block_user")
def block_user():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="blocked" WHERE `id`=%s'
    iud(qry, id)

    qry = "SELECT * FROM `user` WHERE lid = %s"
    res = selectone(qry, id)

    gmail = res['email']

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been blocked by admin")
        print(msg)
        msg['Subject'] = 'Hey there'
        msg['To'] = email
        msg['From'] = 'foodforlifedonation@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(gmail)

    return '''<script>alert("Blocked");window.location="/Block_Unblock"</script>'''


@app.route("/unblock_user")
def unblock_user():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="User" WHERE `id`=%s'
    iud(qry, id)

    qry = "SELECT * FROM `user` WHERE lid = %s"
    res = selectone(qry, id)

    gmail = res['email']

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been Unblocked by admin")
        print(msg)
        msg['Subject'] = 'Hey there'
        msg['To'] = email
        msg['From'] = 'foodforlifedonation@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(gmail)

    return '''<script>alert("UnBlocked");window.location="/Block_Unblock"</script>'''


@app.route("/block_volunteer")
def block_volunteer():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="blocked" WHERE `id`=%s'
    iud(qry, id)

    qry = "SELECT * FROM `volunteer` WHERE lid = %s"
    res = selectone(qry, id)

    gmail = res['email']

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been blocked by admin")
        print(msg)
        msg['Subject'] = 'Hey there'
        msg['To'] = email
        msg['From'] = 'foodforlifedonation@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(gmail)

    return '''<script>alert("Blocked");window.location="/Block_Unblock"</script>'''


@app.route("/unblock_volunteer")
def unblock_volunteer():
    id = request.args.get('id')
    qry = 'UPDATE `login` SET `type`="Volunteer" WHERE `id`=%s'
    iud(qry, id)

    qry = "SELECT * FROM `volunteer` WHERE lid = %s"
    res = selectone(qry, id)

    gmail = res['email']

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been Unblocked by admin")
        print(msg)
        msg['Subject'] = 'Hey there'
        msg['To'] = email
        msg['From'] = 'foodforlifedonation@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(gmail)

    return '''<script>alert("Blocked");window.location="/Block_Unblock"</script>'''


@app.route("/View_donation")
def View_donation():
    return render_template("Admin/View donation.html")


@app.route("/view_donation_details", methods=['post'])
def view_donation_details():
    location=request.form['textfield']
    date=request.form['textfield2']

    qry = "SELECT `user`.`fname` as ufname,`user`.`lname` as ulname,`volunteer`.`fname` as vfname,`volunteer`.`lname` as vlname,`requestdetails`.`status`,`request`.`details` FROM `request` JOIN `requestdetails`ON `request`.id = `requestdetails`.`requestid` JOIN `volunteer` ON `requestdetails`.`volunteerid`=`volunteer`.`lid` JOIN `user`ON `request`.`userid`=`user`.lid WHERE `request`.`date`=%s AND `volunteer`.`location`=%s"
    res = selectall2(qry, (date, location))

    return render_template("Admin/View donation.html", val=res)



@app.route("/Complaint_reply")
def Complaint_reply():

    return render_template("Admin/complaint And reply.html")


@app.route("/insert_reply", methods=['post'])
def insert_reply():
    reply = request.form['textfield']
    qry = "UPDATE `complaint` SET reply = %s WHERE id = %s"
    iud(qry,(reply, session['cid']))
    return render_template("Admin/complaint And reply.html")


@app.route("/display_complaint", methods=['post'])
def display_complaint():
    complaint_type = request.form['select']
    user_type = request.form['select2']

    if complaint_type == "Pending":
        if user_type == "User":
            qry = 'SELECT * FROM `complaint` JOIN `user` ON `complaint`.`lid`=`user`.lid WHERE `complaint`.`reply`="pending"'
            res = selectall(qry)
            return render_template("Admin/complaint And reply.html", val=res, utype = user_type, ctype = complaint_type)
        else:
            qry = 'SELECT * FROM `complaint` JOIN `volunteer` ON `complaint`.`lid`=`volunteer`.lid WHERE `complaint`.`reply`="pending"'
            res = selectall(qry)
            return render_template("Admin/complaint And reply.html", val=res, utype = user_type, ctype = complaint_type)
    else:
        if user_type == "User":
            qry = 'SELECT * FROM `complaint` JOIN `user` ON `complaint`.`lid`=`user`.lid WHERE `complaint`.`reply`!="pending"'
            res = selectall(qry)
            return render_template("Admin/complaint And reply.html", val=res, utype = user_type, ctype = complaint_type)
        else:
            qry = 'SELECT * FROM `complaint` JOIN `volunteer` ON `complaint`.`lid`=`volunteer`.lid WHERE `complaint`.`reply`!="pending"'
            res = selectall(qry)
            return render_template("Admin/complaint And reply.html", val=res, utype = user_type, ctype = complaint_type)


@app.route("/Reply")
def Reply():
    id = request.args.get('id')
    session['cid'] = id
    return render_template("Admin/reply.html")

@app.route("/Rating_review")
def Rating_review():
    qry = 'SELECT `volunteer`.`fname`,`volunteer`.`lname`,`volunteer`.`lid` FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE `login`.`type`="Volunteer"'
    res = selectall(qry)
    return render_template("Admin/rating and review.html", val = res)


@app.route("/view_rating_review", methods=['post'])
def view_rating_review():
    vid = request.form['select']

    qry = 'SELECT `volunteer`.`fname`,`volunteer`.`lname`,`volunteer`.`lid` FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE `login`.`type`="Volunteer"'
    res = selectall(qry)

    qry = 'SELECT `user`.`fname`,`user`.`lname`,`ratingreview`.* FROM `ratingreview` JOIN `user` ON `ratingreview`.`userid`=`user`.`lid` WHERE `ratingreview`.`volunteerid`=%s'
    res2 = selectall2(qry, vid)
    return render_template("Admin/rating and review.html", val = res, val2 = res2, vid=vid)


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

    qry="INSERT INTO `login` VALUES(NULL, %s, %s, 'Pending')"
    val= (username,password)
    id= iud(qry, val)

    session['puserid'] = id

    qry="INSERT INTO `user` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    val= (id, fname, lname, phone, place, post, pin, email)

    iud(qry, val)

    random_number = random.randint(1000, 9999)

    print(random_number)

    s = random_number
    session['otp'] = random_number

    def mail(s, email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('foodforlifedonation@gmail.com', 'jnjd eqxp ajlp dyoc')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Your OTP to verify Email: " + str(s)+ " Dont share your OTP")
        print(msg)
        msg['Subject'] = 'Verify your email'
        msg['To'] = email
        msg['From'] = 'regionalmails@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(s,email)

    return render_template("User/otp.html")


@app.route("/Verify_otp", methods=['post'])
def Verify_otp():
    otp = request.form['textfield']
    print(otp,session['otp'])
    if int(otp) == int(session['otp']):
        qry = "update login set type='User' where id = %s"
        iud(qry, session['puserid'])
        return '''<script>alert("Registration Success");window.location="/"</script>'''
    else:
        return '''<script>alert("Invalid otp");window.location="/"</script>'''


@app.route("/user_home")
def user_Home():
    return render_template("User/user_index.html")


@app.route("/user_sendRequest")
def Send_Request():
    return render_template("User/send request.html")


@app.route("/search_volunteer", methods=['post'])
def search_volunteer():
    button = request.form['send_button']

    if button == "Search":
        location = request.form['textfield']
        qry = "SELECT * FROM `volunteer` JOIN `login` ON `volunteer`.lid = `login`.id WHERE `location`=%s AND `login`.type= 'Volunteer'"
        res = selectall2(qry, location)
        return render_template("User/send request.html", val=res, loc = location)
    else:
        vid = request.form.getlist('checkbox')

        if len(vid) == 0:
            return '''<script>alert("Please select atleast one volunteer");window.location="user_sendRequest"</script>'''
        else:
            session['vlist'] = vid
            print(session['vlist'])
            return render_template("User/send request send details.html")


@app.route("/insert_request", methods=['post'])
def insert_request():
    food_req = request.form['textfield']
    details = request.form['textfield2']
    lati = request.form['textfield3']
    longi = request.form['textfield4']

    qry = "INSERT INTO `request` VALUES(NULL, %s , %s, %s, CURDATE(), %s, %s)"
    id = iud(qry, (session['lid'], food_req, details, lati, longi))

    volunteer_list = session['vlist']

    for i in volunteer_list:
        qry = "INSERT INTO `requestdetails` VALUES(NULL, %s, %s, 'pending')"
        iud(qry, (id, int(i)))

    return '''<script>alert("Success");window.location="user_sendRequest"</script>'''


@app.route("/user_sendRequestview")
def Send_RequestView():
    id = request.args.get('id')
    qry = "SELECT `user`.`fname`,`lname`,`ratingreview`.* FROM `ratingreview` JOIN `user` ON `ratingreview`.userid = user.lid WHERE `ratingreview`.`volunteerid`=%s"
    res = selectall2(qry, id)
    return render_template("User/send request view details.html", val=res)



@app.route("/user_ViewRequest")
def View_Request():
    qry = "SELECT * FROM `request` WHERE `userid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("User/view request status.html", val=res)

@app.route("/user_viewRequestview")
def ViewRequestView():
    id = request.args.get('id')
    qry = "SELECT `volunteer`.`fname`,`lname`,`requestdetails`.`status` FROM `requestdetails` JOIN `volunteer` ON `requestdetails`.`volunteerid`=`volunteer`.`lid` WHERE `requestdetails`.`requestid`=%s"
    res = selectall2(qry, id)
    return render_template("User/view request status2.html", val=res)


@app.route("/user_SendComplaint")
def Send_Complaint():
    qry = "SELECT * FROM `complaint` WHERE `lid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("User/send complaint and view reply.html", val=res)

@app.route("/delete_complaint")
def delete_complaint():
    id = request.args.get('id')
    qry = "DELETE FROM `complaint` WHERE `id`=%s"
    iud(qry, id)
    return '''<script>alert("Deleted");window.location="user_SendComplaint"</script>'''

@app.route("/user_SendComplaintaddview", methods=['post'])
def Send_Complaintaddview():
    return render_template("User/send complaint and view reply 2.html")


@app.route("/insert_complaint", methods=['post'])
def insert_complaint():
    complaint = request.form['textfield']
    qry = "INSERT INTO `complaint` VALUES(NULL, %s, %s, 'pending', CURDATE())"
    iud(qry, (session['lid'], complaint))
    return '''<script>alert("success");window.location="user_SendComplaint"</script>'''



@app.route("/user_SendRating")
def Send_Rating():
    qry = "SELECT `volunteer`.`fname`,`lname`,lid,`request`.* FROM `request` JOIN `requestdetails` ON `request`.`id`=`requestdetails`.`requestid` JOIN `volunteer` ON `requestdetails`.`volunteerid`=`volunteer`.`lid` WHERE `request`.`userid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("User/send rating and review 1.html", val=res)

@app.route("/user_SendRatingReview")
def Send_RatingReview():
    id = request.args.get('id')
    session['vid'] = id
    qry = "SELECT * FROM `ratingreview` WHERE `volunteerid`=%s"
    res = selectall2(qry, id)
    return render_template("User/send rating and review 2.html", val=res)

@app.route("/user_SendRatingAddview", methods=['post'])
def Send_RatingAddview():
    return render_template("User/send rating and review 3.html")


@app.route("/insert_rating", methods=['post'])
def insert_rating():
    rating = request.form['textfield']
    review = request.form['textfield2']
    qry = "INSERT INTO `ratingreview` VALUES(NULL, %s, %s, %s, %s, CURDATE())"
    iud(qry, (session['lid'], session['vid'],rating,review))
    return '''<script>alert("success");window.location="user_SendRating"</script>'''


@app.route("/delete_rating")
def delete_rating():
    id = request.args.get('id')
    qry = "DELETE FROM `ratingreview` WHERE `id`=%s"
    iud(qry, id)
    return '''<script>alert("Deleted");window.location="user_SendRating"</script>'''


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
    return render_template("Volunteer/volunteer_index.html")

@app.route("/View_request_volunteer")
def View_request_volunteer():
    qry = "SELECT `user`.fname,lname,`request`.*,requestdetails.id as reqdid FROM `request` JOIN `user` ON `request`.userid = `user`.lid JOIN `requestdetails` ON `request`.id=`requestdetails`.`requestid` WHERE `requestdetails`.`volunteerid`=%s and `requestdetails`.status='pending'"
    res = selectall2(qry, session['lid'])
    return render_template("Volunteer/View Request.html", val=res)


@app.route("/accept_request")
def accept_request():
    id = request.args.get('id')
    reqid = request.args.get('reqid')
    qry = "UPDATE `requestdetails` SET `status`='Accepted' WHERE `id`=%s"
    iud(qry, reqid)

    qry = "DELETE FROM `requestdetails` WHERE `requestid`=%s AND `volunteerid`!=%s"
    iud(qry,(id, session['lid']))

    return '''<script>alert("Successfully Accepted");window.location="View_request_volunteer"</script>'''


@app.route("/reject_request")
def reject_request():
    id = request.args.get('id')
    qry = "UPDATE `requestdetails` SET `status`='rejected' WHERE `id`=%s"
    iud(qry, id)
    return '''<script>alert("Successfully Rejected ");window.location="View_request_volunteer"</script>'''


@app.route("/Manage_request_volunteer")
def Manage_request_volunteer():
    qry = "SELECT `user`.`fname`,`lname`,`request`.*,`requestdetails`.`status` FROM `request` JOIN `user` ON `request`.`userid`=`user`.`lid` JOIN `requestdetails` ON `request`.`id`=`requestdetails`.`requestid` WHERE `requestdetails`.`volunteerid`=%s and requestdetails.status!='pending' and requestdetails.status!='rejected'"
    res = selectall2(qry, session['lid'])
    return render_template("Volunteer/manage request status.html", val=res)

@app.route("/Manage_requestdetails_volunteer")
def Manage_requestdetails_volunteer():
    id = request.args.get('id')
    session['reqid'] = id
    return render_template("Volunteer/manage rqst status 2.html")


@app.route("/update_reqst", methods=['post'])
def update_reqst():
    status = request.form['textfield']
    qry = "UPDATE `requestdetails` SET `status`=%s where id=%s"
    iud(qry, (status, session['reqid']))
    return '''<script>alert("Success");window.location="/Manage_request_volunteer"</script>'''


@app.route("/Sendcomplaint_viewreply_volunteer")
def Sendcomplaint_viewreply_volunteer():
    qry = "SELECT * FROM `complaint` WHERE `lid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Volunteer/Send compliant & view reply.html", val=res)


@app.route("/delete_complaint2")
def delete_complaint2():
    id = request.args.get('id')
    qry = "DELETE FROM `complaint` WHERE `id`=%s"
    iud(qry, id)
    return '''<script>alert("Deleted");window.location="Sendcomplaint_viewreply_volunteer"</script>'''


@app.route("/add_new_complaint", methods=['post'])
def add_new_complaint():
    return render_template("Volunteer/Add new complaint.html")


@app.route("/insert_complaint2", methods=['post'])
def insert_complaint2():
    complaint = request.form['textfield']
    qry = "INSERT INTO `complaint` VALUES(NULL, %s, %s, 'pending', CURDATE())"
    iud(qry, (session['lid'], complaint))
    return '''<script>alert("success");window.location="Sendcomplaint_viewreply_volunteer"</script>'''


@app.route("/Viewrating_review_volunteer")
def Viewrating_review_volunteer():
    qry = "SELECT `ratingreview`.*,`user`.`fname`,`lname` FROM `ratingreview` JOIN `user` ON `ratingreview`.userid=`user`.`lid` WHERE `ratingreview`.`volunteerid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Volunteer/View rating and review.html", val = res)

app.run(debug = True)