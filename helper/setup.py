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
  url = up.urlparse(os.environ["postgres://hrtaronw:nAzNly4037pRe5h5ercGQYap2wNOah79@ruby.db.elephantsql.com:5432/hrtaronw"])
  conn = psycopg2.connect(database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
  )
  return conn
