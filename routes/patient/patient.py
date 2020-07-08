import hashlib
import json

from flask import Blueprint, redirect, render_template, request, url_for

from helper.functions import JSONSerialConvertor, genRandomId
from routes.general.__init__ import connection

patient_blueprint = Blueprint('patient', 'patient',template_folder= 'templates')

@patient_blueprint.route('/<string:username>/patient/records', methods = ['GET', 'POST'])
def patientHomePage(username):
    cursor = connection.cursor()
    nameQuery = "SELECT name from users where username = '" + str(username) + "';"
    cursor.execute(nameQuery)
    nameResults = json.loads(json.dumps(cursor.fetchall()))
    name = str(nameResults[0][0])
    print(name)
    recordsQuery = "SELECT * from records where patientname = '" + str(name) + "';"
    cursor.execute(recordsQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    if len(results) == 0:
        isEmpty = True
        return render_template('patientrecords.html', username = username, isEmpty = isEmpty)
    else:
        return render_template('patientrecords.html', username = username, results = results)

@patient_blueprint.route('/<string:username>/patient/appt', methods = ['GET', 'POST'])
def patientAppt(username):
    cursor = connection.cursor()
    query = "SELECT * from appointment where patientid = '" + str(username) + "' and status = 'approved';"
    cursor.execute(query)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    if len (results) == 0:
        isEmpty = True
        return render_template('patientAppt.html', isEmpty = isEmpty, username = username)
    else:
        return render_template('patientAppt.html', resulst = results, username = username)

@patient_blueprint.route('/<string:username>/patient/new/appt/', methods = ['GET', 'POST'])
def newAppt(username):
    cursor = connection.cursor()
    if request.method == 'POST':
        doctorID = request.form['doctorID']
        date = request.form['apptDate']
        comments = request.form['reason']
        checkQuery = "SELECT * from users where username = '" + str(doctorID) + "' and role = 'doctor';"
        print(checkQuery)
        cursor.execute(checkQuery)
        results = json.loads(json.dumps(cursor.fetchall()))
        print(results)
        if len (results) == 0:
            isError = "There is no such doctor. Please try again"
            return render_template('newAppt.html', username = username, isError = isError)
        else:
            apptId = genRandomId()
            insertQuery = "INSERT INTO appointment(doctorid,patientid,apptdate,status,apptid,comments) VALUES('" + str(doctorID) + "','" + str(username) + "','" + str(date) + "','pending','" + str(apptId) + "','" + str(comments) + "');"
            cursor.execute(insertQuery)
            connection.commit()
            print(insertQuery)
            successMessage = "Appointment has been registered"
            return render_template('newAppt.html', username = username, successMessage = successMessage)
    else:
        return render_template('newAppt.html', username = username)
    
@patient_blueprint.route('/<string:username>/patient/records/<string:recordid>/', methods = ['GET', 'POST'])
def patientDiagnosis(username,recordid):
    cursor = connection.cursor()
    diagnosisQuery = "SELECT * from records where recordid = '" + str(recordid) + "';"
    cursor.execute(diagnosisQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    if request.method == 'POST':
        comments = request.form['patientComments']
        updateQuery = "UPDATE records set patientcomments = '" + str(comments) + "' where recordid = '" + str(recordid) + "';"
        cursor.execute(updateQuery)
        connection.commit()
        successMessage = "Your comments have been updated!"
        return render_template('patientdiagnosis.html', username = username, results = results, successMessage = successMessage)
    return render_template('patientdiagnosis.html', username = username, results = results)
