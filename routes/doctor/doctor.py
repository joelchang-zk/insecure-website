import json
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from helper.functions import JSONSerialConvertor, genRandomId
from routes.doctor.__init__ import connection

doctor_blueprint = Blueprint('doctor','doctor', template_folder= 'templates')

@doctor_blueprint.route('/<string:username>/doctor/records', methods=['GET', 'POST'])
def doctorHomePage(username):
    cursor = connection.cursor()
    recordsQuery = "SELECT * from records where doctorid = '" + \
        str(username) + "';"
    cursor.execute(recordsQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    if len(results) == 0:
        isEmpty = True
        return render_template('doctorrecords.html', username=username, isEmpty=isEmpty, results=results)
    else:
        if request.method == 'POST':
            name = request.form['queryName']
            searchQuery = "SELECT * from records where patientname = '" + str(name) + "';"
            cursor.execute(searchQuery)
            searchResults = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
            if len(searchResults) == 0:
                emptySearch = True
                return render_template('doctorsearchrecords.html', username = username, emptySearch = emptySearch)
            else:
                return render_template('doctorsearchrecords.html', username = username, searchResults = searchResults)
        else:
            return render_template('doctorrecords.html', username=username, results=results)

@doctor_blueprint.route('/<string:username>/doctor/appt/view/', methods = ['GET', 'POST'])
def doctorViewAppt(username):
    cursor = connection.cursor()
    viewQuery = "SELECT * from appointment where doctorid = '" + str(username) + "' and status = 'approved';"
    cursor.execute(viewQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    print(results)
    if len(results) == 0:
        isEmpty = True
        return render_template('doctorViewAppt.html', isEmpty = isEmpty, username = username)
    else:
        return render_template('doctorViewAppt.html', results = results, username = username)

@doctor_blueprint.route('/<string:username>/doctor/appt/check/', methods = ['GET', 'POST'])
def doctorCheckAppt(username):
    cursor = connection.cursor()
    checkQuery = "SELECT * from appointment where doctorid = '" + str(username) + "' and status = 'pending';"
    cursor.execute(checkQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    if len(results) == 0:
        isEmpty = True
        return render_template('doctorCheckAppt.html', isEmpty = isEmpty, username = username)
    else:
        return render_template('doctorCheckAppt.html', results = results, username = username)

@doctor_blueprint.route('/<string:username>/doctor/<string:apptid>/delete/', methods = ['GET', 'POST'])
def doctorDeleteAppt(username, apptid):
    cursor = connection.cursor()
    deleteQuery = "DELETE from appointment where doctorid = '" + str(username) + "' and apptid = '" + str(apptid) + "';"
    cursor.execute(deleteQuery)
    connection.commit()
    return redirect(url_for('doctor.doctorCheckAppt', username = username))

@doctor_blueprint.route('/<string:username>/doctor/<string:apptid>/approve/', methods = ['GET', 'POST'])
def doctorApproveAppt(username, apptid):
    cursor = connection.cursor()
    updateQuery = "UPDATE appointment set status = 'approved' where doctorid = '" + str(username) + "' and apptid = '" + str(apptid) + "';"
    cursor.execute(updateQuery)
    connection.commit()
    return redirect(url_for('doctor.doctorCheckAppt', username = username))

@doctor_blueprint.route('/<string:username>/doctor/records/<string:recordid>/new/request/', methods=['GET', 'POST'])
def doctorNewRequest(username, recordid):
    cursor = connection.cursor()
    if request.method == 'POST':
        requestID = genRandomId()
        reason = request.form['reason']
        doctorid = request.form['requestID']
        print("REASON: " + str(reason))
        checkQuery = "SELECT * from users where username = '" + str(doctorid) + "';"
        cursor.execute(checkQuery)
        results = json.loads(json.dumps(cursor.fetchall()))
        if len(doctorid) == 0 or len(reason) == 0:
           errorMessage = "The fields cannot be left empty. Please try again!"
           return render_template('doctorrequest.html', username=username, recordid=recordid, errorMessage=errorMessage)
        elif len(results) == 0 or doctorid == username:
            errorMessage = "Invalid doctor id! Please try again!"
            return render_template('doctorrequest.html', username = username, recordid = recordid, errorMessage = errorMessage)
        else:
            updateQuery = "INSERT INTO requests(doctorid,reason,requestid,recordid,requestingdoctorid) VALUES ('" + str(doctorid) + "','" + str(reason) + "','" + str(requestID) + "','" + str(recordid) + "','" + str(username) + "');"
            print(updateQuery)
            cursor.execute(updateQuery)
            connection.commit()
            successMessage = "Your request has been made successfully!"
            return render_template('doctorrequest.html', username = username, recordid = recordid, successMessage = successMessage)
    return render_template('doctorrequest.html', username = username, recordid = recordid)

@doctor_blueprint.route('/<string:username>/doctor/records/<string:recordid>/', methods = ['GET', 'POST'])
def doctorDiagnosis(username, recordid):
    cursor = connection.cursor()
    diagnosisQuery = "SELECT * from records where recordid = '" + str(recordid) + "';"
    cursor.execute(diagnosisQuery)
    results = json.loads(json.dumps(cursor.fetchall(),default=JSONSerialConvertor))
    if request.method == 'POST':
        condition = request.form['patientCondition']
        diagnosis = request.form['patientDiagnosis']
        followup = request.form['doctorFollowUp']
        updateQuery = "UPDATE records set condition = '" + str(condition) + "', diagnosis = '" + str(diagnosis) + "', followup = '" + str(followup) + "' where recordid = '" + str(recordid) + "';"
        cursor.execute(updateQuery)
        connection.commit()
        successMessage = "Diagnosis has been updated successfully!"
        return render_template('doctordiagnosis.html', username = username, results = results, successMessage = successMessage)
    else:
        return render_template('doctordiagnosis.html', username = username, results = results)

@doctor_blueprint.route('/<string:username>/doctor/records/new/', methods = ['GET', 'POST'])
def doctorNewRecords(username):
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['patientName']
        weight = request.form['patientWeight']
        height = request.form['patientHeight']
        bp = request.form['patientBP']
        temp = request.form['patientTemp']
        diagnosis = request.form['patientDiagnosis']
        condition =request.form['patientCondition']
        followup = request.form['follow-up']
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        recordid = genRandomId()
        checkNameQuery = "SELECT * from users where name = '" + str(name) + "' and role = 'patient';"
        cursor.execute(checkNameQuery)
        checkResults = json.loads(json.dumps(cursor.fetchall()))
        if len(checkResults) == 0:
            errorMessage = "Invalid User! Please try again!"
            return render_template('doctornewrecords.html', username = username, errorMessage = errorMessage)
        elif len(name) == 0 or len(weight) == 0 or len(height) == 0 or len(bp) == 0 or len(temp) == 0 or len(diagnosis) == 0 or len(condition) == 0:
            errorMessage = "Fields cannot be left empty. Please try again!"
            return render_template('doctornewrecords.html', username = username, errorMessage = errorMessage)
        else:    
            addQuery = "INSERT into records (patientname, doctorid, height, weight, bp, temp, condition,diagnosis, followup, datetime, recordid) VALUES('" + str(name) + "','" + str(username) + "','" + str(height) + "','" + str(weight) + "','" + str(bp) + "','" + str(temp) + "','" + str(condition) + "','" + str(diagnosis) + "','" + str(followup) + "','"+ str(current_time) + "','" + str(recordid) + "');"
            cursor.execute(addQuery)
            connection.commit()
            successMessage = "New Record has been added!"
            return render_template("doctornewrecords.html", username = username, successMessage = successMessage)
    return render_template('doctornewrecords.html', username = username)
