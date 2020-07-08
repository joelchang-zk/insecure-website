import urllib.parse as up
import psycopg2

def setUpDB():
  up.uses_netloc.append("postgres")
  connection = psycopg2.connect(user="hrtaronw", password="nAzNly4037pRe5h5ercGQYap2wNOah79", host="ruby.db.elephantsql.com", port="5432", database="hrtaronw")
  return connection
