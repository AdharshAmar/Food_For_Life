from flask import *
from src.dbconnectionnew import *

app =Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/user_Registrartion")
def user_registration():
    return render_template("User/user reg.html")

@app.route("/user_Home")
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