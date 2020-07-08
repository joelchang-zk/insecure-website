import hashlib
import os
from datetime import datetime

from flask import redirect, render_template, url_for

from helper.functions import (allowed_file, genRandomId,
                              getRandomAlphaNumericString)


def commitEnquiry(name, email, enquiry, cursor, connection):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    enquiryid = genRandomId()
    insertQuery = "INSERT INTO enquiry(name,email,enquiry,enquiryid,datetime) VALUES ('" + str(name) + "','" + str(
        email) + "','" + str(enquiry) + "','" + str(enquiryid) + "','" + str(current_time) + "');"
    cursor.execute(insertQuery)
    connection.commit()


def checkDoctorLogin(results, cursor, connection, username):
    for x in results:
        storeRole = str(x[4])
    role = storeRole
    if role == "doctor":
        response = redirect(url_for('doctor.doctorHomePage', username=username))
        first = getRandomAlphaNumericString()
        second = getRandomAlphaNumericString()
        updateQuery = "Update cookie set first = '" + \
            str(first) + "', second = '" + str(second) + \
            "' where username = '" + str(username) + "';"
        cursor.execute(updateQuery)
        connection.commit()
        response.set_cookie(first, second)
        return response
    else:
        error = "Invalid Role"
        return render_template("login.html", error=error)


def checkPatientLogin(results, cursor, connection, username):
    for x in results:
        storeRole = str(x[4])
    role = storeRole
    if role == "patient":
        response = redirect(
            url_for('patient.patientHomePage', username=username))
    else:
        error = "Invalid Role"
        return render_template('login.html', error=error)
    first = getRandomAlphaNumericString()
    second = getRandomAlphaNumericString()
    updateQuery = "Update cookie set first = '" + \
        str(first) + "', second = '" + str(second) + \
        "' where username = '" + str(username) + "';"
    cursor.execute(updateQuery)
    connection.commit()
    response.set_cookie(first, second)
    return response


def checkLabTechLogin(results, cursor, connection, username):
    for x in results:
        storeRole = str(x[4])
    role = storeRole
    if role == "lab technician":
        response = redirect(url_for('labtech.LTHomePage', username=username))
    else:
        error = "Invalid Role"
        return render_template('login.html', error=error)
    first = getRandomAlphaNumericString()
    second = getRandomAlphaNumericString()
    updateQuery = "Update cookie set first = '" + \
        str(first) + "', second = '" + str(second) + \
        "' where username = '" + str(username) + "';"
    cursor.execute(updateQuery)
    connection.commit()
    response.set_cookie(first, second)
    return response

def checkAdminLogin(results, cursor, connection, username):
    for x in results:
        storeRole = str(x[4])
    role = storeRole
    if role == "admin":
        response = redirect(
                    url_for('admin.adminHomePage', username=username))
    else:
        error = "Invalid Role"
        return render_template('login.html', error = error)
    first = getRandomAlphaNumericString()
    second = getRandomAlphaNumericString()
    updateQuery = "Update cookie set first = '" + \
                str(first) + "', second = '" + str(second) + \
                    "' where username = '" + str(username) + "';"
    cursor.execute(updateQuery)
    connection.commit()
    response.set_cookie(first, second)
    return response

def changePasswordActions(hashedCurrentPassword, currentPass, repeatPassword, newPassword, cursor, connection, username, role):
    if hashedCurrentPassword != currentPass:
        errorMessage = "The current password field is incorrect. Please try again!"
        return render_template('changepassword.html', username=username, role=role, errorMessage=errorMessage)
    elif newPassword != repeatPassword:
        errorMessage = "New password and repeated passwords are not the same. Please try again!"
        return render_template('changepassword.html', username=username, role=role, errorMessage=errorMessage)
    elif len(newPassword) == 0 or len(repeatPassword) == 0:
        errorMessage = "The password fields cannot be left empty. Please try again!"
        return render_template('changepassword.html', username=username, role=role, errorMessage=errorMessage)
    else:
        hashedNewPassword = hashedCurrentPassword = hashlib.md5(
                str(newPassword).encode()).hexdigest()
        updateQuery = "Update users set password = '" + \
                str(hashedNewPassword) + \
                    "' where username = '" + str(username) + "';"
        cursor.execute(updateQuery)
        connection.commit()
        successMessage = "Password updated successfully"
        return render_template('changepassword.html', username=username, role=role, successMessage=successMessage)

def profileActions(request, cursor, connection, username, ALLOWED_EXTENSIONS, results, role,filedir):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        if request.files:
            image = request.files['profileImage']
            print(image.filename)
            if allowed_file(image.filename, ALLOWED_EXTENSIONS):
                extension = "\\static\\uploads\\" + str(username) + str(image.filename)
                filedir = "/static/uploads/" + str(username) + str(image.filename)
                directory = str(os.getcwd()) + str(extension)
                updateQuery = "UPDATE users set name = '" + str(name) + "', email = '" + str(email) + "', filedir = '" + str(filedir) + "', address = '" + str(address) + "' where username = '" + str(username) + "';"
                cursor.execute(updateQuery)
                connection.commit()
                image.save(directory)
                print("FILE SAVED")
                return render_template('profile.html', username=username, results = results, role = role)
            elif str(image.filename) == "":
                query = "UPDATE users set name = '" + str(name) + "', email = '" + str(email) + "', address = '" + str(address) + "' where username = '" + str(username) + "';"
                cursor.execute(query)
                connection.commit()
                return render_template('profile.html', username=username, results = results, role = role)
            else:
                errorMessage = "Invalid File Types. Only JPEG, JPG and PNG files are allowed."
                return render_template('profile.html', username=username, errorMessage=errorMessage, results = results, role = role)
        else:
            query = "UPDATE users set name = '" + str(name) + "', email = '" + str(email) + "', address = '" + str(address) + "' where username = '" + str(username) + "';"
            cursor.execute(query)
            connection.commit()
            return render_template('profile.html', username=username, results = results, role = role)
    else:
        return render_template('profile.html', username=username, role=role, filedir=filedir, results = results)
