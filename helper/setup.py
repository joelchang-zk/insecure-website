# import psycopg2
# import os

# def setUpDB():
#     DATABASE_URL = os.environ['DATABASE_URL']
#     connection = psycopg2.connect(DATABASE_URL, sslmode='require')
#     return connection

import os
import urllib.parse as up
import psycopg2

def setUpDB():
  up.uses_netloc.append("postgres")
  conn = psycopg2.connect(database='hrtaronw',
  user='hrtaronw'
  password='nAzNly4037pRe5h5ercGQYap2wNOah79',
  host='ruby.db.elephantsql.com',
  port='5432'
  )
  return conn
