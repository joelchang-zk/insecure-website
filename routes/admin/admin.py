import hashlib
import json

from flask import Blueprint, redirect, render_template, request, url_for

from helper.functions import JSONSerialConvertor
from routes.admin.__init__ import connection

admin_blueprint = Blueprint('admin','admin', template_folder= 'templates')

@admin_blueprint.route('/<string:username>/admin/', methods = ['GET', 'POST'])
def adminHomePage(username):
    cursor = connection.cursor()
    role = "admin"
    usersQuery = "SELECT * from users where role = 'patient' OR role = 'doctor';"
    cursor.execute(usersQuery)
    results = json.loads(json.dumps(cursor.fetchall()))
    if len(results) == 0:
        isEmpty = True
        return render_template('adminhomepage.html', username = username, isEmpty = isEmpty, results = results, role = role)
    else:
        return render_template('adminhomepage.html', username = username, results = results, role = role)

@admin_blueprint.route('/<string:username>/admin/delete/<string:deleteUsername>/', methods = ['GET', 'POST'])
def deleteUsers(username, deleteUsername):
    cursor = connection.cursor()
    deleteQuery = "DELETE from users where username = '" + str(deleteUsername) + "';"
    deleteCookieQuery = "DELETE from cookie where username = '" + str(deleteUsername) + "';"
    cursor.execute(deleteQuery)
    cursor.execute(deleteCookieQuery)
    connection.commit()
    return redirect(url_for('admin.adminHomePage', username = username))

@admin_blueprint.route('/<string:username>/admin/new/user/', methods = ['GET', 'POST'])
def createNewUser(username):
    cursor = connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeatPassword = request.form['repeatPassword']
        role = request.form['role']
        usernameQuery = "SELECT * from users where username = '" + str(username) + "';"
        nameQuery = "SELECT * from users where name = '" + str(name) + "';"
        emailQuery = "SELECT * from users where email = '" + str(email) + "';"
        cursor.execute(usernameQuery)
        usernameResults = json.loads(json.dumps(cursor.fetchall()))
        cursor.execute(emailQuery)
        emailResults = json.loads(json.dumps(cursor.fetchall()))
        cursor.execute(nameQuery)
        nameResults = json.loads(json.dumps(cursor.fetchall()))
        if len(name) == 0 or len(username) == 0 or len(email) == 0 or len(password) == 0 or len(repeatPassword) == 0:
            errorMessage = "The form cannot be left empty. Please try again!"
            return render_template('addNewUser.html', username = username, errorMessage = errorMessage)

        elif len(usernameResults) != 0 or len(nameResults) != 0 or len(emailResults) != 0:
            errorMessage = "Repeated email/username/name. Please try again!"
            return render_template('addNewUser.html', username = username, errorMessage = errorMessage)

        elif password != repeatPassword:
            errorMessage = "Passwords do not match! Please try again!"
            return render_template('addNewUser.html', username = username, errorMessage = errorMessage)
        else:
            hashedPassword = hashlib.md5(str(password).encode()).hexdigest()
            insertQuery = "INSERT INTO USERS(username, password, name, email, role) VALUES('" + str(username) + "','" + str(hashedPassword) + "','" + str(name) + "','" + str(email) + "','" + str(role) + "');"
            cursor.execute(insertQuery)
            cookieQuery = "INSERT into USERS(username, first, second) VALUES('" + str(username) + "',NULL,NULL);"
            cursor.execute(cookieQuery)
            connection.commit()
            successMessage = "User has been successfully added!"
            return render_template('addNewUser.html', username = username, successMessage = successMessage)
    return render_template('addNewUser.html', username = username)

@admin_blueprint.route("/<string:username>/admin/requests/", methods = ['GET', 'POST'])
def adminRequests(username):
    cursor = connection.cursor()
    requestQuery = "SELECT * from requests where status = 'pending';"
    cursor.execute(requestQuery)
    requestResults = json.loads(json.dumps(cursor.fetchall()))
    if len(requestResults) == 0:
        isEmpty = True
        return render_template('adminrequests.html', username = username, isEmpty = isEmpty)
    else:
        return render_template('adminrequests.html', username = username, results = requestResults)

@admin_blueprint.route("/<string:username>/admin/requests/<string:requestid>/delete/", methods = ['GET', 'POST'])
def adminDeleteRequests(username, requestid):
    cursor = connection.cursor()
    deleteQuery = "delete from requests where requestid = '" + str(requestid) + "';"
    cursor.execute(deleteQuery)
    connection.commit()
    return redirect(url_for('admin.adminRequests', username = username))

@admin_blueprint.route("/<string:username>/admin/requests/<string:requestid>/approve/", methods = ['GET', 'POST'])
def adminApproveRequests(username, requestid):
    cursor = connection.cursor()
    approveQuery = "UPDATE requests set status = 'approved' where requestid = '" + str(requestid) + "';"
    cursor.execute(approveQuery)
    connection.commit()
    return redirect(url_for('admin.adminRequests', username = username))

@admin_blueprint.route("/<string:username>/admin/enquiry/", methods = ['GET', 'POST'])
def adminEnquiry(username):
    cursor = connection.cursor()
    selectQuery = "SELECT * from enquiry;"
    cursor.execute(selectQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    if len(results) == 0:
        isEmpty = True
        return render_template('adminenquiry.html', username = username, isEmpty = isEmpty)
    else:
        return render_template('adminenquiry.html', username = username, results = results) 

@admin_blueprint.route("/<string:username>/admin/enquiry/<string:enquiryid>/resolve/", methods = ['GET', 'POST'])
def resolveEnquiry(username, enquiryid):
    cursor = connection.cursor()
    deleteEnquiry = "DELETE from enquiry where enquiryid = '" + str(enquiryid) + "';"
    cursor.execute(deleteEnquiry)
    connection.commit()
    return redirect(url_for('admin.adminEnquiry', username = username))
